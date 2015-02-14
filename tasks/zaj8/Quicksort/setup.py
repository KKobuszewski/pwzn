from Cython.Build import cythonize

__author__ = 'karolina'



setup(
    name='qsort',
    version='0.0.1',
    ext_modules=cythonize("qsort.pyx"),
    license='Apache 2.0',
    author='Jacek Bzdak',
    author_email='jbzdak@gmail.com',
    description='Cython example of module generating Fibbonaci numbers',
    classifiers="""
        Development Status :: 1 - Beta
        Intended Audience :: Developers
        License :: OSI Approved :: Apache Software License
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3.4
    """.strip().split('\n')
)
