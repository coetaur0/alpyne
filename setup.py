from setuptools import setup


setup(
  name='alpyne',
  version=1.0,
  url='https://github.com/coetaur0/alpyne',
  license='Apache 2',
  author='Aurelien Coet',
  author_email='aurelien.coet19@gmail.com',
  description='Algebraic Petri Nets in Python3',
  packages=[
    'alpyne',
    'alpyne.adts',
  ],
  test_suite='tests',
  install_requires=[
    'graphviz'
  ]
)
