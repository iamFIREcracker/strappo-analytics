#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from app.request_decorators import authorized


class LoginController():
    def GET(self):
        if not web.cookies().get('authorized'):
            return web.ctx.render.login()
        raise web.seeother("/")

    def POST(self):
        data = web.input(secret='')
        if data.secret != web.config.SECRET:
            raise web.unauthorized()

        web.setcookie('authorized', 1, 3600)
        raise web.seeother('/')


class IndexController():
    @authorized
    def GET(self):
        return web.ctx.render.index()
