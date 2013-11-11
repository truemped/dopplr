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
import logging
import json
import urllib
import types

from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import HTTPHeaders
from tornado.ioloop import IOLoop


__all__ = ['SolrClient']


log = logging.getLogger('solr')


def try_json(response, callback):
    try:
        return json.loads(response.body)
    except TypeError:
        log.error('Error searching solr: %s' % response.body)
        callback({'error': 'no_json', 'result': response.body})


def handle_search_response(query, callback):
    """
    Closure for handling the search response.
    """
    def inner_callback(response):
        result = try_json(response, callback)
        numFound = result['response']['numFound']
        log.info('Search returned "%s" results' % numFound)
        callback(query.response_mapper(result))
    return inner_callback


def handle_suggest_response(query, callback):
    """
    Closure for handling the suggest response.
    """
    def inner_callback(response):
        result = try_json(response, callback)
        callback(query.response_mapper(result))
    return inner_callback


def default_document_verifier(doc):
    """
    By default we try to index the document.

    In `production` environments you should set the `document_verifier` via
    `Solr.__init__()` in order to minimize the traffic to solr.
    """
    return {'ok': 'true'}


def handle_indexing_response(callback=None):
    """
    Handle the solr indexing or commit response.
    The `callback` to be called with the result being either::

        {'error': 'not_indexed', 'response': httpresp}

    in case of a failure or::

        {'ok': True}

    in case of success.
    """
    def inner_callback(response):
        # since solr 4.X, we can actually json load the response; to remain
        # backwards compatible, we just add several keys to our response
        try:
            solr = json.loads(response.body)
            if "error" in solr:
                callback({'error': 'not_indexed', 'reason': solr['error'],
                    'code': solr["code"], 'response': response})
                return
        except TypeError:
            solr = response.body
            if not solr or "ERROR" in solr:
                callback({'error': 'not_indexed', 'response': response})
                return

        callback({'ok': True})

    return inner_callback


