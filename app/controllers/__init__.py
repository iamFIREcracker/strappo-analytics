#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

import json
import urllib
import urllib2

import web


class Trace(object):
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.user_name = data['user_name']
        self.created = data['date']
        self.created_day = data['date'].split('T')[0]
        self.message = data['message']

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

