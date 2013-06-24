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

from dopplr.solr.query import ResultGrouping


@Vows.batch
class WhenGroupingResults(Vows.Context):

    class WithNoParametersExceptTheField(Vows.Context):

        def topic(self):
            field = "my_field"
            return ResultGrouping(field).get_params()

        def mustIncludeGroupingParameter(self, topic):
            expect(topic).to_include(('group', 'true'))

        def mustIncludeTheCorrectField(self, topic):
            expect(topic).to_include(('group.field', 'my_field'))

    class WithManyAdditionalParameters(WithNoParametersExceptTheField):

        def topic(self):
            field = "my_field"
            return ResultGrouping(field, limit=10, offset=20,
                query="field:value").get_params()

        def mustIncludeTheCorrectParameters(self, topic):
            expect(topic).to_include(('group.limit', '10'))
            expect(topic).to_include(('group.offset', '20'))
            expect(topic).to_include(('group.query', 'field:value'))
            expect(topic).to_length(5)
