# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2012 Retresco GmbH
# Copyright (c) 2011 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
"""
The basic queries for Apache Solr. Here we implement the simple `Query` as well
as the `FilterQuery`.
"""
from dopplr.basequery import BaseQuery


class Query(BaseQuery):
    """
    The most simple Solr query: `q`.
    """

    def __init__(self, query):
        """
        Initialize the query value.
        """
        self.__query = query

    def get_params(self):
        """
        Return the list of query params.
        """
        return [('q', self.__query)]


class FilterQuery(BaseQuery):
    """
    A `FilterQuery`.
    """

    def __init__(self, query, tag=None):
        """
        Set the query value.
        """
        self.__query = query
        self.__tag = tag

    def get_params(self):
        """
        Return the list of query params.
        """
        if self.__tag:
            return [('fq', '{!tag=%s}%s' % (self.__tag, self.__query))]
        return [('fq', self.__query)]
