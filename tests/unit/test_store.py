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

from cormoran.store import Store


class TestStore(unittest.TestCase):
    def test_add_new_object_adds_it_to_new(self):
        self.store.add(self.persistent)
        assert_that(self.store.new, contains(self.persistent))

    def test_add_already_added_object_doesnt_adds_it(self):
        self.store.add(self.persistent)
        self.store.add(self.persistent)
        assert_that(self.store.new, contains(self.persistent))

    def test_flush_begins_persistence_transaction_if_not_already_begun(self):
        when(self.persistence.transaction).then_return(False)

        self.store.flush()

        assert_that_method(self.persistence.begin_transaction).was_called()

    def test_flush_doesnt_begin_persistence_transaction_is_already_begun(self):
        when(self.persistence.transaction).then_return(True)

        self.store.flush()

        assert_that_method(self.persistence.begin_transaction).was_never_called()

    def test_flush_inserts_new_objects_into_persistence_mechanism(self):
        self.store.add(self.persistent)

        self.store.flush()

        assert_that_method(self.persistence.insert).was_called().with_args(self.persistent)

    def test_commit_flush_and_commits_persistence_transaction(self):
        # TODO: We should test the call to Store.flush method.
        self.store.add(self.persistent)

        self.store.commit()

        assert_that(self.store.new, is_not(contains(self.persistent)))
        assert_that_method(self.persistence.commit_transaction).was_called()

    def setUp(self):
        self.persistent = empty_stub()
        self.persistence = empty_spy()
        self.store = Store(self.persistence)

