# -*- coding: utf-8 -*-

from cormoran.sql.statements import Select, Update, Delete, Insert


class SQLCompiler(object):
    def __init__(self, placeholder='?'):
        self.placeholder = placeholder

    def select(self, persistent, filters=None, limit=None):
        return Select(self.placeholder).compile(persistent, filters, limit)

    def update(self, persistent):
        return Update(self.placeholder).compile(persistent)

    def delete(self, persistent):
        return Delete(self.placeholder).compile(persistent)

    def insert(self, persistent):
        return Insert(self.placeholder).compile(persistent)
