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
Facet queries for Apache Solr.

See http://wiki.apache.org/solr/SimpleFacetParameters for details.
"""
from dopplr.basequery import BaseQuery
from dopplr.solr.query.query import FilterQuery


class FacetFieldQuery(BaseQuery):
    """
    The simple `FacetQuery` for facetting a field.
    """

    def __init__(self, field, prefix=None, sort=None, limit=None, offset=None,
            mincount=None, missing=None, method=None, minDf=None, value=None,
            tag=True):
        """
        Set the field for which the facet should get created.

        If the `value` is given the appropriate `FilterQuery` is automatically
        appended.
        """
        self.__field = field
        self.__value = value
        self.__tag = tag

        self.__optional_params = {
            'prefix': prefix,
            'sort': sort,
            'limit': limit,
            'offset': offset,
            'mincount': mincount,
            'missing': missing,
            'method': method,
            'enum.cache.minDf': minDf
        }

    def get_params(self):
        """
        Return the list of query params.
        """
        params = []
        params.append(('facet', 'true'))
        params.append(('facet.field', self.__field))

        for p in self.__optional_params:
            if self.__optional_params[p]:
                params.append(('f.%s.facet.%s' % (self.__field, p),
                    str(self.__optional_params[p])))

        if self.__value:
            if self.__tag:
                params.extend(FilterQuery(
                    '%s:%s' % (self.__field, self.__value),
                    tag=self.__field).get_params())
            else:
                params.extend(FilterQuery(
                    '%s:%s' % (self.__field, self.__value)).get_params())

        return params


class MultiselectFacetQuery(FacetFieldQuery):
    """
    Use the `MultiselectFacetQuery` if you want the facet field to be
    calculated even though there is a `FilterQuery` on this field.
    """

    def __init__(self, field, additional_excludes=[], **kwargs):
        """
        Initialize the multiselect facet.
        """
        kwargs['tag'] = True
        super(MultiselectFacetQuery, self).__init__(field, **kwargs)

        self.__field = field
        self.__value = kwargs.get('value')
        self.__additional_excludes = additional_excludes

    def get_params(self):
        """
        Return the list of query params for the multiselect facet.
        """
        params = super(MultiselectFacetQuery, self).get_params()

        ignores = self.__additional_excludes[:]
        if self.__value:
            # remove the field definition and replace it
            params = filter(lambda (n,v): n!='facet.field', params)
            ignores.append(self.__field)
            params.append(('facet.field', '{!ex=%s}%s' % (','.join(ignores),
                self.__field)))

        return params


class RangeFacetQuery(BaseQuery):
    """
    A range facet query.

    See: http://wiki.apache.org/solr/SimpleFacetParameters#Facet_by_Range
    """

    def __init__(self, field, start, gap, end, hardened=None, other=None,
            include=None, value=None, tag=True):
        """
        Set range facet parameters for this query.
        """
        self.__field = field
        self.__start = start
        self.__gap = gap
        self.__end = end
        self.__value = value
        self.__tag = tag

        self.__optional_params = {
            'hardened': hardened,
            'other': other,
            'include': include
        }

    def get_params(self):
        """
        Compute the parameters for the `RangeFacetQuery`.
        """
        params = []
        params.append(('facet', 'true'))
        params.append(('facet.range', self.__field))

        params.append(('f.%s.facet.range.start' % self.__field,
            str(self.__start)))
        params.append(('f.%s.facet.range.gap' % self.__field, str(self.__gap)))
        params.append(('f.%s.facet.range.end' % self.__field, str(self.__end)))

        for p in self.__optional_params:
            if self.__optional_params[p]:
                params.append(('f.%s.facet.range.%s' % (self.__field, p),
                    self.__optional_params[p]))

        if self.__value:
            if self.__tag:
                params.extend(FilterQuery(
                    '%s:%s' % (self.__field, self.__value),
                    tag=self.__field).get_params())
            else:
                params.extend(FilterQuery(
                    '%s:%s' % (self.__field, self.__value)).get_params())

        return params


class FacetQueryQuery(BaseQuery):
    """
    Query for facetting through a query
    """

    def __init__(self, query, excludeFqs=[]):

        self.__query = query
        self.__excludeFqs = excludeFqs

    def get_params(self):

        params = []
        params.append(('facet', 'true'))
        query = self.__query
        if len(self.__excludeFqs) > 0:
            query = '{!ex=%s}%s' % (','.join(self.__excludeFqs), self.__query)
        params.append(('facet.query', query))

        return params
