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

from doppler.solr.query import Spellcheck


@Vows.batch
class TheSpellcheckQuery(Vows.Context):

    class WithDefaultParams(Vows.Context):

        def topic(self):
            return Spellcheck().get_params()

        def mustActivateSpellchecking(self, topic):
            expect(topic).to_include(('spellcheck', 'true'))

        def mustIncludeTheCollateParam(self, topic):
            expect(topic).to_include(('spellcheck.collate', 'true'))

        def mustIncludeTheOnlyMorePopularParam(self, topic):
            expect(topic).to_include(('spellcheck.onlyMorePopular', 'true'))

        def maybeIncludeTheDictionary(self, topic):
            l = filter(lambda (x,v): x == 'spellcheck.dictionary', topic)
            expect(l).to_length(0)

    class WithNoCollationAndNoMorePopular(WithDefaultParams):

        def topic(self):
            return Spellcheck(collate=False, onlyMorePopular=False).get_params()

        def mustIncludeTheCollateParam(self, topic):
            expect(topic).to_include(('spellcheck.collate', 'false'))

        def mustIncludeTheOnlyMorePopularParam(self, topic):
            expect(topic).to_include(('spellcheck.onlyMorePopular', 'false'))

    class WithCountParam(WithDefaultParams):

        def topic(self):
            return Spellcheck(count=4).get_params()

        def mustIncludeTheCountParam(self, topic):
            expect(topic).to_include(('spellcheck.count', '4'))
