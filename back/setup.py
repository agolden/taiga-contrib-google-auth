#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

setup(
    name = 'taiga-contrib-google-auth',
    version = ":versiontools:taiga_contrib_google_auth:",
    description = "The Taiga plugin for google authentication",
    long_description = "",
    keywords = 'taiga, google, auth, plugin',
    author = 'Alexander M Golden, Jesús Espino García',
    author_email = 'alex@agolden.com, jesus.espino@kaleidos.net',
    url = 'https://github.com/agolden/taiga-contrib-google-auth',
    license = 'AGPL',
    include_package_data = True,
    packages = find_packages(),
    install_requires=[
        'django >= 1.7',
    ],
    setup_requires = [
        'versiontools >= 1.8',
    ],
    classifiers = [
        "Programming Language :: Python",
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
