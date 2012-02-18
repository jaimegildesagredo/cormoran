# -*- coding: utf-8 -*-

from cormoran.persistence import Persistence as Persistence_
from cormoran.fields import IntegerField
from cormoran.sql.statements import Insert, Update, Delete, Select

import sqlite3 as dbapi2


class Persistence(Persistence_):
    def __init__(self, path):
        if path is not None:
            self._connection = dbapi2.connect(path, isolation_level=None)
            self._connection.row_factory = dbapi2.Row
        self._transaction = False

    def _cursor(self):
        return self._connection.cursor()

    def begin_transaction(self):
        if not self._transaction:
            self._cursor().execute('BEGIN TRANSACTION')
            self._transaction = True

    def commit_transaction(self):
        self._cursor().execute('COMMIT')
        self._transaction = False

    def insert(self, persistent):
        cursor = self._cursor().execute(*Insert().compile(persistent))

        return cursor.lastrowid

    def update(self, persistent):
        self._cursor().execute(*Update().compile(persistent))

    def delete(self, persistent):
        self._cursor().execute(*Delete().compile(persistent))

    def select(self, persistent, filters, limit):
        cursor = self._cursor().execute(
            *Select().compile(persistent, filters, limit))
        return cursor
