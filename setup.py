from distutils.core import setup

setup(name='umirr',
      version='0.5',
      description='micro mirror service',
      author='Carl George',
      author_email='carl.george@rackspace.com',
      packages=['umirr'],
      install_requires=['falcon', 'PyYAML', 'six'])
