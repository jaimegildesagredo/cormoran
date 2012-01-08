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

from cormoran.persistent import Persistent, PersistentError
from cormoran.fields import StringField, IntegerField


class TestPersistent(unittest.TestCase):
    def test_sets_field_name_if_not_already_setted(self):
        class PersistentClass(Persistent):
            field = StringField()

        assert_that(PersistentClass.field.name, is_('field'))

    def test_doesnt_set_field_name_if_already_setted(self):
        assert_that(self.persistent_class.field.name, is_('field_name'))

    def test_create_fields_dict_with_persistent_fields(self):
        assert_that(self.persistent_class.__cormoran_fields__, has_entries({
            'field': self.persistent_class.field,
            'other': self.persistent_class.other
        }))

    def test_default_cormoran_name_is_lowercase_class_name(self):
        assert_that(self.persistent_class.__cormoran_name__,
            is_(self.persistent_class.__name__.lower()))

    def test_set_cormoran_name_overwrites_default(self):
        class PersistentClass(Persistent):
            __cormoran_name__ = 'test'

        assert_that(PersistentClass.__cormoran_name__, is_('test'))

    def test_use_primary_field_sets_cormoran_pk_attribute(self):
        class PersistentClass(Persistent):
            field = StringField(primary=True)

        assert_that(PersistentClass.__cormoran_pk__, has_entry(
            'field', PersistentClass.field))

    def test_use_more_than_one_primary_field_raises_error(self):
        with assert_raises(PersistentError):
            class PersistentClass(Persistent):
                field = StringField(primary=True)
                other = StringField(primary=True)

    def test_default_primary_key_is_integer_field(self):
        cormoran_fields = self.persistent_class.__cormoran_fields__
        cormoran_pk = self.persistent_class.__cormoran_pk__

        assert_that(cormoran_pk, has_entry('_id', instance_of(IntegerField)))
        assert_that(cormoran_fields, has_entry(
            '_id', instance_of(IntegerField)
        ))
        assert_that(cormoran_pk['_id'].primary)

    def setUp(self):
        class PersistentClass(Persistent):
            field = StringField(name='field_name')
            other = StringField()

        self.persistent_class = PersistentClass

