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

from doppler.solr.query import Highlighting


@Vows.batch
class AHighlightingQuery(Vows.Context):

    class WithRequiredParams(Vows.Context):

        def topic(self):
            return Highlighting(['title']).get_params()

        def mustActivateHighlighting(self, topic):
            expect(topic).to_include(('hl', 'true'))

        def mustIncludeTheHighlightingFields(self, topic):
            expect(topic).to_include(('hl.fl', 'title'))

        def mustIncludeThePreTag(self, topic):
            expect(topic).to_include(('hl.simple.pre', '<em>'))

        def mustIncludeThePostTag(self, topic):
            expect(topic).to_include(('hl.simple.post', '</em>'))

        def mustIncludeTheFragSize(self, topic):
            expect(topic).to_include(('hl.fragsize', 100))

    class WithAFragSize(WithRequiredParams):

        def topic(self):
            return Highlighting(['title'], fragsize=200).get_params()

        def mustIncludeTheFragSize(self, topic):
            expect(topic).to_include(('hl.fragsize', 200))

    class WithDifferentTags(WithRequiredParams):

        def topic(self):
            q = Highlighting(['title'], pre='<span>', post='</span>')
            return q.get_params()

        def mustIncludeThePreTag(self, topic):
            expect(topic).to_include(('hl.simple.pre', '<span>'))

        def mustIncludeThePostTag(self, topic):
            expect(topic).to_include(('hl.simple.post', '</span>'))
