
from .server_connector import ServerConnector
from .local_params import get_local_vars
import dill
import sys

def run_in_cloud(cell, connector, stack_depth=6):

    gpu_hash, gpu_ip, ws_port = connector.contact_server()

    if (gpu_hash is None or gpu_ip is None or ws_port is None):
        return

    env = get_local_vars(cell, stack_depth)

    uploads = {}
    uploads['cell'] = cell
    uploads['env'] = env

    with open('uploads.pkl', 'wb') as file:
        dill.dump(uploads, file)

    connector.upload_params_magic(gpu_ip, gpu_hash)
    outUrl = connector.stream_output(gpu_ip, gpu_hash, ws_port)

    if outUrl is None:
        return 

    result = connector.get_return_object(outUrl)
    return result
    