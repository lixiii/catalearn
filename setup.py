from setuptools import setup

setup(name='catalearn',
      version='0.1',
      description='A module for running machine learning code on cloud GPUs',
      url='https://github.com/Catalearn/catalearn',
      author='Edward Liu',
      author_email='edward@catalearn.com',
      license='MIT',
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