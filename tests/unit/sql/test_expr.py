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
from nose.tools import nottest

from cormoran.persistent import Persistent
from cormoran.fields import StringField, IntegerField
from cormoran.sql.expr import Insert, Update, Delete, Select


class PersistentClass(Persistent):
    _id = IntegerField(primary=True)
    field = StringField(primary=True)
    other = StringField()


class _ExprTestCase(unittest.TestCase):
    def test_table_is_persistent_cormoran_name(self):
        assert_that(self.expr.table, is_(self.persistent.__cormoran_name__))

    def test_columns_are_persistent_fields_names(self):
        assert_that(self.expr.columns, contains('field', '_id', 'other'))

    def test_columns_and_values_are_in_same_order(self):
        self.persistent.field = 'test'

        self.assert_that_in_same_order('field')
        self.assert_that_in_same_order('_id')

    def assert_that_in_same_order(self, field):
            assert_that(self.expr.columns.index(field),
                is_(self.expr.values.index(getattr(self.persistent, field)))
            )

    def setUp(self):
        self.persistent = PersistentClass()
        self.expr = self.expr_cls(self.persistent)


class TestInsert(_ExprTestCase):
    expr_cls = Insert

    def test_values_are_persistent_stored_values(self):
        self.persistent.field = 'test'
        self.persistent.other = 'other'

        assert_that(self.expr.values, contains('test', None, 'other'))

    def test_str_is_insert_statement(self):
        assert_that(str(self.expr), is_(
            'INSERT INTO persistentclass (field, _id, other) VALUES (?, ?, ?)'))


class TestUpdate(_ExprTestCase):
    expr_cls = Update

    def test_values_are_persistent_stored_values_and_where_clause_values(self):
        self.persistent.field = 'test'
        self.persistent.other = 'other'

        assert_that(self.expr.values, contains('test', None, 'other', 'test', None))

    def test_str_is_update_statement(self):
        assert_that(str(self.expr), is_(
            'UPDATE persistentclass SET field=?, _id=?, other=? WHERE field=? AND _id=?'
        ))


class TestDelete(_ExprTestCase):
    expr_cls = Delete

    def test_values_are_persistent_object_primary_fields_values(self):
        self.persistent._id = 1
        self.persistent.field = 'test'

        assert_that(self.expr.values, contains('test', 1))

    def test_str_is_delete_statement(self):
        assert_that(str(self.expr), is_(
            'DELETE FROM persistentclass WHERE field=? AND _id=?'))


class TestSelect(_ExprTestCase):
    expr_cls = Select

    def test_table_is_persistent_cormoran_name(self):
        assert_that(self.expr.table, is_(self.persistent.__cormoran_name__))

    @nottest
    def test_columns_are_persistent_fields_names(self):
        pass

    def test_columns_are_an_empty_list(self):
        assert_that(self.expr.columns, has_length(0))

    def test_values_are_an_empty_list(self):
        assert_that(self.expr.values, has_length(0))

    @nottest
    def test_columns_and_values_are_in_same_order(self):
        pass

    def test_str_is_select_statement(self):
        assert_that(str(self.expr), is_('SELECT * FROM persistentclass'))
