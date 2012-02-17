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


class BaseField(object):
    def __init__(self, name=None, primary=False, default=None, nullable=True):
        self.name = name
        self.primary = primary
        self.nullable = nullable
        self.default = default if default is None else self.validate(default)

    def __get__(self, instance, owner):
        if instance:
            return instance.__cormoran_data__.get(self.name, self.default)
        return self

    def __set__(self, instance, value):
        instance.__cormoran_data__[self.name] = self._validate(value)

    def _validate(self, value):
        if value is None:
            if not self.nullable:
                raise ValueError()
            return value
        else:
            return self.validate(value)

    def validate(self, value):
        raise NotImplementedError()


class IntegerField(BaseField):
    def validate(self, value):
        return int(value)


class StringField(BaseField):
    def validate(self, value):
        return unicode(value)


class FloatField(BaseField):
    def validate(self, value):
        return float(value)


class BooleanField(BaseField):
    def validate(self, value):
        return bool(value)
