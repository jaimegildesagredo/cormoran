# -*- coding: utf-8 -*-

from urllib import *


class URI(dict):
    def __init__(self, uri):
        super(URI, self).__init__()

        self.schema, uri = splittype(uri)

        uri, self['db'] = splithost(uri)
        self['db'] = self['db'][1:]

        userpass, hostport = splituser(uri)
        if userpass:
            self['user'], self['passwd'] = splitpasswd(userpass)

        if hostport:
            self['host'], self['port'] = splitnport(hostport)
