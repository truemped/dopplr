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
from pyvows import Vows, expect

from dopplr.solr.query import JoinQuery
from dopplr.solr.query import JoinFilterQuery


@Vows.batch
class WhenDoingJoins(Vows.Context):

    class WithinTheQuery(Vows.Context):

        def topic(self):
            from_field = "from_field"
            to_field = "to_field"
            query = "*:*"
            return JoinQuery(query, from_field, to_field).get_params()

        def mustIncludeJoinParameter(self, topic):
            expect(topic).to_include(('q', '{!join}*:*'))

        def mustIncludeFromParameter(self, topic):
            expect(topic).to_include(('from', 'from_field'))

        def mustIncludeToParameter(self, topic):
            expect(topic).to_include(('to', 'to_field'))

    class WithinTheFilterQuery(Vows.Context):

        def topic(self):
            from_field = "from_field"
            to_field = "to_fied"
            query = "*:*"
            return JoinFilterQuery(query, from_field, to_field).get_params()

        def mustIncludeJoinParameter(self, topic):
            expect(topic).to_include(('fq', '{!join}*:*'))
