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

from dopplr.solr.query.query import Query
from dopplr.solr.query.query import FilterQuery


@Vows.batch
class SimpleQueries(Vows.Context):

    def topic(self):
        return Query('content:(foo OR bar)').get_params()

    def mustMatch(self, topic):
        expect(topic).to_include(('q', 'content:(foo OR bar)'))

    def mustHaveNoOtherQueries(self, topic):
        expect(topic).to_length(1)


@Vows.batch
class SimpleFilterQueries(Vows.Context):

    class MustBeSimple(Vows.Context):

        def topic(self):
            return FilterQuery('category:Test').get_params()

        def mustMatch(self, topic):
            expect(topic).to_include(('fq', 'category:Test'))

        def mustHaveNoOtherQueries(self, topic):
            expect(topic).to_length(1)

    class CanBeTagged(MustBeSimple):

        def topic(self):
            return FilterQuery('category:Test', tag='test').get_params()

        def mustMatch(self, topic):
            expect(topic).to_include(('fq', '{!tag=test}category:Test'))
