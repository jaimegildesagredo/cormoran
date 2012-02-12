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

from cormoran.persistent import Persistent
from cormoran.fields import StringField
from cormoran.resultset import ResultSet


class TestResultSet(unittest.TestCase):
    def test_iterate_over_resultset_returns_all(self):
        persistence = empty_spy()

        when(persistence.select).with_args(PersistentClass).then_return([{u'_id': 1, u'field': u'test1'}, {u'_id': 2, u'field': u'test2'}])

        result = list(ResultSet(persistence, PersistentClass))

        assert_that(len(result), is_(2))
        assert_that(result[0].field, is_(u'test1'))
        assert_that(result[0]._id, is_(1))
        assert_that(result[1].field, is_(u'test2'))
        assert_that(result[1]._id, is_(2))

    def test_persistent_objects_have_persisted_flag_to_true(self):
        persistence = empty_spy()

        when(persistence.select).with_args(PersistentClass).then_return([{u'_id': 1, u'field': u'test1'}])

        result = list(ResultSet(persistence, PersistentClass))

        assert_that(result[0].__cormoran_persisted__)



class PersistentClass(Persistent):
    field = StringField()
