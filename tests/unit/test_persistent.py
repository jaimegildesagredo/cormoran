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

from cormoran.persistent import Persistent
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

    def test_use_more_than_one_primary_field_sets_cormoran_pk_attribute(self):
        class PersistentClass(Persistent):
            field = StringField(primary=True)
            other = StringField(primary=True)

        assert_that(PersistentClass.__cormoran_pk__, has_entries({
            'field': PersistentClass.field,
            'other': PersistentClass.other
        }))

    def test_without_primary_field_raises_value_error(self):
        with assert_raises(ValueError):
            class PersistentClass(Persistent):
                _id = IntegerField(primary=False)

    def test_default_sets_id_integer_primary_field(self):
        assert_that(self.persistent_class._id, instance_of(IntegerField))
        assert_that(self.persistent_class._id.primary)
        assert_that(self.persistent_class.__cormoran_fields__,
            has_entry('_id', self.persistent_class._id))
        assert_that(self.persistent_class.__cormoran_pk__,
            has_entry('_id', self.persistent_class._id))

    def test_overwrite_default_id_field(self):
        class PersistentClass(Persistent):
            _id = StringField()
            field = StringField(primary=True)

        assert_that(PersistentClass._id, instance_of(StringField))
        assert_that(not PersistentClass._id.primary)
        assert_that(PersistentClass.__cormoran_fields__,
            has_entry('_id', PersistentClass._id))

    def test_subclass_inherits_fields_from_super_class(self):
        class PersistentSubclass(self.persistent_class):
            pass

        assert_that(PersistentSubclass.field, is_(self.persistent_class.field))
        assert_that(PersistentSubclass.__cormoran_fields__,
            has_entries(self.persistent_class.__cormoran_fields__))

    def test_overwrite_inherited_field_from_super_class(self):
        class PersistentSubclass(self.persistent_class):
            _id = StringField()
            field = StringField(primary=True)

        assert_that(PersistentSubclass._id, instance_of(StringField))
        assert_that(PersistentSubclass._id, is_not(self.persistent_class._id))
        assert_that(PersistentSubclass.__cormoran_fields__,
            has_entry('_id', PersistentSubclass._id))

    def test_instantiate_with_kw_arguments_sets_fields_values(self):
        persistent = self.persistent_class(field=u'test', other=u'other')

        assert_that(persistent.field, is_(u'test'))
        assert_that(persistent.other, is_(u'other'))

    def test_instantiate_with_one_kw_argument_sets_these_field_value(self):
        persistent = self.persistent_class(field=u'test')

        assert_that(persistent.field, is_(u'test'))
        assert_that(persistent.other, is_(self.persistent_class.other.default))

    def test_dict_returns_a_fields_values_dict(self):
        persistent = self.persistent_class(_id=1, field=u'test', other=u'other')
        assert_that(dict(persistent),
            has_entries({u'_id': 1, u'field': u'test', u'other': u'other'}))

    def test_persisted_flag_is_false_by_defalt(self):
        persistent = self.persistent_class()

        assert_that(not persistent.__cormoran_persisted__)

    def test_persisted_flag_is_instance_independet(self):
        persistent = self.persistent_class()
        another = self.persistent_class()

        persistent.__cormoran_persisted__ = True

        assert_that(persistent.__cormoran_persisted__,
            is_not(another.__cormoran_persisted__))

    def test_data_store_dict_is_empty_by_default(self):
        persistent = self.persistent_class()

        assert_that(persistent.__cormoran_data__, instance_of(dict))
        assert_that(persistent.__cormoran_data__, has_length(0))

    def test_data_store_dict_is_instance_independent(self):
        persistent = self.persistent_class()
        another = self.persistent_class()

        persistent.__cormoran_data__['field'] = u'test'

        assert_that(another.__cormoran_data__, has_length(0))

    def setUp(self):
        class PersistentClass(Persistent):
            field = StringField(name='field_name')
            other = StringField()

        self.persistent_class = PersistentClass

