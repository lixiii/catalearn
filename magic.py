
from IPython.core.magic import register_cell_magic
import sys
import ast
import builtins
import dill
import os

@register_cell_magic
def gpu(line, cell):
    "my cell magic"
    print('This is my magic!')

    
    path = '/Users/yuxuanliu/Desktop/'
    save_params(cell, path)
    #send to gpu
    run_code(cell, path)
    


def save_params(source, path):

    local_vars = sys._getframe(3).f_locals
    local_vars_names = set(local_vars.keys())

    root = ast.parse(source)

    required_vars_names = set()
    for node in ast.walk(root):
        if isinstance(node, ast.Name):
            required_vars_names.add(node.id)

    builtin_vars_names = set(vars(builtins).keys())

    required_local_vars = required_vars_names & local_vars_names

    # we might want to add a compiler-ish thing in the future 

    # required_builtin_vars = required_vars_names & builtin_vars_names
    # accessible_vars = required_local_vars | required_builtin_vars

    # if accessible_vars != required_vars_names:
    #     print('missing variable')
    #     print('what we have: ' + str(accessible_vars))
    #     print('what we need: ' + str(required_vars_names))
    #     return

    params = {}
    for v in required_local_vars:
        params[v] = local_vars[v]

    with open(os.path.join(path, 'params.pkl'), 'wb') as file:
        dill.dump(params, file)

def run_code(source, path):
    with open(os.path.join(path, 'params.pkl'), 'rb') as file:
        data = dill.load(file)      
        for k in data.keys():
            sys._getframe(0).f_locals[k] = data[k]
        exec(source)

