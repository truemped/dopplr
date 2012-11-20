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
A collection of sample response mappers.
"""


def map_to_docs(solr_response):
    """
    Response mapper that only returns the list of result documents.
    """
    return solr_response['response']['docs']


def _flatten_to_dict(list_of_facets):
    """
    Simple helper that flattens the solr facet into a dict.
    """
    facet = {'sort': []}
    for i in range(0, len(list_of_facets), 2):
        facet['sort'].append(list_of_facets[i])
        facet[list_of_facets[i]] = list_of_facets[i+1]

    return facet


def detailed_response_mapper(solr_response):
    """
    Response mapper that also extracts the returned facets into a dict. In
    order to keep the sort order, a separate list contains the keys for the
    facet dictionary in sorted order.
    """
    result = {
        'docs': [],
        'numFound': 0
    }

    if 'response' in solr_response:
        result['numFound'] = solr_response['response']['numFound']
        result['docs'] = solr_response['response']['docs']

    if 'facet_counts' in solr_response:

        result['facet'] = {}
        facets = solr_response['facet_counts']

        if 'facet_fields' in facets:
            result['facet']['field'] = rf = {}
            for field in facets['facet_fields']:
                rf[field] = _flatten_to_dict(facets['facet_fields'][field])

        if 'facet_queries' in facets:
            result['facet']['query'] = rq = {}
            for query in facets['facet_queries']:
                rq[query] = _flatten_to_dict(facets['facet_queries'][query])

        if 'facet_ranges' in facets:
            result['facet']['range'] = rr = {}
            for frange in facets['facet_ranges']:
                rr[frange] = \
                    _flatten_to_dict(facets['facet_ranges'][frange]['counts'])
                rr[frange]['start'] = facets['facet_ranges'][frange]['start']
                rr[frange]['end'] = facets['facet_ranges'][frange]['end']
                rr[frange]['gap'] = facets['facet_ranges'][frange]['gap']

    return result
