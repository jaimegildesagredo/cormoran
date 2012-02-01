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

from cormoran.fields import BaseField, IntegerField


class PersistentMetaclass(type):
    def __new__(cls, name, bases, attrs):
        cormoran_fields = {}

        for base in bases:
            if hasattr(base, '__cormoran_fields__'):
                cormoran_fields.update(base.__cormoran_fields__)

        if '_id' not in attrs and '_id' not in cormoran_fields:
            attrs['_id'] = IntegerField(primary=True)

        for key, value in attrs.iteritems():
            if isinstance(value, BaseField):
                value.name = value.name or key
                cormoran_fields[key] = value

        attrs['__cormoran_fields__'] = cormoran_fields
        attrs['__cormoran_pk__'] = dict(
            [x for x in cormoran_fields.iteritems() if x[1].primary])

        if not '__cormoran_name__' in attrs:
            attrs['__cormoran_name__'] = name.lower()

        return super(PersistentMetaclass, cls).__new__(cls, name, bases, attrs)


class Persistent(object):
    __metaclass__ = PersistentMetaclass

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

