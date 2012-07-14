# -*- coding: utf-8 -*-

import time
import logging

from cormoran.persistence import Persistence as Persistence_
from cormoran.sql.compiler import SQLCompiler

import MySQLdb as dbapi2

log = logging.getLogger('cormoran.backend.mysql')


class Persistence(Persistence_):
    def __init__(self, uri):
        self._connection = None
        self._transaction = False
        self._last_use_time = time.time()

        self.uri = uri
        self.compiler = SQLCompiler(placeholder='%s')
        self.connection_recycle = uri.options.get('connection_recycle', 7200)

        self.reconnect()

    def __del__(self):
        self.close()

    def _cursor(self):
        self._ensure_connected()
        return self._connection.cursor(dbapi2.cursors.DictCursor)

    def _ensure_connected(self):
        """Based on the Connection class from tornado.database module.

            http://www.tornadoweb.org/documentation/_modules/tornado/database.html#Connection

        """

        if self._connection is None or \
            time.time() - self._last_use_time > self.connection_recycle:

            self.reconnect()
        self._last_use_time = time.time()

    def reconnect(self):
        self.close()
        self._connection = dbapi2.connect(**self.uri)

        log.debug('Connected to %s', self.uri['db'])

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

            log.debug('Connection closed', self.uri)

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
