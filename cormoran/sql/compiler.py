# -*- coding: utf-8 -*-

from cormoran.sql.statements import Select, Update


class SQLCompiler(object):
    def select(self, persistent, filters=None, limit=None):
        return Select().compile(persistent, filters, limit)

    def update(self, persistent):
        return Update().compile(persistent)
