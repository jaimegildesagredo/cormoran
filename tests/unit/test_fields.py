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
from nose.tools import assert_raises, nottest

from cormoran.persistent import Persistent
from cormoran.fields import IntegerField, StringField, FloatField, BooleanField

class _BaseFieldTestCase(unittest.TestCase):

    def test_name_is_none_by_default(self):
        assert_that(self.field.name, is_(None))

    def test_name_from_constructor_key_argument(self):
        self.field = self.FieldClass(name=u'field')

        assert_that(self.field.name, is_(u'field'))

    def test_name_from_constructor_positional_argument(self):
        self.field = self.FieldClass(u'field')

        assert_that(self.field.name, is_(u'field'))

    def test_primary_is_false_by_default(self):
        assert_that(not self.field.primary)

    def test_primary_from_constructor_argument(self):
        self.field = self.FieldClass(primary=True)

        assert_that(self.field.primary)

    def test_default_is_none_by_default(self):
        assert_that(self.field.default, is_(None))

    def test_default_from_constructor_argument(self):
        self.field = self.FieldClass(default=self.valid())

        assert_that(self.field.default, is_(self.valid()))

    def test_invalid_default_raises_value_error(self):
        with assert_raises(ValueError):
            self.FieldClass(default=self.invalid())

    def test_nullable_is_true_by_default(self):
        assert_that(self.field.nullable)

    def test_nullable_from_constructor_argument(self):
        self.field = self.FieldClass(nullable=False)

        assert_that(not self.field.nullable)

    def test_get_from_persistent_class_returns_field(self):
        assert_that(self.User.field, instance_of(self.FieldClass))

    def test_get_from_persistent_instance_returns_default(self):
        assert_that(self.User().field, is_(None))

    def test_get_from_persistent_instance_returns_value(self):
        assert_that(self.User(field=self.valid()).field, is_(self.valid()))

    def test_set_stores_value_in_persistent_data_store(self):
        user = self.User(field=self.valid())

        assert_that(user.__cormoran_data__, has_entry(u'field', self.valid()))

    def test_set_invalid_value_raises_value_error(self):
        with assert_raises(ValueError):
            self.User(field=self.invalid())

    def test_set_none_value_if_nullable_is_ok(self):
        assert_that(self.User(field=None).field, is_(None))

    def test_set_none_value_if_not_nullable_raises_value_error(self):
        with assert_raises(ValueError):
            self.User(another=None)

    def setUp(self):
        class User(Persistent):
            field = self.FieldClass()
            another = self.FieldClass(nullable=False)

        self.User = User
        self.field = self.FieldClass()


class TestIntegerField(_BaseFieldTestCase):
    FieldClass = IntegerField

    def valid(self):
        return 1

    def invalid(self):
        return u'test'


class TestStringField(_BaseFieldTestCase):
    FieldClass = StringField

    @nottest
    def test_invalid_default_raises_value_error(self):
        pass

    @nottest
    def test_set_invalid_value_raises_value_error(self):
        pass

    def valid(self):
        return u'test'


class TestFloatField(_BaseFieldTestCase):
    FieldClass = FloatField

    def test_set_integer_stores_float_value_in_persistent_data_store(self):
        user = self.User(field=1)

        assert_that(user.field, is_(1.0))

    def valid(self):
        return 1.0

    def invalid(self):
        return u'test'


class TestBooleanField(_BaseFieldTestCase):
    FieldClass = BooleanField

    @nottest
    def test_invalid_default_raises_value_error(self):
        pass

    @nottest
    def test_set_invalid_value_raises_value_error(self):
        pass

    def test_set_unicode_stores_bool_value_in_persistent_data_store(self):
        user = self.User(field=u'test')

        assert_that(user.field, is_(True))

    def valid(self):
        True
