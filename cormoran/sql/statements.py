# -*- coding: utf-8 -*-


class SQLStmt(object):
    def __init__(self, placeholder='?'):
        self.placeholder = placeholder

        self._buffer = []
        self._params = []

    def _assignment(self, field):
        return field.name + '=' + self.placeholder

    def write(self, chunk):
        self._buffer.append(chunk)

    def append(self, params):
        self._params.extend(params)

    def flush(self):
        return ' '.join(self._buffer)


class DMLStmt(SQLStmt):
    def compile_where(self, persistent):
        self.write('WHERE')
        self.write(self._assignment(persistent.__class__._id))
        self.append([getattr(persistent, '_id')])


class Select(SQLStmt):
    def compile(self, persistent, filters=None, limit=None):
        self.write('SELECT')
        self.write(self._columns(persistent._fields))
        self.write('FROM')
        self.write(persistent._collection)

        if filters:
            self.compile_where(persistent._fields, filters)

        if limit:
            self.compile_limit(limit)

        return self.flush(), self._params

    def _columns(self, fields):
        columns = []
        for name, field in fields.iteritems():
            if name != field.name:
                columns.append(field.name + ' AS ' + name)
            else:
                columns.append(name)

        return ', '.join(columns)

    def compile_where(self, fields, filters):
        self.write('WHERE')
        self.write(' AND '.join(self._assignment(fields[x]) for x in filters))
        self.append(filters.values())

    def compile_limit(self, limit):
        if limit.stop:
            self.write('LIMIT')
            self.write(str(limit.stop))
        if limit.start:
            self.write('OFFSET')
            self.write(str(limit.start))


class Update(DMLStmt):
    def compile(self, persistent):
        self.write('UPDATE')
        self.write(persistent._collection)

        self.compile_set(persistent)
        self.compile_where(persistent)

        return self.flush(), self._params

    def compile_set(self, persistent):
        fields = persistent._fields
        self.write('SET')
        self.write(', '.join(self._assignment(x) for x in fields.itervalues()))
        self.append(getattr(persistent, x) for x in persistent._fields)


class Delete(DMLStmt):
    def compile(self, persistent):
        self.write('DELETE FROM')
        self.write(persistent._collection)

        self.compile_where(persistent)

        return self.flush(), self._params


class Insert(SQLStmt):
    def compile(self, persistent):
        self.write('INSERT INTO')
        self.write(persistent._collection)

        self.compile_columns(persistent._fields)
        self.compile_values(persistent)

        return self.flush(), self._params

    def compile_columns(self, fields):
        self.write('(' + ', '.join(x.name for x in fields.itervalues()) + ')')

    def compile_values(self, persistent):
        fields = persistent._fields
        self.write('VALUES (' + ', '.join([self.placeholder]*len(fields)) + ')')
        self.append(getattr(persistent, x) for x in fields)
