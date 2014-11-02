#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.perks import PerksRepository
from app.request_decorators import authorized
from app.workflows.perks import ListPerksWorkflow


class ListPerksController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        perks = ListPerksWorkflow()
        params = web.input(limit=1000, offset=0)
        ret = Future()

        class ListPerksSubscriber(object):
            def success(self, driver_perks, passenger_perks):
                ret.set(web.ctx.render.perks(driver_perks=driver_perks,
                                             passenger_perks=passenger_perks))

        perks.add_subscriber(logger, ListPerksSubscriber())
        perks.perform(web.ctx.logger, PerksRepository, params)
        return ret.get()
