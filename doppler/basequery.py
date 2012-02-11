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
Base class for all query implementations.

In the *Solr* context, the `BaseQuery.get_params` method must return a list of
query tuples. For a single Solr request, all lists are joined and `urlencode`
creates the Solr query string.

In the *ElasticSearch* context, the `BaseQuery.get_params` must return a
`dict`. For a single ES request, a single dict is created and the query dicts
are updated into the main dict, thus creating the ES query.
"""


class BaseQuery(object):
    """
    Base class for all query implementations.
    """

    def get_params(self):
        """
        Return the actual params for the query.
        """
        raise NotImplemented
