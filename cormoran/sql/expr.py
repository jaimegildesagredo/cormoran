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


class BaseExpr(object):
    def __init__(self, persistent):
        self._persistent = persistent
        self._fields = persistent.__cormoran_fields__

    @property
    def table(self):
        return self._persistent.__cormoran_name__

    @property
    def columns(self):
        return [x.name for x in self._fields.itervalues()]

    @property
    def values(self):
        return [getattr(self._persistent, x) for x in self._fields]


class Insert(BaseExpr):

    def __str__(self):
        sql = 'INSERT INTO '
        sql += self.table
        sql += ' (' + ', '.join(self.columns)
        sql += ') VALUES (' + ', '.join('?'*len(self.columns))
        sql += ')'

        return sql


class Update(BaseExpr):
    """UPDATE T SET C1 = 1 WHERE C2 = 'a'"""

    def __init__(self, persistent):
        super(Update, self).__init__(persistent)
        self._pk = persistent.__cormoran_pk__

    @property
    def values(self):
        values = super(Update, self).values
        values.extend([getattr(self._persistent, x) for x in self._pk])
        return values

    def __str__(self):
        sql = 'UPDATE '
        sql += self.table
        sql += ' SET '
        sql += ', '.join(['%s=?' % x.name for x in self._fields.itervalues()])
        sql += ' WHERE '
        sql += ' AND '.join(['%s=?' % x.name for x in self._pk.itervalues()])

        return sql


class Delete(BaseExpr):
    def __init__(self, persistent):
        super(Delete, self).__init__(persistent)
        self._pk = persistent.__cormoran_pk__

    @property
    def values(self):
        return [getattr(self._persistent, x) for x in self._pk]

    def __str__(self):
        sql = 'DELETE FROM '
        sql += self.table
        sql += ' WHERE '
        sql += ' AND '.join(['%s=?' % x.name for x in self._pk.itervalues()])

        return sql


class Select(BaseExpr):
    @property
    def values(self):
        return []

    @property
    def columns(self):
        return []

    def __str__(self):
        sql = 'SELECT * FROM '
        sql += self.table
        return sql
