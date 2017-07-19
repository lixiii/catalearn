import sys

class DummyModule(object):
    def dummy():
        return None

sys.modules["gpu"] = DummyModule
sys.modules["runners"] = DummyModule
sys.modules["loggers"] = DummyModule
sys.modules["global_params"] = DummyModule