#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import json
import urllib
import urllib2

import web


class User(object):
    def __init__(self, data):
        self.id = data['id'] if data else ''
        self.name = data['name'] if data else ''

class Trace(object):
    def __init__(self, data):
        self.id = data['id']
        self.created = data['date']
        self.created_day = data['date'] # XXX
        self.user = User(data['user'])

class IndexController():
    TRACES_URL = "http://%(host)s/1/traces?limit=%(limit)s&offset=%(offset)s"
    def GET(self):
        data = web.input(limit=1000, offset=0)
        url = self.TRACES_URL % dict(host=web.config.API_HOST,
                                     limit=data.limit,
                                     offset=data.offset)
        data = json.load(urllib2.urlopen(url))
        traces = [Trace(t) for t in data['traces']]
        return web.ctx.render.traces(traces=traces)

