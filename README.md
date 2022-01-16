# NEPC

![workflow status](https://github.com/USNavalResearchLaboratory/nepc/actions/workflows/main.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/nepc/badge/?version=latest)](https://nepc.readthedocs.io/en/latest/?badge=latest)
![GitHub](https://img.shields.io/github/license/USNavalResearchLaboratory/nepc)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3974315.svg)](https://doi.org/10.5281/zenodo.3974315)

The goals of the nepc project are to provide tools to:

1. parse, evaluate, and populate metadata for electron scattering cross sections;
2. build a NEPC MySQL database of cross sections;
2. curate, access, visualize, and use cross section data from a NEPC database; and
4. support verification and validation of electron scattering cross section data.

The database schema and Python module are designed 
for anyone interested in plasma chemistry with a background in physics at the graduate level.

Documentation for the nepc project: [https://nepc.readthedocs.io](https://nepc.readthedocs.io).

## Organization

The project is organized in the following directories:

* tests - unit and integration testing
* tests/data - data directory for the `nepc_test` database--an example NEPC database containing fictitious electron scattering cross section data used in unit and integration testing
* tests/data/eda - example exploratory data analysis (EDA) of a NEPC database that is possible with the nepc Python module
* tests/data/curate - code used to curate fictitious cross section data in [LXCat](https://nl.lxcat.net/data/set_type.php) format and create various NEPC `Model`s for the `nepc_test` database
* docs - files used by Sphinx to generate the [NEPC documentation](https://nepc.readthedocs.io)
* nepc - the Python code for the nepc package and building a NEPC database
* nepc/mysql - the Python code for creating a NEPC database from data in `NEPC_CS_HOME` environment variable; also creates the `nepc_test` database from data in `NEPC_HOME/tests/data` (must have the `NEPC_HOME` environment variable set)

## Getting Started

To install `nepc` with pip, run:

```shell
$ pip install nepc
```

Establish a connection to the database named `nepc` running on a
production server (you must set an environment variable `NEPC_PRODUCTION` that
points to the production server):

```python
>>> cnx, cursor = nepc.connect()
```

If you've built the `nepc_test` database on your local machine 
(see instructions [here](https://nepc.readthedocs.io/en/latest/mysql.html)), establish a connection to it:

```python
>>> cnx, cursor = nepc.connect(local=True, test=True)
```

Access the pre-defined plasma chemistry model, `fict_min2`, in the `nepc_test` database:

```python
>>> fict_min2 = nepc.Model(cursor, "fict_min2")
```

Print a summary of the ``fict_min2`` model, including a stylized Pandas dataframe:

```python
>>> fict_min2.summary()
```

Plot the cross sections in `fict_min2`.

```python
>>> fict_min2.plot(ylog=True, xlog=True, width=8, height=4) 
```

Additional examples of EDA using nepc are in `tests/data/eda`. Examples of scripts for
curating raw data for the `nepc_test` database, including parsing
[LXCat](https://nl.lxcat.net/data/set_type.php) formatted data,
are in `tests/data/curate`.

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


***Approved for public release, distribution is unlimited.***
