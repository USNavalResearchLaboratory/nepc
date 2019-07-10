# NEPC

[![pipeline status](http://predator.nrl.navy.mil/padamson/nepc/badges/master/pipeline.svg)](http://predator.nrl.navy.mil/padamson/nepc/commits/master)
[![coverage report](http://predator.nrl.navy.mil/padamson/nepc/badges/master/coverage.svg)](http://predator.nrl.navy.mil/padamson/nepc/commits/master)
[![pylint report](http://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/public/pylint.svg?job=pylint)](http://predator.nrl.navy.mil/padamson/nepc/commits/master)
[![docstr-coverage report](http://predator.nrl.navy.mil/padamson/nepc/-/jobs/artifacts/master/raw/public/docstr-coverage.svg?job=sphinx)](http://predator.nrl.navy.mil/padamson/nepc/commits/master)

NEPC, standing for NRL Evaluated Plasma Chemistry, is a project involving the building of a 
database of evaluated electron-scattering cross-sections from various sources as well as 
tools to access and visualize the data. Data can be accessed, raw and formatted, through the 
"data" directory, while other directories of the project are used for builing and accessing 
the database. For more information on how the project is organized, please see the 
[Wiki](http://predator.nrl.navy.mil/padamson/nepc/wikis/home). This database is designed 
for anyone interested in plasma chemistry with a background in physics at the graduate level.

## Getting Started

In order to be able to use nepc, make sure that you have Anaconda downloaded, and that conda is included. Additionally, make sure that you have Ubuntu downloaded and working.

*  Clone nepc using the git command `git clone "predator.nrl.navy.mil/padamson/nepc/"`
*  Next, use the command `conda env create -f environment.yml` to create the development environment based on the files included - which is for the sake of version control.
*  Activate the environment just created with `conda activate nepc`. You'll have to do this everytime you use nepc.
*  Now you'll have to download the nepc package inside nepc, using this command: `pip install -e .`
*  To check to see if it works feel free to use the command `pytest` to verify if all of the tests have passed.

## Built With

*  [Python](https://www.python.org/) 
*  [Jupyter Notebook](https://jupyter.org/)
*  [LaTeX](https://www.latex-project.org/)
*  [MySQL](https://www.mysql.com/)
