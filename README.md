# NEPC

<!--[![pipeline status](http://predator.nrl.navy.mil/padamson/nepc/badges/master/pipeline.svg)](http://predator.nrl.navy.mil/padamson/nepc/commits/master)
-->
[![pytest coverage report](https://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/pytest.svg?job=pytest)](https://predator.nrl.navy.mil/padamson/nepc/commits/master)
[![sphinx coverage report](https://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/sphinx.svg?job=sphinx)](http://132.250.158.124:3838/nepc/doc/)
[![pylint report](https://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/pylint.svg?job=pylint)](https://predator.nrl.navy.mil/padamson/nepc/commits/master)

The goals of the nepc project are to provide tools to:

1. parse, evaluate, and populate metadata for electron scattering cross sections;
2. build a [NEPC MySQL database](mysql) of cross sections;
2. curate, access, visualize, and use cross section data from a NEPC database; and
4. support [verification and validation](vandv) of electron scattering cross section data.

The database schema and Python module are designed 
for anyone interested in plasma chemistry with a background in physics at the graduate level.

Documentation for the nepc project: [click here](http://132.250.158.124:3838/nepc/doc/).

## Organization

The project is organized in the following directories:

* tests - unit and integration testing
* tests/data - data directory for the `nepc_test` database--an example NEPC database containing fictitious electron scattering cross section data used in unit and integration testing
* tests/data/eda - example exploratory data analysis (EDA) of a NEPC database that is possible with the nepc Python module
* tests/data/methods - code used to parse fictitious cross section data in [LXCat](https://nl.lxcat.net/data/set_type.php) format and create various NEPC `Model`s for the `nepc_test` database
* docs - files used by Sphinx to generate the [NEPC documentation](http://132.250.158.124:3838/nepc/doc/)
* nepc - the Python code for the nepc package and building a NEPC database
* nepc/mysql - the Python code for creating a NEPC database from data in `$NEPC_DATA_HOME`; also creates the `nepc_test` database from data in `$NEPC_HOME/tests/data`

## Getting Started

The nepc Python package works best within a conda environment (`environment.yml` file provided). 
Also, if you are going to build a database yourself, you will need MySQL. To get started:

```console
$ git clone predator.nrl.navy.mil/padamson/nepc/
$ cd nepc
$ conda env create -f environment.yml #create the nepc conda environment 
$ conda activate nepc
$ pip install -e . # install the nepc package and sub-packages into the nepc conda environment
$ export NEPC_HOME=/path/to/cloned/nepc/repo/ # put this in your `~/.bashrc or ~/.bash_profile`
$ pytest # if on the NRL network (otherwise see the [notes on MySQL](MYSQL.md))
```

## Built With

*  [Python](https://www.python.org/) 
*  [MySQL](https://www.mysql.com/)
*  [LaTeX](https://www.latex-project.org/)
*  [Jupyter Notebook](https://jupyter.org/)

## Pronunciation

NEPC rhymes with the loser of the [Cola War](https://en.wikipedia.org/wiki/Cola_wars).
If NEPC were in the
[CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict),
its entry would be `N EH P S IY .`.

