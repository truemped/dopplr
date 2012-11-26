#
# Copyright (c) 2011 Retresco GmbH
#
# setup.py 01-Apr-2011
#
#
from setuptools import setup, find_packages


tests_require = ['coverage', 'tornado-pyvows>=0.5.0']


setup(
    name = "dopplr",
    version = "0.8.3",
    description = "Dopplr is a Tornado based client library for Solr and ElasticSearch",
    author = "Daniel Truemper",
    author_email = "truemped@googlemail.com",
    url = "http://truemped.github.com/dopplr",
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'tornado>=2.1',
    ],
    tests_require = tests_require,
    extras_require = {'test': tests_require}
)
