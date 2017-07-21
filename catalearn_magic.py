
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import catalearn

@magics_class
class CatalearnMagics(Magics):

    @cell_magic
    def catalyse(self, line, cell):
        if len(line) == 0:
            print('User token missing')
            print('Please pass it in as %%catalyse <YOUR_TOKEN>')
            return

        args = line.split(' ')
        user_token = args[0]
        if len(args) == 1:
            mode = 'local'
        else:
            mode = args[1]

        print(user_token, mode)

        try:
            connector = catalearn.ServerConnector(user_token, mode)
            result = catalearn.run_in_cloud(cell, connector, self.shell.user_ns)
            for k in result:
                self.shell.user_ns[k] = result[k]
        except Exception as e:
            print(e)

ip = get_ipython()
ip.register_magics(CatalearnMagics)