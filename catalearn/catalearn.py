
import sys
import dill
import inspect
import ast
import re
from .server_connector import ServerConnector

def format(sourceLines): # removes indentation
    head = sourceLines[0]
    while head[0] == ' ' or head[0] == '\t':
        sourceLines = [ l[1:] for l in sourceLines]
        head = sourceLines[0]
    return sourceLines

def run_on_gpu(func, local=False):

    def gpu_func(*args, **kwargs):

        serverType = 'gpu'
        if local:
            serverType = 'local'
        connector = ServerConnector('afju4x9p9q3j7s2', serverType)
        sourceLines = inspect.getsourcelines(func)[0]
        sourceLines = format(sourceLines)
        sourceLines = sourceLines[1:] # remove the decorator
        source = ''.join(sourceLines)
        data = {}
        data['source'] = source
        data['args'] = args
        data['kwargs'] = kwargs
        data['name'] = func.__name__

        dill.dump(data, open("uploads.pkl", "wb"))

        server_info = connector.contact_server()
        gpu_hash, gpu_ip, ws_port = server_info
        connector.upload_params_decorator(gpu_ip, gpu_hash)
        outUrl = connector.stream_output(gpu_ip, gpu_hash, ws_port)
        if not outUrl:
            return
        result = connector.get_return_object(outUrl)
        return result

    return gpu_func

    # data = dill.load(open("data.pkl", "rb"))
    # func = data['func']
    # args = data['args']
    # kwargs = data['kwargs']
    # env = data['env']
    # for k in env:
    #     sys._getframe(0).f_locals[k] = env[k]
    # result = func(*args, **kwargs)
    # def returnFunc(x, kw=None):
    #     pass
    # return returnFunc

    





