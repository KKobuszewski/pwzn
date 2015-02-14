from distutils.core import setup
from Cython.Build import cythonize

__author__ = 'karolina'


setup(
    name='qsort',
    version='0.0.1',
    ext_modules=cythonize("qsort.pyx"),
    license='',
    author='Konrad Kobuszewski & Karolina Kulesz',
    author_email='konrad.kobuszewski93@gmail.com',
    description='Example of quicksort algorithm implementation in cython',
    classifiers=
    """
        Development Status :: 1 - Beta
        Intended Audience :: Developers
        License :: OSI Approved :: Apache Software License
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3.4
    """.strip().split('\n')
)
