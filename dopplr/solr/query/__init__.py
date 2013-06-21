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
"""
The implementations for Apache Solr queries.
"""
from .boostquery import BoostQuery
from .boostquery import BoostFunctionQuery
from .facets import FacetFieldQuery
from .facets import FacetQueryQuery
from .facets import MultiselectFacetQuery
from .facets import RangeFacetQuery
from .grouping import ResultGrouping
from .highlighting import Highlighting
from .join import JoinQuery
from .join import JoinFilterQuery
from .mlt import MoreLikeThisQuery
from .paging import Paging
from .query import Query, FilterQuery
from .spellcheck import Spellcheck
from .spatial import BoundingBoxSpatialQuery
from .spatial import GeofiltSpatialQuery
from .spatial import SpatialQuery


__all__ = [
    'BoostQuery',
    'BoostFunctionQuery',
    'BoundingBoxSpatialQuery',
    'FacetFieldQuery',
    'FacetQueryQuery',
    'GeofiltSpatialQuery',
    'Highlighting',
    'JoinQuery',
    'JoinFilterQuery',
    'MultiselectFacetQuery',
    'RangeFacetQuery',
    'MoreLikeThisQuery',
    'Paging',
    'Query',
    'FilterQuery',
    'ResultGrouping',
    'Spellcheck',
    'SpatialQuery',
]
