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
The `QueryBuilder` creating Apache Solr queries.
"""
from dopplr.basequery import BaseQuery
from dopplr.solr.query import Query


class TooManyQs(Exception):
    """
    Exception raised when you try to add more than one `Query` to a single
    `QueryBuilder` instance.
    """
    pass


class QueryBuilder(object):
    """
    The Solr query builder.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize me.

        The `*args` parameter allows you to write queries like this::

            QueryBuilder(Query('*:*'), FilterQuery('field:TEST'),
                callback=callback)

        The `response_mapper` will be called with the complete `Solr` response
        so you may map it into some internal format. If not given, the solr
        response will be passed to the `callback`.
        """
        self.__has_q = False

        self.__queries = []
        for q in args:
            self.add(q)

        self.__params = []
        if len(kwargs.get('fields', [])) > 0:
            self.__params.append(('fl', ','.join(kwargs.get('fields'))))
        if kwargs.get('sort', None):
            self.__params.append(('sort', kwargs.get('sort')))

        self.__rows = kwargs.get('rows', 10)

        self.response_mapper = kwargs.get('response_mapper', lambda x: x)
        self.headers = kwargs.get('headers', None)

    def add_param(self, param):
        """
        Directly add a parameter to the `QueryBuilder`. This is intended for
        stuff like `dismax` parametrization etc.

        `param` needs to be a tuple of the form::
            (name, value)
        """
        self.__params.append(param)

    def add_params(self, params):
        """
        Directly add a parameter list to the `QueryBuilder`. This is intended
        for stuff like `dismax` parametrization etc.

        `params` needs to be a list of tuples of the form::
            (name, value)
        """
        self.__params.extend(params)

    def add(self, query):
        """
        Add a query objet to the `QueryBuilder`.
        """
        if not isinstance(query, BaseQuery):
            raise TypeError
        if isinstance(query, Query):
            if self.__has_q:
                raise TooManyQs
            self.__has_q = True
        self.__queries.append(query)

    def get_params(self):
        """
        Compute and return a list of all query values.
        """
        queries = []
        queries.extend(self.__params)
        if not self.__has_q:
            queries.append(('q', '*:*'))
        has_facet_on = False
        has_rows = False
        for q in self.__queries:
            for name, value in q.get_params():
                if name == 'facet':
                    if not has_facet_on:
                        has_facet_on = True
                    else:
                        continue
                if name == 'rows':
                    has_rows = True
                queries.append((name, value))

        if not has_rows:
            queries.append(('rows', str(self.__rows)))
        return queries
