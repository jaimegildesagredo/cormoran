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
from pyDoubles.framework import *
from nose.tools import assert_raises

from cormoran.store import Store
from cormoran.persistent import Persistent
from cormoran.fields import StringField
from cormoran.resultset import ResultSet


class TestStore(unittest.TestCase):
    def test_add_new_object_adds_it_to_new(self):
        self.store.add(self.persistent)
        assert_that(self.store.new, contains(self.persistent))

    def test_add_already_added_object_doesnt_adds_it(self):
        self.store.add(self.persistent)
        self.store.add(self.persistent)
        assert_that(self.store.new, contains(self.persistent))

    def test_add_various_objects_preserve_order(self):
        item = PersistentClass()
        another = PersistentClass()

        self.store.add(item)
        self.store.add(self.persistent)
        self.store.add(another)

        assert_that(self.store.new, contains(item, self.persistent, another))

    def test_add_no_persistent_subclass_object_raises_type_error(self):
        with assert_raises(TypeError):
            self.store.add(str())

    def test_add_persisted_object_adds_it_to_dirty(self):
        self.persistent.__cormoran_persisted__ = True

        self.store.add(self.persistent)

        assert_that(self.store.dirty, contains(self.persistent))
        assert_that(self.store.new, is_not(contains(self.persistent)))

    def test_add_already_added_persisted_object_doesnt_adds_it(self):
        self.persistent.__cormoran_persisted__ = True

        self.store.add(self.persistent)
        self.store.add(self.persistent)

        assert_that(self.store.dirty, contains(self.persistent))

    def test_delete_persisted_object_adds_it_to_deleted(self):
        self.store.delete(self.persistent)
        assert_that(self.store.deleted, contains(self.persistent))

    def test_delete_already_deleted_object_doesnt_adds_it(self):
        self.store.delete(self.persistent)
        self.store.delete(self.persistent)
        assert_that(self.store.deleted, contains(self.persistent))

    def test_delete_object_in_new_removes_it_from_new(self):
        self.store.add(self.persistent)
        self.store.delete(self.persistent)

        assert_that(self.store.new, is_not(contains(self.persistent)))
        assert_that(self.store.deleted, is_not(contains(self.persistent)))

    def test_delete_various_objects_preserve_order(self):
        item = PersistentClass()
        another = PersistentClass()

        self.store.delete(item)
        self.store.delete(self.persistent)
        self.store.delete(another)

        assert_that(self.store.deleted, contains(item, self.persistent, another))

    def test_delete_no_persistent_subclass_object_raises_type_error(self):
        with assert_raises(TypeError):
            self.store.delete(str())

    def test_find_with_no_persistent_subclass_raises_type_error(self):
        with assert_raises(TypeError):
            self.store.find(str)

    def test_find_flush_and_returns_the_resultset_object(self):
        # TODO: Test that flush method was called.

        result = self.store.find(PersistentClass)

        assert_that(result, instance_of(ResultSet))
        # Using `is_` matcher doesn't work as expected.
        assert_that(result._persistent_cls is PersistentClass)
        assert_that(result._persistence, is_(self.store.persistence))

    def test_flush_calls_begin_transaction_persistence_method(self):
        self.store.flush()

        assert_that_method(self.persistence.begin_transaction).was_called()

    def test_flush_inserts_new_objects_into_persistence_mechanism(self):
        self.store.add(self.persistent)

        self.store.flush()

        assert_that_method(self.persistence.insert).was_called().with_args(self.persistent)

    def test_flush_sets_new_objects_as_persisted(self):
        self.store.add(self.persistent)

        self.store.flush()

        assert_that(self.persistent.__cormoran_persisted__)

    def test_flush_populates_persisted_objects_integer_primary_fields(self):
        when(self.persistence.insert).with_args(self.persistent).then_return(1)

        self.store.add(self.persistent)
        self.store.flush()

        assert_that(self.persistent._id, is_(1))
        assert_that(self.persistent.field, is_not(1))

    def test_flush_doesnt_populates_already_setted_interger_primary_field(self):
        when(self.persistence.insert).with_args(self.persistent).then_return(1)

        self.persistent._id = 2
        self.store.add(self.persistent)
        self.store.flush()

        assert_that(self.persistent._id, is_(2))

    def test_flush_deletes_deleted_objects_from_persistence_mechanism(self):
        self.store.delete(self.persistent)

        self.store.flush()

        assert_that_method(self.persistence.delete).was_called().with_args(self.persistent)

    def test_flush_updates_dirty_objects_in_persistence_mechanism(self):
        self.persistent.__cormoran_persisted__ = True

        self.store.add(self.persistent)
        self.store.flush()

        assert_that_method(self.persistence.update).was_called().with_args(self.persistent)

    def test_commit_flush_and_commits_persistence_transaction(self):
        # TODO: We should test the call to Store.flush method.
        self.store.add(self.persistent)

        self.store.commit()

        assert_that_method(self.persistence.commit_transaction).was_called()

    def test_commit_clears_new_objects_list(self):
        self.store.add(self.persistent)

        self.store.commit()

        assert_that(self.store.new, is_not(contains(self.persistent)))

    def test_commit_clears_deleted_objects_list(self):
        self.store.delete(self.persistent)

        self.store.commit()

        assert_that(self.store.deleted, is_not(contains(self.persistent)))

    def test_commit_clears_dirty_objects_list(self):
        self.persistent.__cormoran_persisted__ = True

        self.store.add(self.persistent)
        self.store.commit()

        assert_that(self.store.dirty, is_not(contains(self.persistent)))

    def setUp(self):
        self.persistent = PersistentClass()
        self.persistence = empty_spy()
        self.store = Store(self.persistence)


class PersistentClass(Persistent):
    field = StringField(primary=True)
