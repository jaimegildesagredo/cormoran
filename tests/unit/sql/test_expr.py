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

from cormoran.persistent import Persistent
from cormoran.fields import StringField
from cormoran.sql.expr import Insert


class PersistentClass(Persistent):
    field = StringField()
    other = StringField()


class TestInsert(unittest.TestCase):
    def test_table_is_persistent_cormoran_name(self):
        assert_that(self.insert.table, is_(self.persistent.__cormoran_name__))

    def test_columns_are_persistent_fields_names(self):
        assert_that(self.insert.columns, contains('field', 'other'))

    def test_values_are_persistent_stored_values(self):
        self.persistent.field = 'test'

        assert_that(self.insert.values, contains('test', None))

    def test_str_is_insert_statement(self):
        assert_that(str(self.insert), is_(
            'INSERT INTO persistentclass (field, other) VALUES (?, ?)'))

    def setUp(self):
        self.persistent = PersistentClass()
        self.insert = Insert(self.persistent)

