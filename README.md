# NEPC

<!--[![pipeline status](http://predator.nrl.navy.mil/padamson/nepc/badges/master/pipeline.svg)](http://predator.nrl.navy.mil/padamson/nepc/commits/master)
-->
[![pytest coverage report](https://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/pytest.svg?job=pytest)](https://predator.nrl.navy.mil/padamson/nepc/commits/master)
[![sphinx coverage report](https://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/sphinx.svg?job=sphinx)](http://132.250.158.124:3838/nepc/doc/)
[![pylint report](https://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/pylint.svg?job=pylint)](https://predator.nrl.navy.mil/padamson/nepc/commits/master)

The NRL Evaluated Plasma Chemistry (NEPC) project provides tools for building a 
database of evaluated electron-scattering cross-sections from various sources as well as 
tools to curate, access, visualize, and use the data. 
For more information on the goals of the project and how it is organized, please see the 
[Wiki](http://predator.nrl.navy.mil/padamson/nepc/wikis/home). The database schema and Python
module is designed 
for anyone interested in plasma chemistry with a background in physics at the graduate level.

## Getting Started

The nepc Python package works best within a conda environment (`environment.yml` file provided). Also, if you are going to build a
database yourself, you will need MySQL. To get started:

```console
$ git clone predator.nrl.navy.mil/padamson/nepc/
$ cd nepc
$ conda env create -f environment.yml #create the nepc conda environment 
$ conda activate nepc
$ pip install -e . # install the nepc package and sub-packages into the nepc conda environment
$ export NEPC_HOME=/path/to/cloned/nepc/repo/ # put this in your `~/.bashrc or ~/.bash_profile`
$ pytest # if on the NRL network (otherwise see [Wiki notes on MySQL database](https://predator.nrl.navy.mil/padamson/nepc/-/wikis/mysql))
```

## Built With

*  [Python](https://www.python.org/) 
*  [MySQL](https://www.mysql.com/)
*  [LaTeX](https://www.latex-project.org/)
*  [Jupyter Notebook](https://jupyter.org/)

