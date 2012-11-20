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
from dopplr.basequery import BaseQuery


class Paging(BaseQuery):
    """
    Query implementing search result paging. Paging is implemented `1` based,
    i.e. the first page is `1` not `0`!
    """
    def __init__(self, page, rows=10):
        self._page = page
        self._rows = rows

    def get_params(self):
        """
        Compute the `start` and `rows` parameter.
        """
        params = []
        params.append(('rows', str(self._rows)))
        if self._page > 1:
            params.append(('start', str((self._page - 1) * self._rows)))

        return params
