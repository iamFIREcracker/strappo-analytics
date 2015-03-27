#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.pubsub import LoggingSubscriber
from weblib.pubsub import Publisher

from app.pubsub.drive_requests import CompletedDriveRequestsGetter


class ListCompletedDriveRequestsWorkflow(Publisher):
    def perform(self, logger, drive_requests_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        drive_requests_getter = CompletedDriveRequestsGetter()

        class DriveRequestsGetterSubscriber(object):
            def drive_requests_found(self, drive_requests):
                outer.publish('success', drive_requests)

        drive_requests_getter.add_subscriber(logger,
                                             DriveRequestsGetterSubscriber())
        drive_requests_getter.\
            perform(drive_requests_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
