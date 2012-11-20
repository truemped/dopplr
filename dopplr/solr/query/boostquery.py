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
Solr Boost Query
"""
from dopplr.basequery import BaseQuery


class BoostQuery(BaseQuery):
    """
    A boosting query.
    """

    def __init__(self, boostquery):
        """
        Add `boostqueries`.
        """
        self.__boostquery = boostquery

    def get_params(self):
        """
        Return the list of query params for the `BoostQuery`.
        """
        params = []
        params.append(('bq', self.__boostquery))

        return params


class BoostFunctionQuery(BaseQuery):
    """
    A boosting function query.
    """

    def __init__(self, boostfunction, **kwargs):
        """
        Add `boostfunctions` and possible external boosting parameters.
        """
        self.__boostfunction = boostfunction
        self.__external_boost_params = []
        for arg in kwargs:
            if "$" + arg in self.__boostfunction:
                self.__external_boost_params.append((arg, kwargs[arg]))

    def get_params(self):
        """
        Return the list of query params for the `BoostFunctionQuery`.
        """
        params = []
        params.append(('bf', self.__boostfunction))
        params.extend(self.__external_boost_params)

        return params
