# vim: set fileencoding=utf-8 :
#
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
from dopplr.basequery import BaseQuery


class Spellcheck(BaseQuery):
    """
    `Did you mean`?

    See: http://wiki.apache.org/solr/SpellCheckComponent
    """

    def __init__(self, count=None, collate=True, onlyMorePopular=True,
            dictionary=None):
        """
        Initialize the query value.
        """
        self.__count = count
        self.__collate = collate
        self.__onlyMorePopular = onlyMorePopular
        self.__dictionary = dictionary

    def get_params(self):
        """
        Return the list of query params.
        """
        params = []
        params.append(('spellcheck', 'true'))

        if self.__count:
            params.append(('spellcheck.count', str(self.__count)))

        if self.__collate:
            params.append(('spellcheck.collate', 'true'))
        else:
            params.append(('spellcheck.collate', 'false'))

        if self.__onlyMorePopular:
            params.append(('spellcheck.onlyMorePopular', 'true'))
        else:
            params.append(('spellcheck.onlyMorePopular', 'false'))

        if self.__dictionary:
            params.append(('spellcheck.dictionary', self.__dictionary))

        return params