class SolrClient(object):
    """
    Apache Solr Client class.
    """

    def __init__(self, search_host, update_host=None, default_headers=None,
            required_query_params=[], client_args={}, select_path='/select',
            update_path='/update/json', mlt_path='/mlt',
            suggest_path='/suggest', document_verifier=None, ioloop=None):
        """
        Initialize me.
        """
        self._ioloop = ioloop or IOLoop.instance()

        self._search_url = '%s%s' % (search_host, select_path)
        self._mlt_url = '%s%s' % (search_host, mlt_path)
        self._termsuggest_url = '%s%s' % (search_host, suggest_path)
        uhost = update_host or search_host
        self._update_url = '%s%s' % (uhost, update_path)

        self._required_query_params = required_query_params
        if len([k for (k,v) in self._required_query_params if k=="wt"]) == 0:
            self._required_query_params.append(('wt', 'json'))

        self._document_verifier = document_verifier or \
            default_document_verifier

        self._default_headers = HTTPHeaders()
        if default_headers:
            self._default_headers.update(default_headers)
        self._client = AsyncHTTPClient(self._ioloop, **client_args)

    def _get(self, url, headers=None, callback=None):
        """
        A `GET` request to the solr.
        """
        h = HTTPHeaders()
        h.update(self._default_headers)
        if headers:
            h.update(headers)

        req = HTTPRequest(url, headers=headers)
        self._client.fetch(req, callback)

    def _post(self, url, body, headers=None, callback=None):
        """
        A `POST` request to the solr.
        """
        h = headers or HTTPHeaders()
        h.update(self._default_headers)
        if type(body) == str:
            body, h["Content-type"] = body, "application/x-www-form-urlencoded"
        else:
            body, h["Content-type"] = json.dumps(body), "application/json"
        request = HTTPRequest(url, headers=h, method="POST", body=body)
        self._client.fetch(request, callback)

    def _get_params(self, querybuilder):
        query_params = querybuilder.get_params()
        for p in self._required_query_params:
            if p not in query_params:
                query_params.append(p)

        return query_params

    def search(self, querybuilder, callback=None):
        """
        Search the Solr with `querybuilder.get_params()` as query parameters.
        Use GET by default, but switch to POST in case of very long urls.
        """
        query_params = self._get_params(querybuilder)

        log.debug('Searching solr with params: %s' % query_params)
        qs = urllib.urlencode(query_params)

        final_url = "?".join([self._search_url, qs])
        # use POST if the final url is very long
        final_url, use_post = (self._search_url, True) if len(final_url) > 2000 \
                                                    else (final_url, False)
        log.debug('Final search URL: %s' % final_url)

        if use_post:
            self._post(final_url, qs, headers=querybuilder.headers,
                callback=handle_search_response(querybuilder, callback))
        else:
            self._get(final_url, headers=querybuilder.headers,
                callback=handle_search_response(querybuilder, callback))

    def more_like_this(self, querybuilder, callback=None, match_include=True,
            match_offset=None, interestingTerms=None):
        """
        `interestingTerms` can be one of: 'list', 'details', 'none'.
        """
        query_params = self._get_params(querybuilder)

        if match_include and isinstance(match_include, types.BooleanType):
            query_params.append(('mlt.match.include', str(match_include).lower()))
        if match_offset:
            query_params.append(('mlt.match.offset', str(match_offset)))
        if interestingTerms:
            query_params.append(('mlt.interestingTerms', interestingTerms))

        log.debug('MoreLikeThis with params: %s' % query_params)
        qs = urllib.urlencode(query_params)
        final_url = '?'.join([self._mlt_url, qs])

        final_url, use_post = (self._mlt_url, True) if len(final_url) > 2000 \
                                                    else (final_url, False)
        log.debug('Final MLT URL: %s' % final_url)

        if use_post:
            self._post(final_url, qs, headers=querybuilder.headers,
                callback=handle_search_response(querybuilder, callback))
        else:
            self._get(final_url, headers=querybuilder.headers,
                callback=handle_search_response(querybuilder, callback))

    def term_suggest(self, querybuilder, callback=None):
        """
        simple query against the /term_suggest requesthandler from solr.
        """
        query_params = self._get_params(querybuilder)

        log.debug('term_suggest with params: %s' % query_params)
        qs = urllib.urlencode(query_params)
        final_url = '?'.join([self._termsuggest_url, qs])
        log.debug('Final suggest URL: %s' % final_url)

        self._get(final_url, headers=querybuilder.headers,
            callback=handle_suggest_response(querybuilder, callback))

    def index_document(self, doc, callback=None, commit=False,
                       commitWithin=None, softCommit=None, overwrite=None,
                       boost=None):
        """
        Index a `doc` into Solr. The `callback` will be called from within
        `self._handle_indexing_response`. If `commit is True`, then a `commit`
        request is sent to Solr.
        """
        verification = self._document_verifier(doc)
        if 'error' in verification:
            callback({'error': 'document refused', 'reason': verification,
                      'doc': doc})
            return

        to_index = {'add': {'doc': doc}}
        if boost:
            to_index['add']['boost'] = boost

        params = []
        if commitWithin:
            params.append(('commitWithin', str(commitWithin)))
        if overwrite is not None:
            if not overwrite:
                params.append(('overwrite', 'false'))
        if commit:
            params.append(('commit', 'true'))
        if softCommit:
            params.append(('softCommit', 'true'))
        final_url = '%s?%s' % (self._update_url, urllib.urlencode(params))

        self._post(final_url, to_index,
                callback=handle_indexing_response(callback))

    def commit(self, callback=None):
        """
        Commit any pending changes within Solr.
        """
        to_commit = {}
        final_url = "%s?commit=true" % self._update_url

        self._post(final_url, to_commit,
                callback=handle_indexing_response(callback))

    def remove_by_id(self, doc_id, callback=None, commit=False,
            commitWithin=None, softCommit=None):
        """
        Remove the document with id `doc_id`.

        If `commit=True` the change will be committed immidiately.
        The `callback` is called from within the
        `self._handle_indexing_response` method.
        """
        to_remove = {'delete': {'id': doc_id}}

        params = []
        if commitWithin:
            params.append(('commitWithin', str(commitWithin)))
        if commit:
            params.append(('commit', 'true'))
        if softCommit:
            params.append(('softCommit', 'true'))
        final_url = '%s?%s' % (self._update_url, urllib.urlencode(params))

        self._post(final_url, to_remove,
                callback=handle_indexing_response(callback))

    def remove_by_query(self, query, callback=None, commit=False,
            commitWithin=None, softCommit=None):
        """
        Remote any documents matching the given query.

        The query must be of the form `field:value`.
        """
        to_remove = {'delete': {'query': query}}

        params = []
        if commitWithin:
            params.append(('commitWithin', str(commitWithin)))
        if commit:
            params.append(('commit', 'true'))
        if softCommit:
            params.append(('softCommit', 'true'))
        final_url = '%s?%s' % (self._update_url, urllib.urlencode(params))

        self._post(final_url, to_remove,
                callback=handle_indexing_response(callback))
