
from IPython.core.magic import Magics, magics_class, cell_magic
import catalearn

@magics_class
class CatalearnMagics(Magics):

    @cell_magic
    def catalyse(self, line, cell):
        try:
            connector = catalearn.ServerConnector('user1', 'local')
            result = catalearn.run_in_cloud(cell, connector)
            for k in result:
                self.shell.user_ns[k] = result[k]
        except Exception as e:
            print(e)

ip = get_ipython()
ip.register_magics(CatalearnMagics)