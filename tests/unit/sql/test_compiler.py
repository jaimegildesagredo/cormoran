# -*- coding: utf-8 -*-

import unittest
from hamcrest import *

from cormoran.persistent import Persistent
from cormoran.fields import StringField
from cormoran.sql.compiler import SQLCompiler


class User(Persistent):
    name = StringField()

class Group(Persistent):
    name = StringField(name='groupname')


class TestSQLCompiler(unittest.TestCase):
    def test_select_returns_sql_and_params(self):
        compiled, params = self.compiler.select(User)

        assert_that(compiled, is_('SELECT _id, name FROM User'))
        assert_that(params, has_length(0))

    def test_select_with_different_field_names_uses_alias(self):
        compiled, params = self.compiler.select(Group)

        assert_that(compiled, is_('SELECT _id, groupname AS name FROM Group'))

    def test_select_with_filter_uses_where_clause(self):
        compiled, params = self.compiler.select(User, filters={'name': u'Mike'})

        assert_that(compiled, is_('SELECT _id, name FROM User WHERE name=?'))
        assert_that(params, contains(u'Mike'))

    def test_select_with_filters_uses_where_clause(self):
        compiled, params = self.compiler.select(User,
            filters={'name': u'Mike', '_id': 1})

        assert_that(compiled, is_(
            'SELECT _id, name FROM User WHERE _id=? AND name=?'))
        assert_that(params, contains(1, u'Mike'))

    def test_select_with_limit_stop_uses_limit_clause(self):
        compiled, params = self.compiler.select(User, limit=slice(1))

        assert_that(compiled, is_('SELECT _id, name FROM User LIMIT 1'))

    def test_select_with_limit_start_and_stop_uses_offset_clause(self):
        compiled, params = self.compiler.select(User, limit=slice(1, 1))

        assert_that(compiled, is_('SELECT _id, name FROM User LIMIT 1 OFFSET 1'))

    def test_select_with_empty_slice_limit_doesnt_uses_limit_clause(self):
        compiled, params = self.compiler.select(User, limit=slice(None))

        assert_that(compiled, is_('SELECT _id, name FROM User'))

    def test_update_returns_sql_and_params(self):
        compiled, params = self.compiler.update(self.user)

        assert_that(compiled, is_('UPDATE User SET _id=?, name=? WHERE _id=?'))
        assert_that(params, contains(1, u'Bob', 1))

    def test_delete_returns_sql_and_params(self):
        compiled, params = self.compiler.delete(self.user)

        assert_that(compiled, is_('DELETE FROM User WHERE _id=?'))
        assert_that(params, contains(1))

    def test_insert_returns_sql_and_params(self):
        compiled, params = self.compiler.insert(self.user)

        assert_that(compiled, is_(
            'INSERT INTO User (_id, name) VALUES (?, ?)'))
        assert_that(params, contains(1, u'Bob'))

    def test_insert_with_different_field_names(self):
        compiled, params = self.compiler.insert(self.group)

        assert_that(compiled, is_(
            'INSERT INTO Group (_id, groupname) VALUES (?, ?)'))

    def setUp(self):
        self.user = User(_id=1, name=u'Bob')
        self.group = Group(_id=1, name=u'Admin')

        self.compiler = SQLCompiler()


class TestSQLCompilerWithPlaceholder(unittest.TestCase):
    def test_select_returns_sql_and_params(self):
        compiled, params = self.compiler.select(User, filters={'name': u'Mike'})

        assert_that(compiled, is_('SELECT _id, name FROM User WHERE name=%s'))

    def test_update_returns_sql_and_params(self):
        compiled, params = self.compiler.update(self.user)

        assert_that(compiled, is_('UPDATE User SET _id=%s, name=%s WHERE _id=%s'))

    def test_delete_returns_sql_and_params(self):
        compiled, params = self.compiler.delete(self.user)

        assert_that(compiled, is_('DELETE FROM User WHERE _id=%s'))

    def test_insert_returns_sql_and_params(self):
        compiled, params = self.compiler.insert(self.user)

        assert_that(compiled, is_(
            'INSERT INTO User (_id, name) VALUES (%s, %s)'))

    def setUp(self):
        self.user = User(_id=1, name=u'Bob')

        self.compiler = SQLCompiler(placeholder='%s')