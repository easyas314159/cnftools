#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:copyright: (c) 2018 by Kevin Loney
:license: MIT, see LICENSE for more details.
"""

import setuptools

VERSION = '0.0.2'

def readme():
	"""print long description"""
	with open('README.rst') as f:
		return f.read()

setuptools.setup(
    name='cnftools',
	version=VERSION,
	python_requires='>=3.4',
    author='Kevin Loney',
    author_email='kevin.loney@brainsinjars.com',
    description='A collection of tools for working with and generating Dimacs CNF files.',
	long_description=readme(),
    url='https://github.com/easyas314159/cnftools',
	license='MIT',
	keywords='dimacs cnf sat 3-cnf 3-sat 3cnf 3sat',
    packages=setuptools.find_packages(),
    classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
		'Topic :: Scientific/Engineering :: Mathematics',
    ],
	entry_points={
		'console_scripts': [
			'cnf = cnftools.cli.cnf:main',
		],
	},
	install_requires=[
		'networkx>=2.2',
	],
	include_package_data=True
)
