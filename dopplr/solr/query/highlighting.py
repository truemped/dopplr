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
"""
Solr result snippet highlighting.
"""
from dopplr.basequery import BaseQuery


class Highlighting(BaseQuery):
    """
    Highlighting with solr.
    """

    def __init__(self, fields, fragsize=100, pre='<em>', post='</em>'):
        """
        Initialize the query value.
        """
        self.__fields = fields
        self.__pre = pre
        self.__post = post
        self.__fragsize = fragsize

    def get_params(self):
        """
        Return the list of query params.
        """
        result_list = list()
        result_list.append(('hl', 'true'))
        result_list.append(('hl.fl', ",".join(self.__fields)))
        result_list.append(('hl.simple.pre', self.__pre))
        result_list.append(('hl.simple.post', self.__post))
        result_list.append(('hl.fragsize', self.__fragsize))
        return result_list
