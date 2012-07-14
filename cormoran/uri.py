# -*- coding: utf-8 -*-

from urllib import *
import urlparse


class URI(dict):
    def __init__(self, uri):
        super(URI, self).__init__()

        self.schema, uri = splittype(uri)
        uri, query = splitquery(uri)

        self.options = URIOptions()
        if query is not None:
            self.options.update(urlparse.parse_qsl(query))

        uri, self['db'] = splithost(uri)
        self['db'] = self['db'][1:]

        userpass, hostport = splituser(uri)
        if userpass:
            self['user'], self['passwd'] = splitpasswd(userpass)

        if hostport:
            self['host'], self['port'] = splitnport(hostport)


class URIOptions(dict):
    def __getitem__(self, key):
        value = dict.__getitem__(self, key)

        try:
            return int(value)
        except ValueError:
            return value

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
