# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Daniel Truemper <truemped at googlemail.com>
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
Solr Join (Filter) Query
only available since Solr 4.X
"""
from dopplr.basequery import BaseQuery


class JoinBaseQuery(BaseQuery):
    """
    A base query for all join operations.
    """

    def __init__(self, query, from_field, to_field):
        """
        Join base query takes care of joining syntax
        """
        self._query = '{!join}' + query
        self._from = from_field
        self._to = to_field

    def get_params(self):
        """
        Return the list of query params for the `JoinBaseQuery`.
        """
        params = []
        params.append(('from', self._from))
        params.append(('to', self._to))

        return params


class JoinQuery(JoinBaseQuery):
    """
    A join query.
    """

    def __init__(self, query, from_field, to_field):
        super(JoinQuery, self).__init__(query, from_field, to_field)

    def get_params(self):
        """
        Return the list of query params for the `JoinQuery`.
        """
        params = super(JoinQuery, self).get_params()
        params.append(('q', self._query))

        return params


class JoinFilterQuery(JoinBaseQuery):
    """
    A join filter query.
    """

    def __init__(self, query, from_field, to_field):
        super(JoinFilterQuery, self).__init__(query, from_field, to_field)

    def get_params(self):
        """
        Return the list of query params for the `JoinFilterQuery`.
        """
        params = super(JoinFilterQuery, self).get_params()
        params.append(('fq', self._query))

        return params
