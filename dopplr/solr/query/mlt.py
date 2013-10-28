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
import types

from dopplr.basequery import BaseQuery


class MoreLikeThisQuery(BaseQuery):
    """
    The `MoreLikeThisQuery` queries for similiar items. It can be used in
    addition to a `/select` query, or with a configured `MoreLikeThisHandler`.
    """

    def __init__(self, fields, mintf=None, mindf=None, minwl=None, maxwl=None,
            maxqt=None, maxntp=None, boost=False, qf=None, count=None,
            stream_body=None):
        """
        `fields` is a list of field names the mlt is based on.
        """
        if not isinstance(fields, types.ListType):
            raise TypeError('fields must be a list')
        self._fields = fields
        self._optional_params = {}
        self._optional_params['mintf'] = mintf
        self._optional_params['mindf'] = mindf
        self._optional_params['minwl'] = minwl
        self._optional_params['maxwl'] = maxwl
        self._optional_params['maxqt'] = maxqt
        self._optional_params['maxntp'] = maxntp
        self._optional_params['boost'] = boost
        self._optional_params['qf'] = qf
        self._optional_params['count'] = count
        self.stream_body = stream_body

    def get_params(self):
        """
        Return the list of query params for the mlt query.
        """
        params = []
        params.append(('mlt', 'true'))
        params.append(('mlt.fl', ','.join(self._fields)))

        for optional in self._optional_params:
            if self._optional_params[optional]:
                params.append(('mlt.%s' % optional,
                    self._optional_params[optional]))

        if self.stream_body:
            params.append(('stream.body', self.stream_body))

        return params
