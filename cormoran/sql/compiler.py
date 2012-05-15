# -*- coding: utf-8 -*-

from cormoran.sql.statements import Select


class SQLCompiler(object):
    def select(self, persistent, filters=None, limit=None):
        return Select().compile(persistent, filters, limit)
