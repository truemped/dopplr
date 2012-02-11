#
# Copyright (c) 2011 Retresco GmbH
#
# setup.py 01-Apr-2011
#
#
from setuptools import setup, find_packages


tests_require = ['tornado-pyvows>=0.3.1']


setup(
    name = "doppler",
    version = "0.1.0",
    description = "Doppler is a Tornado based client library for Solr and ElasticSearch",
    author = "Daniel Truemper",
    author_email = "truemper@retresco.de",
    url = "http://retresco.github.com/doppler",
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'tornado',
    ],
    tests_require = tests_require,
    extras_require = {'test': tests_require}
)
