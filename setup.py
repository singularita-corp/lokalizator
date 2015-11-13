#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from setuptools import setup
import os.path

setup(
    name = 'lokalizator',
    version = '1',
    author = 'Magistrát hl. m. Prahy',
    description = ('CSV Geocoding Service'),
    license = 'MIT',
    keywords = 'csv geocoding',
    url = 'http://private.opendata.praha.eu/lokalizator/',
    include_package_data = True,
    package_data = {
        '': ['*.png', '*.js', '*.png', '*.html'],
    },
    packages = [
        'mhmp',
        'mhmp.lokalizator',
    ],
    classifiers = [
        'License :: OSI Approved :: MIT License',
    ],
    scripts = ['lokalizator']
)


# vim:set sw=4 ts=4 et:
