from setuptools import setup
from shutil import copyfile
import os

setup(name='catalearn',
      version='0.1',
      description='A module for running machine learning code on cloud GPUs',
      url='https://github.com/Catalearn/catalearn',
      author='Edward Liu',
      author_email='edwardliu573@gmail.com',
      license='GNU LGPL',
      packages=['catalearn'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'dill',
          'requests',
          'websocket-client',
          'requests_toolbelt',
          'Ipython',
          'tqdm'
      ])

os.system("ipython profile create")
copyfile('./catalearn_magic.py', os.path.expanduser('~/.ipython/profile_default/startup/catalearn_magic.py'))