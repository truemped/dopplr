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

from dopplr.solr.query.mlt import MoreLikeThisQuery


@Vows.batch
class MoreLikeThisQueries(Vows.Context):

    class WithRequiredParameters(Vows.Context):

        def topic(self):
            return MoreLikeThisQuery(['content']).get_params()

        def mltOnMustBePresent(self, topic):
            expect(topic).to_include(('mlt', 'true'))

        def mltFieldsMustBeCorrect(self, topic):
            expect(topic).to_include(('mlt.fl', 'content'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(2)

    class WithOptionalParameters(Vows.Context):

        def topic(self):
            valid_params = [
                'mintf',
                'mindf',
                'minwl',
                'maxwl',
                'maxqt',
                'maxntp',
                'boost',
                'qf',
                'count']

            for v in valid_params:
                kwargs = {v: 'a'}
                q = MoreLikeThisQuery(['content'], **kwargs)
                yield (v, q.get_params())

        def mltOnMustBePresent(self, (field, params)):
            expect(params).to_include(('mlt', 'true'))

        def mltFieldsMustBeCorrect(self, (field, params)):
            expect(params).to_include(('mlt.fl', 'content'))

        def theNumberOfParamsMatches(self, (field, params)):
            expect(params).to_length(3)

        def theQueryMustMatch(self, (field, params)):
            expect(params).to_include(('mlt.%s' % field, 'a'))

    class WithAStreamBody(Vows.Context):

        def topic(self):
            return MoreLikeThisQuery(['content'], stream_body="b").get_params()

        def mltOnMustBePresent(self, topic):
            expect(topic).to_include(('mlt', 'true'))

        def mltFieldsMustBeCorrect(self, topic):
            expect(topic).to_include(('mlt.fl', 'content'))

        def theNumberOfParamsMatches(self, topic):
            expect(topic).to_length(3)

        def theQueryMustMatch(self, topic):
            expect(topic).to_include(('stream.body', 'b'))
