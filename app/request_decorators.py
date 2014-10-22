#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web


def authorized(func):
    def inner(self, *args, **kw):
        if not web.cookies().get('authorized'):
            raise web.seeother('/login')
        return func(self, *args, **kw)
    return inner
