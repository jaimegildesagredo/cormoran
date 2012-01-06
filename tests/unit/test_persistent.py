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

from cormoran.persistent import Persistent
from cormoran.fields import StringField


class TestPersistent(unittest.TestCase):
    def test_sets_field_name_if_not_already_setted(self):
        class User(Persistent):
            login = StringField()

        assert_that(User.login.name, is_('login'))

    def test_doesnt_set_field_name_if_already_setted(self):
        assert_that(self.User.login.name, is_('user_login'))

    def test_create_fields_dict_with_persistent_fields(self):
        assert_that(self.User.__cormoran_fields__,
            has_entries({'login': self.User.login, 'email': self.User.email}))

    def setUp(self):
        class User(Persistent):
            login = StringField(name='user_login')
            email = StringField()

        self.User = User

