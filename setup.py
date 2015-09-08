# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = open('requirements.txt').read().splitlines()
long_description = open('README.md').read()

setup(
    name='ipa',
    version='0.0.1',
    description='Asynchronous RESTful API consumer using Sqlalchemy',
    long_description=long_description,
    author='Naveen Kumar Lekkalapudi',
    author_email='rekojtoor@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        ]
    )
