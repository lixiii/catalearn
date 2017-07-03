from setuptools import setup

setup(name='catalearn',
      version='0.1',
      description='A module for running machine learning code on cloud GPUs',
      url='https://github.com/Catalearn/catalearn',
      author='Edward Liu',
      author_email='edwardliu573@gmail.com',
      license='GNU LGPL',
      packages=['catalearn'],
      zip_safe=False,
      install_requires=[
          'dill',
          'requests',
          'websocket-client'
      ])