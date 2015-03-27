#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.drive_requests import DriveRequestsRepository
from app.request_decorators import eggauthorized
from app.workflows.drive_requests import ListCompletedDriveRequestsWorkflow


class ListCompletedDriveRequestsController():
    @eggauthorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        drive_requests = ListCompletedDriveRequestsWorkflow()
        ret = Future()

        class ListDriveRequestsSubscriber(object):
            def success(self, drive_requests):
                ret.set(web.ctx.render.
                        completed_drive_requests(drive_requests=drive_requests))

        drive_requests.add_subscriber(logger, ListDriveRequestsSubscriber())
        drive_requests.perform(web.ctx.logger, DriveRequestsRepository,
                               web.input(limit=1000, offset=0))
        return ret.get()
