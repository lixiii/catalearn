
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import catalearn

@magics_class
class CatalearnMagics(Magics):

    @cell_magic
    def catalearn(self, line, cell):
        if len(line) == 0:
            print('API key missing')
            print('Please pass it in as %%catalearn <YOUR_API_KEY>')
            return

        args = line.split(' ')
        user_token = args[0]
        if len(args) == 1:
            mode = 'gpu'
        else:
            mode = args[1]

        try:
            connector = catalearn.ServerConnector(user_token, mode)
            result = catalearn.run_in_cloud(cell, connector, self.shell.user_ns)
            if result is None:
                return
            for k in result:
                self.shell.user_ns[k] = result[k]
        except Exception as e:
            print(e)

ip = get_ipython()
ip.register_magics(CatalearnMagics)