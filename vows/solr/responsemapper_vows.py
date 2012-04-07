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
import os.path
import json

from pyvows import Vows, expect

from doppler.solr.responsemapper import detailed_response_mapper


with open(os.path.join(os.path.dirname(__file__), 'sampleresult.json')) as f:
    SAMPLE_RESULT = json.loads(f.read())


@Vows.batch
class TheDetailedResponseMapper(Vows.Context):

    def topic(self):
        return (SAMPLE_RESULT, detailed_response_mapper(SAMPLE_RESULT))

    def shouldReturnTheListOfDocuments(self, (solr, result)):
        expect(result['docs']).to_equal(solr['response']['docs'])

    class shouldContainTheFieldFacet(Vows.Context):

        def topic(self, (solr, result)):
            for field in result['facet']['field']:
                yield (solr, result['facet']['field'][field])

        def andTheFacetMustBeADict(self, (_, facet)):
            expect(isinstance(facet, dict)).to_be_true()

        def andTheFacetDictContainsTheSortOrder(self, (_, facet)):
            expect(facet).to_include('sort')

        def andTheFacetSortMustNotBeEmpty(self, (_, facet)):
            expect(facet['sort']).Not.to_be_empty()

    class shouldContaineTheRangeFacet(shouldContainTheFieldFacet):

        def topic(self, (solr, result)):
            for frange in result['facet']['range']:
                yield (solr, result['facet']['range'][frange])

        def andTheRangeStart(self, (_, frange)):
            expect(frange).to_include('start')

        def andTheRangeGap(self, (_, frange)):
            expect(frange).to_include('gap')

        def andTheRangeEnd(self, (_, frange)):
            expect(frange).to_include('end')
