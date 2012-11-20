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

from dopplr.solr.query.paging import Paging


@Vows.batch
class PagingQueries(Vows.Context):

    class MustBeCalculatedCorrectly(Vows.Context):

        def topic(self):
            test_data = [
                {'rows': 10, 'page': 2, 'expected':{'rows': '10', 'start': '10'}},
                {'rows': 20, 'page': 2, 'expected':{'rows': '20', 'start': '20'}},
                {'rows': 30, 'page': 4, 'expected':{'rows': '30', 'start': '90'}},
                {'rows': 8, 'page': 4, 'expected':{'rows': '8', 'start': '24'}},
            ]
            for data in test_data:
                yield (
                    (data['expected']['rows'], data['expected']['start']),
                    Paging(data['page'], data['rows']).get_params())

        def theRowsParameterMustBeCorrect(self, ((rows, start), params)):
            expect(params).to_include(('rows', str(rows)))

        def theStartParameterMustBeCorrect(self, ((rows, start), params)):
            expect(params).to_include(('start', str(start)))
