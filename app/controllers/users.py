#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from app.repositories.users import UsersRepository
from app.request_decorators import authorized
from app.weblib.pubsub import Future
from app.weblib.pubsub import LoggingSubscriber
from app.workflows.users import ListUsersWorkflow


class ListUsersController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        users = ListUsersWorkflow()
        ret = Future()

        class ListUsersSubscriber(object):
            def success(self, users):
                ret.set(web.ctx.render.users(users=users))

        users.add_subscriber(logger, ListUsersSubscriber())
        users.perform(web.ctx.logger, UsersRepository,
                      web.input(limit=1000, offset=0))
        return ret.get()
