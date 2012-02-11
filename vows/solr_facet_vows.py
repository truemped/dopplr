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

from doppler.solr.query.facets import FacetQuery
from doppler.solr.query.facets import MultiselectFacetQuery
from doppler.solr.query.facets import RangeFacetQuery


@Vows.batch
class FacettingQueries(Vows.Context):

    class WithASimpleFacet(Vows.Context):

        def topic(self):
            q = FacetQuery('foo')
            return q.get_params()

        def FacetOnMustBePresent(self, topic):
            expect(topic).to_include(('facet', 'on'))

        def FacetFieldMustBeCorrect(self, topic):
            expect(topic).to_include(('facet.field', 'foo'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(2)

    class WithAMinCountParameter(WithASimpleFacet):

        def topic(self):
            q = FacetQuery('foo', mincount=1)
            return q.get_params()

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(3)

        def FacetMincountMustBeCorrect(self, topic):
            expect(topic).to_include(('f.foo.facet.mincount', '1'))

    class WithAFacetValue(WithASimpleFacet):

        def topic(self):
            q = FacetQuery('foo', value='bar')
            return q.get_params()

        def theFilterQueryMustBeCreated(self, topic):
            expect(topic).to_include(('fq', '{!tag=foo}foo:bar'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(3)

    class WithAFacetValueAndWithoutATag(WithASimpleFacet):

        def topic(self):
            q = FacetQuery('foo', value='bar', tag=False)
            return q.get_params()

        def theFilterQueryMustBeCreated(self, topic):
            expect(topic).to_include(('fq', 'foo:bar'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(3)

    class WithASortParameter(WithAFacetValue):

        def topic(self):
            q = FacetQuery('foo', value='bar', sort='count')
            return q.get_params()

        def theFacetsShouldBeSortedByCount(self, topic):
            expect(topic).to_include(('f.foo.facet.sort', 'count'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(4)

    class WithMissingParams(WithAFacetValue):

        def topic(self):
            q = FacetQuery('foo', value='bar', sort='count', missing=1)
            return q.get_params()

        def theFacetsShouldBeSortedByCount(self, topic):
            expect(topic).to_include(('f.foo.facet.missing', '1'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(5)


@Vows.batch
class MultiSelectFacettingQueries(Vows.Context):

    class WithASimpleFacet(Vows.Context):

        def topic(self):
            q = MultiselectFacetQuery('foo')
            return q.get_params()

        def facetOnMustBePresent(self, topic):
            expect(topic).to_include(('facet', 'on'))

        def facetFieldMustBeCorrect(self, topic):
            expect(topic).to_include(('facet.field', 'foo'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(2)

    class WithAMinCountParameter(WithASimpleFacet):

        def topic(self):
            q = MultiselectFacetQuery('foo', mincount=1)
            return q.get_params()

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(3)

        def FacetMincountMustBeCorrect(self, topic):
            expect(topic).to_include(('f.foo.facet.mincount', '1'))

    class WithAFacetValue(WithASimpleFacet):

        def topic(self):
            q = MultiselectFacetQuery('foo', value='bar')
            return q.get_params()

        def facetFieldMustBeCorrect(self, topic):
            expect(topic).to_include(('facet.field', '{!ex=foo}foo'))

        def theFilterQueryMustBeCreated(self, topic):
            expect(topic).to_include(('fq', '{!tag=foo}foo:bar'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(3)

    class WithAFacetValueAndWithoutATag(WithAFacetValue):

        def topic(self):
            q = MultiselectFacetQuery('foo', value='bar', tag=False)
            return q.get_params()

        def theFilterQueryMustBeCreated(self, topic):
            expect(topic).Not.to_include(('fq', 'foo:bar'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(3)

    class WithASortParameter(WithAFacetValue):

        def topic(self):
            q = MultiselectFacetQuery('foo', value='bar', sort='count')
            return q.get_params()

        def theFacetsShouldBeSortedByCount(self, topic):
            expect(topic).to_include(('f.foo.facet.sort', 'count'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(4)

    class WithMissingParams(WithAFacetValue):

        def topic(self):
            q = MultiselectFacetQuery('foo', value='bar', sort='count',
                missing=1)
            return q.get_params()

        def theFacetsShouldBeSortedByCount(self, topic):
            expect(topic).to_include(('f.foo.facet.missing', '1'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(5)

    class WithAdditionalExcludes(WithAFacetValue):

        def topic(self):
            q = MultiselectFacetQuery('foo', value='bar',
                additional_excludes=['test'])
            return q.get_params()

        def facetFieldMustBeCorrect(self, topic):
            expect(topic).to_include(('facet.field', '{!ex=test,foo}foo'))


@Vows.batch
class ARangeFacetQuery(Vows.Context):

    class WithRequiredParams(Vows.Context):

        def topic(self):
            return RangeFacetQuery('foo', 1, 2, 10).get_params()

        def facetOnMustBePresent(self, topic):
            expect(topic).to_include(('facet', 'on'))

        def facetFieldMustBeCorrect(self, topic):
            expect(topic).to_include(('facet.range', 'foo'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(5)

        def theStartParameterEquals(self, topic):
            expect(topic).to_include(('f.foo.facet.range.start', '1'))

        def theGapParameterEquals(self, topic):
            expect(topic).to_include(('f.foo.facet.range.gap', '2'))

        def theEndParameterEquals(self, topic):
            expect(topic).to_include(('f.foo.facet.range.end', '10'))

    class WithAValue(WithRequiredParams):

        def topic(self):
            return RangeFacetQuery('foo', 1, 2, 10, value=5).get_params()

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(6)

        def theFqMustEqual(self, topic):
            expect(topic).to_include(('fq', '{!tag=foo}foo:5'))

    class WithAValueAndWithoutATag(WithAValue):

        def topic(self):
            q = RangeFacetQuery('foo', 1, 2, 10, value=5, tag=False)
            return q.get_params()

        def theFqMustEqual(self, topic):
            expect(topic).to_include(('fq', 'foo:5'))

    class WithAHardenedParam(WithRequiredParams):

        def topic(self):
            return RangeFacetQuery('foo', 1, 2, 10, hardened=True).get_params()

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(6)

        def theHardenedParamMatches(self, topic):
            expect(topic).to_include(('f.foo.facet.range.hardened', True))

    class WithAOtherParameter(WithRequiredParams):

        def topic(self):
            return RangeFacetQuery('foo', 1, 2, 10, other='after').get_params()

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(6)

        def theOtherParamMatches(self, topic):
            expect(topic).to_include(('f.foo.facet.range.other', 'after'))

    class WithAnIncludeParameter(WithRequiredParams):

        def topic(self):
            q = RangeFacetQuery('foo', 1, 2, 10, include='all')
            return q.get_params()

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(6)

        def theOtherParamMatches(self, topic):
            expect(topic).to_include(('f.foo.facet.range.include', 'all'))
