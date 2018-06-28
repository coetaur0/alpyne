from setuptools import setup


setup(name='alpynet',
      version=1.0,
      url='https://github.com/coetaur0/alpynet',
      license='Apache 2',
      author='Aurelien Coet',
      author_email='aurelien.coet19@gmail.com',
      description='Algebraic Petri Nets in Python3',
      packages=[
        'alpynet',
        'alpynet.adts',
      ],
      test_suite='tests',
      install_requires=[
        'graphviz',
      ]
      )
