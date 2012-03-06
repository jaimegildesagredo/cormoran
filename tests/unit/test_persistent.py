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
from nose.tools import assert_raises, assert_raises_regexp

from cormoran.persistent import Persistent
from cormoran.fields import StringField, IntegerField


class TestPersistent(unittest.TestCase):
    def test_sets_field_name_if_not_already_setted(self):
        assert_that(User.email.name, is_('email'))

    def test_doesnt_set_field_name_if_already_setted(self):
        assert_that(User.name.name, is_('username'))

    def test_create_fields_dict_with_persistent_fields(self):
        assert_that(User._fields, has_entries({
            'name': User.name,
            'email': User.email
        }))

    def test_without_primary_field_uses_default(self):
        assert_that(User._id.primary)
        assert_that(User._id.name, is_('_id'))
        assert_that(User._id, instance_of(IntegerField))
        assert_that(User._fields, has_entry('_id', User._id))

    def test_with_primary_field_uses_it_and_alias_as_id(self):
        class User(Persistent):
            name = StringField(primary=True)

        assert_that(User._id, is_(User.name))
        assert_that(User._fields, is_not(has_item('_id')))

    def test_with_multiple_primary_raises_value_error(self):
        with assert_raises_regexp(ValueError,
            'Persistent subclasses must have one primary field'):

            class User(Persistent):
                bar = IntegerField(primary=True)
                foo = StringField(primary=True)

    def test_overwrite_default_primary_field_raises_value_error(self):
        with assert_raises_regexp(ValueError,
            'Persistent subclasses must have one primary field'):

            class User(Persistent):
                _id = StringField()

    def test_overwrite_id_field_and_use_another_primary_raises_value_error(self):
        with assert_raises_regexp(ValueError,
            '`_id` attribute can only be overridden by a primary field.'):

            class User(Persistent):
                _id = StringField()
                name = StringField(primary=True)

    def test_overwrite_id_field_with_primary_field_is_ok(self):
        class User(Persistent):
            _id = StringField(primary=True)

        assert_that(User._id, instance_of(StringField))

    def test_overwrite_superclass_id_field_with_primary_field_is_ok(self):
        class FooUser(User):
            _id = StringField(primary=True)

        assert_that(FooUser._id, is_not(User._id))

    def test_subclass_inherits_superclass_fields(self):
        assert_that(FooUser._fields, has_entries({
            '_id': FooUser._id,
            'name': FooUser.name,
            'email': FooUser.email,
            'foo': FooUser.foo
        }))

    def test_subclass_inherits_other_superclass_attributes(self):
        assert_that(FooUser.echo_user, is_(User.echo_user))

    def test_subclass_overwrites_superclass_fields(self):
        class FooUser(User):
            name = IntegerField()

        assert_that(FooUser.name, is_not(User.name))
        assert_that(FooUser._fields,
            has_entry('name', FooUser.name))

    def test_subclass_overwrites_superclass_attributes(self):
        class FooUser(User):
            def echo_user(self):
                return 'foo'

        assert_that(FooUser.echo_user, is_not(User.echo_user))

    def test_instantiate_with_kw_arguments_sets_fields_values(self):
        user = User(name=u'test', email=u'test@example.com')

        assert_that(user.name, is_(u'test'))
        assert_that(user.email, is_(u'test@example.com'))

    def test_instantiate_with_one_kw_argument_sets_these_field_value(self):
        user = User(name=u'test')

        assert_that(user.name, is_(u'test'))
        assert_that(user.email, is_(User.email.default))

    def test_dict_returns_a_fields_values_dict(self):
        user = User(name=u'test')
        assert_that(dict(user), has_entries({u'name': u'test'}))

    def test_persisted_flag_is_false_by_defalt(self):
        assert_that(not User()._persisted)

    def test_persisted_flag_is_instance_independet(self):
        user, another = User(), User()

        user._persisted = True

        assert_that(user._persisted,
            is_not(another._persisted))

    def test_data_store_dict_is_empty_by_default(self):
        user = User()

        assert_that(user._data, instance_of(dict))
        assert_that(user._data, has_length(0))

    def test_data_store_dict_is_instance_independent(self):
        user, another = User(), User()

        user._data['field'] = u'test'

        assert_that(another._data, has_length(0))


class User(Persistent):
    name = StringField(name=u'username')
    email = StringField()

    def echo_user(self):
        return '%s <%s>' % (self.name, self.email)

class FooUser(User):
    foo = IntegerField()
