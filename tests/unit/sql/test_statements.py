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
from cormoran.sql.statements import SQLStmt, Select, Update, Delete, Insert

class User(Persistent):
    __cormoran_name__ = u'users'

    name = StringField()


class Group(Persistent):
    __cormoran_name__ = u'groups'

    name = StringField(name='groupname', primary=True)


class _StmtTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User(_id=1, name=u'Bob')
        self.group = Group(_id=1, name=u'Admin')

        self.stmt = self.StmtClass()


class TestSQLStmt(unittest.TestCase):
    def test_write_append_chunk_to_buffer(self):
        self.stmt.write(u'test')

        assert_that(self.stmt._buffer, contains(u'test'))

    def test_flush_returns_concatenated_buffer(self):
        self.stmt.write(u'test')

        assert_that(self.stmt.flush(), is_(u'test'))

    def test_flush_returns_concatenated_buffer_separated_by_space(self):
        self.stmt.write(u'test')
        self.stmt.write(u'another')

        assert_that(self.stmt.flush(), is_(u'test another'))

    def test_append_adds_arguments_to_params(self):
        self.stmt.append([1, 2])

        assert_that(self.stmt._params, contains(1, 2))

    def test_write_and_append_preserves_insertion_order(self):
        self.stmt.write(u'test')
        self.stmt.append([1, 2])
        self.stmt.write(u'another')
        self.stmt.append([0])

        assert_that(self.stmt.flush(), is_('test another'))
        assert_that(self.stmt._params, contains(1, 2, 0))

    def setUp(self):
        self.stmt = SQLStmt()


class TestSelect(unittest.TestCase):
    def test_compile_returns_compiled_sql_and_params(self):
        compiled, params = self.stmt.compile(User)

        assert_that(compiled, is_('SELECT _id, name FROM users'))
        assert_that(params, has_length(0))

    def test_compile_with_different_field_names_use_alias(self):
        compiled, params = self.stmt.compile(Group)

        assert_that(compiled, is_('SELECT _id, groupname AS name FROM groups'))

    def test_compile_with_filter_adds_where_clause(self):
        compiled, params = self.stmt.compile(User, filters={'name': u'Mike'})

        assert_that(compiled, is_('SELECT _id, name FROM users WHERE name=?'))
        assert_that(params, contains(u'Mike'))

    def test_compile_with_filters_adds_where_clause(self):
        compiled, params = self.stmt.compile(User,
            filters={'name': u'Mike', '_id': 1})

        assert_that(compiled, is_(
            'SELECT _id, name FROM users WHERE _id=? AND name=?'))
        assert_that(params, contains(1, u'Mike'))

    def test_compile_with_limit_stop_adds_limit_clause(self):
        compiled, params = self.stmt.compile(User, limit=slice(1))

        assert_that(compiled, is_('SELECT _id, name FROM users LIMIT 1'))

    def test_compile_with_limit_start_and_stop_adds_offset_clause(self):
        compiled, params = self.stmt.compile(User, limit=slice(1, 1))

        assert_that(compiled, is_('SELECT _id, name FROM users LIMIT 1 OFFSET 1'))

    def test_compile_with_empty_slice_limit_doesnt_adds_limit_clause(self):
        compiled, params = self.stmt.compile(User, limit=slice(None))

        assert_that(compiled, is_('SELECT _id, name FROM users'))

    def setUp(self):
        self.stmt = Select()


class TestUpdate(_StmtTestCase):
    StmtClass = Update

    def test_compile_returns_compiled_sql_and_params(self):
        compiled, params = self.stmt.compile(self.user)

        assert_that(compiled, is_('UPDATE users SET _id=?, name=? WHERE _id=?'))
        assert_that(params, contains(1, u'Bob', 1))

    def test_compile_with_persistent_having_various_primary_fields(self):
        compiled, params = self.stmt.compile(self.group)

        assert_that(compiled, is_(
            'UPDATE groups SET _id=?, groupname=? WHERE _id=? AND groupname=?'))
        assert_that(params, contains(1, u'Admin', 1, u'Admin'))


class TestDelete(_StmtTestCase):
    StmtClass = Delete

    def test_compile_returns_compiled_sql_and_params(self):
        compiled, params = self.stmt.compile(self.user)

        assert_that(compiled, is_('DELETE FROM users WHERE _id=?'))
        assert_that(params, contains(1))

    def test_compile_with_persistent_having_various_primary_fields(self):
        compiled, params = self.stmt.compile(self.group)

        assert_that(compiled, is_(
            'DELETE FROM groups WHERE _id=? AND groupname=?'))
        assert_that(params, contains(1, u'Admin'))


class TestInsert(_StmtTestCase):
    StmtClass = Insert

    def test_compile_returns_compiled_sql_and_params(self):
        compiled, params = self.stmt.compile(self.user)

        assert_that(compiled, is_(
            'INSERT INTO users (_id, name) VALUES (?, ?)'))
        assert_that(params, contains(1, u'Bob'))

    def test_compile_with_different_field_names(self):
        compiled, params = self.stmt.compile(self.group)

        assert_that(compiled, is_(
            'INSERT INTO groups (_id, groupname) VALUES (?, ?)'))
