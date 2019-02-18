from setuptools import setup

setup(
    name='nbpyhelp',
    version='0.1',
    description='A collection of helper functions for python',
    long_description='A collection of helper functions for python. The package mosly focuses on functions for bioinformatics analysis',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='helpers bioinformatics',
    url='http://github.com/nbhelpers/nbpyhelp',
    author='Nick Barkas',
    author_email='me@nikolasbarkas.com',
    license='MIT',
    packages=['nbpyhelp'],
    install_requires=[
        'pysam',
        'click',
    ],
    entry_points='''
        [console_scripts]
        nbpyhelp=nbpyhelp:cli
    ''',
    zip_safe=False
)

      
      
