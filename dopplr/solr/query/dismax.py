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
The Solr (e)DisMax query.

For more information see: http://wiki.apache.org/solr/DisMaxQParserPlugin
"""
from dopplr.basequery import BaseQuery


class DisMax(BaseQuery):
    """
    The dismax query.
    """

    def __init__(self, qf, alt=None, mm=None, pf=None, ps=None, qs=None,
            tie=None, bq=None, bf=None, edismax=True):
        """
        Initialize the query values.
        """
        self.__qf = qf
        if edismax:
            self.__deftype = 'edismax'
        else:
            self.__deftype = 'dismax'
        self.__optional_params = {
            'q.alt': alt,
            'mm': mm,
            'pf': pf,
            'ps': ps,
            'qs': qs,
            'tie': tie,
            'bq': bq,
            'bf': bf
        }

    def get_params(self):
        """
        Return the list of query params.
        """
        params = []
        params.append(('defType', self.__deftype))
        params.append(('qf', self.__qf))

        for p in self.__optional_params:
            if self.__optional_params[p]:
                params.append((p, self.__optional_params[p]))

        return params
