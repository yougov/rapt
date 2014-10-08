#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'click',
    'keyring',
    'vr.common',
]

setup(
    name='rapt',
    version='0.1.0',
    description='A command line tool for Velocirapter',
    long_description=readme + '\n\n' + history,
    author='Eric Larson',
    author_email='eric@ionrock.org',
    url='https://github.com/ionrock/rapt',
    packages=[
        'rapt',
    ],
    package_dir={'rapt':
                 'rapt'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='rapt',
    entry_points='''
        [console_scripts]
        rapt=rapt.rapt:rapt
    ''',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
