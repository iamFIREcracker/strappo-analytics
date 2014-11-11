#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.users import UsersRepository
from app.request_decorators import authorized
from app.workflows.users import ListUsersWorkflow
from app.workflows.users import ListUserVersionsWorkflow


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


class ListUserVersionsController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        users = ListUserVersionsWorkflow()
        ret = Future()

        class ListUserVersionsSubscriber(object):
            def success(self, users):
                ret.set(web.ctx.render.versions(groups=users))

        users.add_subscriber(logger, ListUserVersionsSubscriber())
        users.perform(web.ctx.logger, UsersRepository,
                      web.input(limit=1000, offset=0))
        return ret.get()
