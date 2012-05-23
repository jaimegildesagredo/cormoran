# -*- coding: utf-8 -*-

import unittest
from hamcrest import *

from cormoran.uri import URI


class TestURI(unittest.TestCase):
    def test_schema(self):
        uri = URI('sqlite://')

        assert_that(uri.schema, is_('sqlite'))

    def test_db(self):
        uri = URI('sqlite:///database')

        assert_that(uri['db'], is_('database'))

    def test_db_is_empty(self):
        uri = URI('sqlite:///')

        assert_that(uri['db'], is_(''))

    def test_db_in_memory_sqlite(self):
        uri = URI('sqlite:///:memory:')

        assert_that(uri['db'], is_(':memory:'))

    def test_user(self):
        uri = URI('mysql://username@')

        assert_that(uri['user'], is_('username'))

    def test_user_and_passwd(self):
        uri = URI('mysql://username:password@')

        assert_that(uri['user'], is_('username'))
        assert_that(uri['passwd'], is_('password'))

    def test_host(self):
        uri = URI('mysql://hostname')

        assert_that(uri['host'], is_('hostname'))

    def test_host_and_port(self):
        uri = URI('mysql://hostname:1234')

        assert_that(uri['host'], is_('hostname'))
        assert_that(uri['port'], is_(1234))

    def test_user_password_host_and_port(self):
        uri = URI('mysql://username:password@hostname:1234')

        assert_that(uri['user'], is_('username'))
        assert_that(uri['passwd'], is_('password'))
        assert_that(uri['host'], is_('hostname'))
        assert_that(uri['port'], is_(1234))

    def test_uri(self):
        uri = URI('mysql://username:password@hostname:1234/database')

        assert_that(uri.schema, is_('mysql'))

        assert_that(uri['db'], is_('database'))
        assert_that(uri['user'], is_('username'))
        assert_that(uri['passwd'], is_('password'))
        assert_that(uri['host'], is_('hostname'))
        assert_that(uri['port'], is_(1234))
