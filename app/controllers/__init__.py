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
        if data.secret == web.config.SECRET:
            web.setcookie('authorized', 1, 3600)
            raise web.seeother('/')
        elif data.secret == web.config.EGGSECRET:
            web.setcookie('eggauthorized', 1, 3600)
            raise web.seeother('/egg')
        else:
            raise web.unauthorized()


class IndexController():
    @authorized
    def GET(self):
        return web.ctx.render.index()
