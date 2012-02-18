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

from cormoran.persistent import Persistent
from cormoran.fields import IntegerField
from cormoran.resultset import ResultSet


class Store(object):
    """The :class:`Store` class."""

    def __init__(self, persistence):
        self.persistence = persistence
        self.new = list()
        self.dirty = list()
        self.deleted = list()

    def add(self, persistent):
        """Adds the :class:`persistent.Persistent` subclass object to
        this :class:`Store`.

        """

        if not isinstance(persistent, Persistent):
            raise TypeError()

        if persistent.__cormoran_persisted__:
            if persistent not in self.dirty:
                self.dirty.append(persistent)
        else:
            if persistent not in self.new:
                self.new.append(persistent)

    def delete(self, persistent):
        if not isinstance(persistent, Persistent):
            raise TypeError()

        if persistent in self.new:
            self.new.remove(persistent)
        elif persistent not in self.deleted:
            self.deleted.append(persistent)

    def find(self, persistent_cls):
        if not issubclass(persistent_cls, Persistent):
            raise TypeError()

        self.flush()

        return ResultSet(self.persistence, persistent_cls)

    def flush(self):
        self.persistence.begin_transaction()

        for persistent in self.new:
            _id = self.persistence.insert(persistent)
            for name, field in persistent.__cormoran_pk__.iteritems():
                if isinstance(field, IntegerField):
                    setattr(persistent, name, getattr(persistent, name) or _id)
            persistent.__cormoran_persisted__ = True

        for persistent in self.dirty:
            self.persistence.update(persistent)

        for persistent in self.deleted:
            self.persistence.delete(persistent)

    def commit(self):
        self.flush()
        self.persistence.commit_transaction()
        self.new = list()
        self.dirty = list()
        self.deleted = list()
