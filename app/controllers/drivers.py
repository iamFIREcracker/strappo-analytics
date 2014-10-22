#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from app.repositories.drivers import DriversRepository
from app.request_decorators import authorized
from app.weblib.pubsub import Future
from app.weblib.pubsub import LoggingSubscriber
from app.workflows.drivers import ListDriversWorkflow


class ListDriversController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        drivers = ListDriversWorkflow()
        ret = Future()

        class ListDriversSubscriber(object):
            def success(self, drivers):
                ret.set(web.ctx.render.drivers(drivers=drivers))

        drivers.add_subscriber(logger, ListDriversSubscriber())
        drivers.perform(web.ctx.logger, DriversRepository,
                        web.input(limit=1000, offset=0))
        return ret.get()
