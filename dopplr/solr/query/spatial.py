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
from dopplr.basequery import BaseQuery


class SpatialQuery(BaseQuery):
    """
    `SpatialQuery` to search with geolocations
    param lat the latitute point part
    param lon the lontitude point part
    param sfield the location type field
    param function_type is one of {geofilt, bbox}
    param distance the radius around the given location
    """
    def __init__(self, lat, lon, sfield, function_type='geofilt', distance=5):
        super(SpatialQuery, self).__init__()
        self.__lat = lat
        self.__lon = lon
        self.__sfield = sfield
        self.__function_type = function_type
        self.__distance = distance

    def get_params(self):
        params = []
        params.append(('fq', '{!%s}' % (self.__function_type)))
        params.append(('sfield', self.__sfield))
        params.append(('pt', '%s,%s' % (self.__lat, self.__lon)))
        params.append(('d', self.__distance))
        return params


class GeofiltSpatialQuery(SpatialQuery):
    """
    `GeofiltSpatialQuery` to search with geofilt functionality
    param lat the latitute point part
    param lon the lontitude point part
    param sfield the location type field
    param distance the radius around the given location
    """
    def __init__(self, lat, lon, sfield, distance=5):
        super(GeofiltSpatialQuery, self).__init__(lat, lon, sfield,
            function_type='geofilt', distance=distance)


class BoundingBoxSpatialQuery(SpatialQuery):
    """
    `BoundingBoxSpatialQuery` to search with bbox functionality
    param lat the latitute point part
    param lon the lontitude point part
    param sfield the location type field
    param distance the radius around the given location
    """
    def __init__(self, lat, lon, sfield, distance=5):
        super(BoundingBoxSpatialQuery, self).__init__(lat, lon, sfield,
            function_type='bbox', distance=distance)
