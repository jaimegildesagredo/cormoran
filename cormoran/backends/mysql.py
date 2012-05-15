# -*- coding: utf-8 -*-

from cormoran.persistence import Persistence as Persistence_
from cormoran.sql.compiler import SQLCompiler

import MySQLdb as dbapi2


class Persistence(Persistence_):
    def __init__(self, uri):
        self._connection = dbapi2.connect(**uri)
        self._transaction = False

        self.compiler = SQLCompiler(placeholder='%s')

    def _cursor(self):
        return self._connection.cursor(dbapi2.cursors.DictCursor)

    def begin_transaction(self):
        if not self._transaction:
            self._cursor().execute('START TRANSACTION')
            self._transaction = True

    def commit_transaction(self):
        self._cursor().execute('COMMIT')
        self._transaction = False

    def insert(self, persistent):
        cursor = self._cursor()
        cursor.execute(*self.compiler.insert(persistent))

        return cursor.lastrowid

    def update(self, persistent):
        self._cursor().execute(*self.compiler.update(persistent))

    def delete(self, persistent):
        self._cursor().execute(*self.compiler.delete(persistent))

    def select(self, persistent, filters, limit):
        cursor = self._cursor()
        cursor.execute(
            *self.compiler.select(persistent, filters, limit))
        return cursor
