# Better Than MRAN^{TM}

A very simple http server that serves /snapshot/{date} for getting R source packages for a given date straight from
CRAN.

## Example usage from R

```
> options(repos = c(CRAN = "http://localhost:8000/snapshot/2021-12-01"))
> install.packages('ctv')
Installing package into '/usr/local/lib/R/site-library'
(as 'lib' is unspecified)
trying URL 'http://localhost:8000/snapshot/2021-12-01/src/contrib/ctv_0.8-5.tar.gz'
downloaded 355 KB

* installing *source* package 'ctv' ...
** package 'ctv' successfully unpacked and MD5 sums checked
** using staged installation
** R
** inst
** byte-compile and prepare package for lazy loading
** help
*** installing help indices
** building package indices
** installing vignettes
** testing if installed package can be loaded from temporary location
** testing if installed package can be loaded from final location
** testing if installed package keeps a record of temporary installation path
* DONE (ctv)

The downloaded source packages are in
	'/tmp/Rtmp4fRWmH/downloaded_packages'
> options(repos = c(CRAN = "http://localhost:8000/snapshot/2022-12-01"))
> install.packages('ctv')
Installing package into '/usr/local/lib/R/site-library'
(as 'lib' is unspecified)
trying URL 'http://localhost:8000/snapshot/2022-12-01/src/contrib/ctv_0.9-4.tar.gz'
downloaded 85 KB

* installing *source* package 'ctv' ...
** package 'ctv' successfully unpacked and MD5 sums checked
** using staged installation
** R
** inst
** byte-compile and prepare package for lazy loading
** help
*** installing help indices
*** copying figures
** building package indices
** installing vignettes
** testing if installed package can be loaded from temporary location
** testing if installed package can be loaded from final location
** testing if installed package keeps a record of temporary installation path
* DONE (ctv)

The downloaded source packages are in
	'/tmp/Rtmp4fRWmH/downloaded_packages'
```

### Extras

```
options(repos = c(CRAN = "http://localhost:8000/snapshot/2023-05-01", WT = "http://localhost:8000/linux/bionic/", pkgType = "linux/bionic"), HTTPUserAgent = sprintf("R/%s R (%s)", getRversion(), paste(getRversion(), R.version["platform"], R.version["arch"], R.version["os"])))
```

Put binary packages in data/`R_version`/. Run:

```
cd data/<R_version>
R
> write_PACKAGES(latestOnly=FALSE, addFiles=TRUE)
```
