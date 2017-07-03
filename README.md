# Catalearn
### A module for running machine learning code in cloud GPUs#

## Installation
`pip install git+https://github.com/Catalearn/catalearn`

## Usage
Example:
````
import catalearn

name = 'Tom'

def func(name):
    print('hello' + name)
    
    # run machine learning code here

catalearn.run_on_gpu(func, name)