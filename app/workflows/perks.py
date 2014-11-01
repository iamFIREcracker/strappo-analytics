#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import Future
from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.perks import DriverPerksGetter
from app.pubsub.perks import PassengerPerksGetter


class ListPerksWorkflow(Publisher):
    def perform(self, logger, repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        driver_perks_getter = DriverPerksGetter()
        passenger_perks_getter = PassengerPerksGetter()
        limit = int(params.limit) if params.limit != '' else 1000
        offset = int(params.offset) if params.offset != '' else 0
        driver_perks_future = Future()

        class DriverPerksGetterSubscriber(object):
            def perks_found(self, driver_pekrs):
                driver_perks_future.set(driver_pekrs)
                passenger_perks_getter.perform(repository, limit, offset)

        class PassengerPerksGetterSubscriber(object):
            def perks_found(self, passenger_perks):
                outer.publish('success',
                              driver_perks_future.get(), passenger_perks)

        driver_perks_getter.add_subscriber(logger,
                                           DriverPerksGetterSubscriber())
        passenger_perks_getter.add_subscriber(logger,
                                              PassengerPerksGetterSubscriber())
        driver_perks_getter.perform(repository, limit, offset)
