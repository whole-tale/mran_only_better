# A simple fastAPI app that takes a snapshot date and
# fetches proper source from CRAN
import pyreadr
from typing import Annotated
from fastapi.param_functions import Header
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
import datetime
import requests
import uvicorn

app = FastAPI()
if not os.path.exists("cran.toc.rds"):
    print("Downloading cran.toc.rds")
    r = requests.get("https://groundhogr.com/cran.toc.rds", allow_redirects=True)
    open("cran.toc.rds", "wb").write(r.content)
CRAN_TOC = pyreadr.read_r("cran.toc.rds")[None]

# CORS
origins = [
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


async def get_snapshot(date: str):
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    result = CRAN_TOC[CRAN_TOC["Published"] <= date]
    last_date = result.groupby("Package")["Published"].max()
    result = result[
        result.apply(lambda row: row["Published"] == last_date[row["Package"]], axis=1)
    ]

    # iterate over rows with iterrows()
    # and print each row if it's not None
    # This is slow as hell, but it works
    for index, row in result.iterrows():
        for col in result.columns:
            if row[col]:
                yield f"{col}: {row[col]}\n"
        yield "\n"


@app.get("/linux/bionic/src/contrib/{filename}")
async def get_pkg(filename: str, user_agent: Annotated[str | None, Header()] = None):
    R_version = user_agent.split(" ")[0][2:]
    if os.path.exists(f"data/{R_version}/{filename}"):
        return FileResponse(f"data/{R_version}/{filename}", filename=filename)
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/snapshot/{date}/src/contrib/{filename}")
async def get_file(date: str, filename: str):
    if filename.startswith("PACKAGES"):
        if filename != "PACKAGES":
            raise HTTPException(status_code=404, detail="File not found")
        return StreamingResponse(get_snapshot(date), media_type="text/plain")

    # check if filename exists at https://cran.r-project.org/src/contrib/
    # and if not try the Archive
    base_url = "https://cran.r-project.org/src/contrib/"
    for url in [
        base_url,
        f"{base_url}Archive/{os.path.basename(filename).rsplit('_')[0]}/",
    ]:
        r = requests.get(url + filename, allow_redirects=True, stream=True)
        print(r.status_code, r.url)
        if r.status_code == 200:
            return StreamingResponse(r.raw, media_type="application/x-gzip")
    else:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
