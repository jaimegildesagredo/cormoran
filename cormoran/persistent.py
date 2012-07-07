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
        super_new = super(PersistentMetaclass, cls).__new__

        parents = [x for x in bases if isinstance(x, PersistentMetaclass)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        fields = {}
        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)

        for key, value in attrs.iteritems():
            if isinstance(value, BaseField):
                value.name = value.name or key
                fields[key] = value

        primary = dict(x for x in fields.iteritems() if x[1].primary)

        if not primary and '_id' not in fields:
            default_primary = IntegerField(name='_id', primary=True)
            primary[default_primary.name] = default_primary
            attrs.update(primary)
            fields.update(primary)

        if len(primary) != 1:
            raise ValueError('Persistent subclasses must have one '
                'primary field')

        if '_id' in fields and '_id' not in primary:
            raise ValueError('`_id` attribute can only be overridden by '
                'a primary field.')

        attrs['_id'] = primary.values()[0]
        attrs['_fields'] = fields

        return super_new(cls, attrs.get('__name__', name), bases, attrs)


class Persistent(object):
    """The :class:`Persistent` class."""

    __metaclass__ = PersistentMetaclass

    def __new__(cls, **kwargs):
        instance = super(Persistent, cls).__new__(cls, **kwargs)
        instance._data = {}
        instance._persisted = False

        return instance

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            if k not in self._fields:
                raise ValueError()
            setattr(self, k, v)

    def __iter__(self):
        return ((x, getattr(self, x)) for x in self._fields)
