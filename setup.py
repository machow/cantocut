#!/usr/bin/env python

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('cantocut.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
	name = 'cantocut',
	version = version,
	py_modules= ['cantocut'],
	install_requires = ['astar'],
        description = 'word segmentation for cantonese',
        author = 'Michael Chow',
        author_email = 'mc_al_cantocut@fastmail.com',
        url = 'https://github.com/machow/cantocut',
        include_package_data = True)

