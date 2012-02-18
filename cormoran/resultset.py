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


class ResultSet(object):
    def __init__(self, persistence, persistent_cls):
        self._persistence = persistence
        self._persistent_cls = persistent_cls

        self._filters = {}
        self._limit = slice(None)

    def __iter__(self):
        results = self._persistence.select(
            self._persistent_cls,
            filters=self._filters,
            limit=self._limit
        )

        for result in results:
            persistent = self._persistent_cls(**result)
            persistent.__cormoran_persisted__ = True
            yield persistent

    def filter(self, **kwargs):
        for k in kwargs:
            if k not in self._persistent_cls.__cormoran_fields__:
                raise ValueError()
            self._filters[k] = kwargs[k]

        return self

    def limit(self, stop):
        self._limit = slice(self._limit.start, stop)
        return self

    def skip(self, start):
        self._limit = slice(start, self._limit.stop or -1)
        return self
