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

from cormoran.sql.statements import SQLStmt


class TestSQLStmt(unittest.TestCase):
    def test_write_append_chunk_to_buffer(self):
        self.stmt.write(u'test')

        assert_that(self.stmt._buffer, contains(u'test'))

    def test_flush_returns_concatenated_buffer(self):
        self.stmt.write(u'test')

        assert_that(self.stmt.flush(), is_(u'test'))

    def test_flush_returns_concatenated_buffer_separated_by_space(self):
        self.stmt.write(u'test')
        self.stmt.write(u'another')

        assert_that(self.stmt.flush(), is_(u'test another'))

    def test_append_adds_arguments_to_params(self):
        self.stmt.append([1, 2])

        assert_that(self.stmt._params, contains(1, 2))

    def test_write_and_append_preserves_insertion_order(self):
        self.stmt.write(u'test')
        self.stmt.append([1, 2])
        self.stmt.write(u'another')
        self.stmt.append([0])

        assert_that(self.stmt.flush(), is_('test another'))
        assert_that(self.stmt._params, contains(1, 2, 0))

    def setUp(self):
        self.stmt = SQLStmt()
