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
from nose.tools import assert_raises

from cormoran.fields import BaseField, FieldError


class CustomField(BaseField):
    pass


class TestBaseField(unittest.TestCase):
    def test_instantiate_raises_field_error(self):
        with assert_raises(FieldError):
            BaseField()

    def test_instantiate_subclass_is_ok(self):
        CustomField()

    def test_get_from_class_returns_field(self):
        assert_that(self.cls.field, is_(self.field))

    def test_get_from_instance_returns_default_value(self):
        assert_that(self.cls().field, is_(self.field.default))

    def test_get_from_instance_returns_stored_value(self):
        instance = self.cls()
        instance.field = u'test'

        assert_that(instance.field, is_(u'test'))
        assert_that(self.cls.field, is_(self.field))

    def setUp(self):
        self.field = CustomField()

        class Cls(object):
            field = self.field

        self.cls = Cls

