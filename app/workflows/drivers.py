#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.drivers import DriversGetter


class ListDriversWorkflow(Publisher):
    def perform(self, logger, repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        drivers_getter = DriversGetter()

        class DriversGetterSubscriber(object):
            def drivers_found(self, drivers):
                outer.publish('success', drivers)

        drivers_getter.add_subscriber(logger, DriversGetterSubscriber())
        drivers_getter.\
            perform(repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
