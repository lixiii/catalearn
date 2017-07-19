from unittest import TestCase
from unittest.mock import MagicMock
from catalearn.wrapper import Wrapper
from catalearn.server_connector import ServerConnector

mock_connector = ServerConnector()
mock_connector.contact_server = MagicMock(return_value=('gpu_hash', 'gpu_ip', 'ws_port'))
mock_connector.upload_params_decorator = MagicMock()
mock_connector.upload_params_magic = MagicMock()
mock_connector.stream_output = MagicMock()
mock_connector.get_return_object = MagicMock()

class WrapperTest(TestCase):

    def test_wrap(self):

        def func():
            print('hello world')

        self.wrapper = Wrapper(mock_connector)
        wrapped_func = self.wrapper.wrap(func)
        wrapped_func()
        mock_connector.contact_server.assert_called_once_with()
