# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Retresco GmbH
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

from dopplr.solr.querybuilder import QueryBuilder
from dopplr.solr.querybuilder import TooManyQs
from dopplr.solr.query import Query
from dopplr.solr.query import FacetFieldQuery


@Vows.batch
class WhenUsingTheQueryBuilder(Vows.Context):

    class WithNoParams(Vows.Context):

        def topic(self):
            q = QueryBuilder()
            return q.get_params()

        def weGetTheExpectedDefaultParameters(self, topic):
            expect(topic).to_length(2)
            expect(topic).to_include(('q', '*:*'))
            expect(topic).to_include(('rows', '10'))

    class WithAQueryInitialization(Vows.Context):

        def topic(self):
            q = QueryBuilder(Query("field:value"))
            return q.get_params()

        def weGetTheExpectedParameters(self, topic):
            expect(topic).to_length(2)
            expect(topic).to_include(('q', 'field:value'))
            expect(topic).to_include(('rows', '10'))

    class WithAFacetFieldQueryInitialization(Vows.Context):

        def topic(self):
            q = QueryBuilder(FacetFieldQuery("field"),
                FacetFieldQuery("field2"))
            return q.get_params()

        def weGetTheExpectedParameters(self, topic):
            expect(topic).to_length(5)
            expect(topic).to_include(('q', '*:*'))
            expect(topic).to_include(('facet', 'true'))
            expect(topic).to_include(('facet.field', 'field'))
            expect(topic).to_include(('facet.field', 'field2'))
            expect(topic).to_include(('rows', '10'))

    class WithAFieldInitialization(Vows.Context):

        def topic(self):
            q = QueryBuilder(fields=["a", "b"])
            return q.get_params()

        def weGetTheExpectedParameters(self, topic):
            expect(topic).to_length(3)
            expect(topic).to_include(('q', '*:*'))
            expect(topic).to_include(('rows', '10'))
            expect(topic).to_include(('fl', 'a,b'))

    class WithASortFieldInitialization(Vows.Context):

        def topic(self):
            q = QueryBuilder(sort='field asc')
            return q.get_params()

        def weGetTheExpectedParameters(self, topic):
            expect(topic).to_length(3)
            expect(topic).to_include(('q', '*:*'))
            expect(topic).to_include(('rows', '10'))
            expect(topic).to_include(('sort', 'field asc'))

    class AndManuallyAddingParameters(Vows.Context):

        def topic(self):
            q = QueryBuilder()
            q.add_param(("field", "value"))
            q.add_params([("field2", "value2"), ("field3", "value3")])

            return q.get_params()

        def weGetTheExpectedParameters(self, topic):
            expect(topic).to_length(5)
            expect(topic).to_include(('q', '*:*'))
            expect(topic).to_include(('rows', '10'))
            expect(topic).to_include(('field', 'value'))
            expect(topic).to_include(('field2', 'value2'))
            expect(topic).to_include(('field3', 'value3'))

    class AndProducingErrors(Vows.Context):

        def topic(self):
            try:
                QueryBuilder(Query("bla"), Query("ERROR!"))
            except Exception as e:
                yield (e, TooManyQs)

            try:
                QueryBuilder("TypeError")
            except Exception as e:
                yield (e, TypeError)

        def weGetTheExpectedError(self, topic):
            error, expected_error = topic
            expect(type(error)).to_equal(expected_error)
