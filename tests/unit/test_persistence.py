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

from cormoran.persistence import Persistence


class TestPersistence(unittest.TestCase):
    def test_begin_transaction_is_not_implemented(self):
        with assert_raises(NotImplementedError):
            Persistence().begin_transaction()

    def test_commit_transaction_is_not_implemented(self):
        with assert_raises(NotImplementedError):
            Persistence().commit_transaction()

    def test_insert_is_not_implemented(self):
        with assert_raises(NotImplementedError):
            Persistence().insert(object())

