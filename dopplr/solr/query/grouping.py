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
Solr Result Grouping Query
some parameters are only available since Solr 4.X
"""
from dopplr.basequery import BaseQuery


class ResultGrouping(BaseQuery):
    """
    Enable result grouping for a Solr query
    """

    def __init__(self, field, func=None, query=None, limit=None, offset=None,
        sort=None, format=None, main=None, ngroups=None, truncate=None,
        facet=None, cache_percent=None):
        self._params = []
        local_vars = locals()
        # the Solr parameter syntax is always the same: prepend "group." to the
        # variable name if it is set and add it to the parameter list
        for name in filter(lambda x: x != 'self' and local_vars[x] is not None,
            local_vars):
            self._params.append(('group.' + name.replace("_", "."),
                str(local_vars[name])))

    def get_params(self):
        """
        Return the list of query params for `ResultGrouping`.
        """
        return [('group', 'true')] + self._params
