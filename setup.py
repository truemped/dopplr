#
# Copyright (c) 2011 Retresco GmbH
#
# setup.py 01-Apr-2011
#
#
from setuptools import setup


tests_require = ['pyVows==1.1.16', 'coverage', 'tornado-pyvows>=0.5.0']


setup(
    name = "dopplr",
    version = "0.9.0-beta1",
    description = "Dopplr is a Tornado based client library for Solr and ElasticSearch",
    author = "Daniel Truemper",
    author_email = "truemped@googlemail.com",
    url = "http://truemped.github.com/dopplr",
    packages = ['dopplr', 'dopplr.solr', 'dopplr.solr.query'],
    include_package_data = True,
    install_requires = [
        'tornado>=2.1',
    ],
    tests_require = tests_require,
    extras_require = {'test': tests_require}
)
