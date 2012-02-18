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


def connect(uri):
    schema, database = uri.split(':///')
    backend = __import__('cormoran.backends.' + schema,
        fromlist=['Persistence'])
    return backend.Persistence(database)


class Persistence(object):
    def begin_transaction(self):
        raise NotImplementedError()

    def commit_transaction(self):
        raise NotImplementedError()

    def insert(self, persistent):
        raise NotImplementedError()
