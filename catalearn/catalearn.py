
import sys

from .wrapper import Wrapper
from .server_connector import ServerConnector

sys.setrecursionlimit(50000)

connector = ServerConnector('user1', 'test')
wrapper = Wrapper(connector)

def catalyse(func):
    return wrapper.wrap(func)



