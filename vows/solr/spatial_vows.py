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

from dopplr.solr.query import BoundingBoxSpatialQuery
from dopplr.solr.query import GeofiltSpatialQuery
from dopplr.solr.query import SpatialQuery


@Vows.batch
class TheSpatialQuery(Vows.Context):

    class WithDefaultParams(Vows.Context):

        def topic(self):
            lat = 0.0
            lon = 0.0
            sfield = "my_field"
            return SpatialQuery(lat, lon, sfield).get_params()

        def mustIncludeFunctionTypeParameter(self, topic):
            expect(topic).to_include(('fq', '{!geofilt}'))

        def mustIncludeCorrectlyFormattedPoint(self, topic):
            expect(topic).to_include(('pt', '0.0,0.0'))

        def mustIncludeDistanceParameter(self, topic):
            expect(topic).to_include(('d', 5))

        def mustIncludeSpatialFieldParameter(self, topic):
            expect(topic).to_include(('sfield', 'my_field'))

    class WithBboxSpatialQuery(WithDefaultParams):

        def topic(self):
            lat = 0.0
            lon = 0.0
            sfield = "my_field"
            return BoundingBoxSpatialQuery(lat, lon, sfield).get_params()

        def mustIncludeFunctionTypeParameter(self, topic):
            expect(topic).to_include(('fq', '{!bbox}'))

    class WithCustomDistanceParameter(WithDefaultParams):

        def topic(self):
            lat = 0.0
            lon = 0.0
            sfield = "my_field"
            return GeofiltSpatialQuery(lat, lon, sfield,
                distance=10).get_params()

        def mustIncludeDistanceParameter(self, topic):
            expect(topic).to_include(('d', 10))
