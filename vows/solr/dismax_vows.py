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
from pyvows import Vows, expect

from dopplr.solr.query.dismax import DisMax


@Vows.batch
class WithTheDisMax(Vows.Context):

    class WithDefaultParams(Vows.Context):

        def topic(self):
            q = DisMax('title^2 body^1', edismax=False)
            return q.get_params()

        def theDefTypeMustMatch(self, topic):
            expect(topic).to_include(('defType', 'dismax'))

        def theQueryFieldsMatch(self, topic):
            expect(topic).to_include(('qf', 'title^2 body^1'))

        def noUnexpectedArgs(self, topic):
            expect(topic).to_length(2)

    class WithOptionalParameters(WithDefaultParams):

        def topic(self):
            valid_params = [
                'alt',
                'mm',
                'pf',
                'ps',
                'qs',
                'tie',
                'bq',
                'bf'
            ]

            for v in valid_params:
                kwargs = {v: 'a'}
                q = DisMax('title^2 body^1', edismax=False, **kwargs)
                yield (v, q.get_params())

        def theDefTypeMustMatch(self, (field, params)):
            expect(params).to_include(('defType', 'dismax'))

        def theQueryFieldsMatch(self, (field, params)):
            expect(params).to_include(('qf', 'title^2 body^1'))

        def noUnexpectedArgs(self, (field, params)):
            expect(params).to_length(3)

        def theQueryMustMatch(self, (field, params)):
            if field == 'alt':
                field = 'q.alt'
            expect(params).to_include((field, 'a'))


@Vows.batch
class WithTheEDisMax(Vows.Context):

    class WithDefaultParams(Vows.Context):

        def topic(self):
            q = DisMax('title^2 body^1')
            return q.get_params()

        def theDefTypeMustMatch(self, topic):
            expect(topic).to_include(('defType', 'edismax'))

        def theQueryFieldsMatch(self, topic):
            expect(topic).to_include(('qf', 'title^2 body^1'))

        def noUnexpectedArgs(self, topic):
            expect(topic).to_length(2)

    class WithOptionalParameters(WithDefaultParams):

        def topic(self):
            valid_params = [
                'alt',
                'mm',
                'pf',
                'ps',
                'qs',
                'tie',
                'bq',
                'bf'
            ]

            for v in valid_params:
                kwargs = {v: 'a'}
                q = DisMax('title^2 body^1', **kwargs)
                yield (v, q.get_params())

        def theDefTypeMustMatch(self, (field, params)):
            expect(params).to_include(('defType', 'edismax'))

        def theQueryFieldsMatch(self, (field, params)):
            expect(params).to_include(('qf', 'title^2 body^1'))

        def noUnexpectedArgs(self, (field, params)):
            expect(params).to_length(3)

        def theQueryMustMatch(self, (field, params)):
            if field == 'alt':
                field = 'q.alt'
            expect(params).to_include((field, 'a'))
