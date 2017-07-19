# Catalearn

## This module should be installed onto catalearn notebooks to provide gpu magic support

## Installation
1. First install Jupyter Notebook
2. `pip3 install git+https://github.com/yl573/catalearn`

## How it works
* user adds %%catalyse to a cell
* module finds out the variables required to run this cell by parsing the code
* uploads the variables
* computation starts in the server
* after the job is done, the new variables are downloaded and injected to the namespace