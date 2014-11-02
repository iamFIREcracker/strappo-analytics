#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.perks import PerksRepository
from app.repositories.drive_requests import DriveRequestsRepository
from app.request_decorators import authorized
from app.workflows.perks import ListPerksWorkflow
from app.workflows.perks import ViewDriverEarlyBirdWorkflow


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


class ViewDriverEarlyBirdController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        view = ViewDriverEarlyBirdWorkflow()
        ret = Future()

        class ViewPerkSubscriber(object):
            def success(self, eligible_perks):
                ret.set(web.ctx.render.
                        driver_early_bird(back=web.ctx.path,
                                          eligible_perks=eligible_perks))

        view.add_subscriber(logger, ViewPerkSubscriber())
        view.perform(web.ctx.logger, PerksRepository, DriveRequestsRepository,
                     PerksRepository.EARLY_BIRD_DRIVER_NAME)
        return ret.get()
