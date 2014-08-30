#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import json
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
    def GET(self):
        url = "http://%s/1/traces" % web.config.API_HOST
        data = json.load(urllib2.urlopen(url))
        traces = [Trace(t) for t in data['traces']]
        return web.ctx.render.traces(traces=traces)

