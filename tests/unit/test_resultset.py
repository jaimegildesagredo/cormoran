# -*- coding: utf-8 -*-
#
# Cormoran is a fast and lightweight persistence framework.
# Copyright (C) 2012 Jaime Gil de Sagredo Luna <jaimegildesagredo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest
from hamcrest import *
from pyDoubles.framework import *
from nose.tools import assert_raises

from cormoran.persistent import Persistent
from cormoran.fields import StringField
from cormoran.resultset import ResultSet


class TestResultSet(unittest.TestCase):
    def test_iter_yields_results(self):
        when(self.persistence.select).then_return(self.result())

        result = list(self.resultset)

        assert_that(len(result), is_(2))
        assert_that(result[0].field, is_(u'test1'))
        assert_that(result[0]._id, is_(1))
        assert_that(result[1].field, is_(u'test2'))
        assert_that(result[1]._id, is_(2))

    def test_iter_sets_persisted_flag_to_true(self):
        when(self.persistence.select).then_return(self.result())

        result = list(self.resultset)

        assert_that(result[0].__cormoran_persisted__)
        assert_that(result[1].__cormoran_persisted__)

    def test_iter_calls_persistence_select_with_filters(self):
        when(self.persistence.select).then_return(self.result())

        self.resultset.filter(field=u'test')

        list(self.resultset)

        assert_that_method(self.persistence.select).was_called().with_args(
            PersistentClass, filters=self.resultset._filters)

    def test_filter_adds_kwargs_as_filters(self):
        self.resultset.filter(field=u'test')

        assert_that(self.resultset._filters, has_entry('field', u'test'))

    def test_filter_inexistent_field_argument_raises_value_error(self):
        with assert_raises(ValueError):
            self.resultset.filter(inexistent=u'foo')

    def result(self):
        return [
            {u'_id': 1, u'field': u'test1'},
            {u'_id': 2, u'field': u'test2'}
        ]

    def setUp(self):
        self.persistence = empty_spy()
        self.resultset = ResultSet(self.persistence, PersistentClass)


class PersistentClass(Persistent):
    field = StringField()
