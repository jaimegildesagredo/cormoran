# -*- coding: utf-8 -*-

from cormoran.sql.statements import Select, Update, Delete, Insert


class SQLCompiler(object):
    def select(self, persistent, filters=None, limit=None):
        return Select().compile(persistent, filters, limit)

    def update(self, persistent):
        return Update().compile(persistent)

    def delete(self, persistent):
        return Delete().compile(persistent)

    def insert(self, persistent):
        return Insert().compile(persistent)
