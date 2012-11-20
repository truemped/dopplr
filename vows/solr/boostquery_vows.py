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
from pyvows import Vows, expect

from dopplr.solr.query import BoostQuery
from dopplr.solr.query import BoostFunctionQuery


@Vows.batch
class TheSimpleBoostQuery(Vows.Context):

    def topic(self):
        return BoostQuery('test:Title').get_params()

    def shouldContainTheBqParameter(self, topic):
        expect(topic).to_include(('bq', 'test:Title'))


@Vows.batch
class TheBoostFunctionQuery(Vows.Context):

    class WithRequiredParams(Vows.Context):

        def topic(self):
            return BoostFunctionQuery('test:This').get_params()

        def shouldIncludeTheBfParameter(self, topic):
            expect(topic).to_include(('bf', 'test:This'))

    class WithAnExternalBoostingParameter(Vows.Context):

        def topic(self):
            q = BoostFunctionQuery('test:This + $date', date='123')
            return q.get_params()

        def shouldIncludeTheBfParameter(self, topic):
            expect(topic).to_include(('bf', 'test:This + $date'))

        def shouldInlcudeTheExternalParameter(self, topic):
            expect(topic).to_include(('date', '123'))

    class WithAnExternalButUnreferencedParameter(WithRequiredParams):

        def topic(self):
            q = BoostFunctionQuery('test:This', date='123')
            return q.get_params()

        def shouldNotIncludeTheExternalParam(self, topic):
            expect(topic).Not.to_include(('date', '123'))
