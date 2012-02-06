# -*- coding: utf-8 -*-

from cormoran.persistence import Persistence as Persistence_
from cormoran.fields import IntegerField
from cormoran.sql.expr import Insert, Update, Delete

import sqlite3 as dbapi2


class Persistence(Persistence_):
    def __init__(self, path):
        if path is not None:
            self._connection = dbapi2.connect(path, isolation_level=None)
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
        insert = Insert(persistent)

        cursor = self._cursor().execute(str(insert), insert.values)

        return cursor.lastrowid

    def update(self, persistent):
        update = Update(persistent)
        self._cursor().execute(str(update), update.values)

    def delete(self, persistent):
        delete = Delete(persistent)
        self._cursor().execute(str(delete), delete.values)
