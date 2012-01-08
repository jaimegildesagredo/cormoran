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


class Insert(object):
    def __init__(self, persistent):
        self._persistent = persistent
        self._fields = persistent.__cormoran_fields__

    def __str__(self):
        sql = 'INSERT INTO '
        sql += self.table
        sql += ' (' + ', '.join(self.columns)
        sql += ') VALUES (' + ', '.join('?'*len(self.columns))
        sql += ')'

        return sql

    @property
    def table(self):
        return self._persistent.__cormoran_name__

    @property
    def columns(self):
        return [x.name for x in self._fields.itervalues()]

    @property
    def values(self):
        return [getattr(self._persistent, x) for x in self._fields]

