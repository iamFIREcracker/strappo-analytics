#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.passengers import PassengersGetter
from app.pubsub.passengers import PassengerDestinationsGetter
from app.pubsub.passengers import PassengerOriginsGetter


class ListPassengersWorkflow(Publisher):
    def perform(self, logger, passengers_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        passengers_getter = PassengersGetter()

        class PassengersGetterSubscriber(object):
            def passengers_found(self, passengers):
                outer.publish('success', passengers)

        passengers_getter.add_subscriber(logger, PassengersGetterSubscriber())
        passengers_getter.\
            perform(passengers_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)


class ListPassengerDestinationsWorkflow(Publisher):
    def perform(self, logger, passengers_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        destinations_getter = PassengerDestinationsGetter()

        class DestinationsGetterSubscriber(object):
            def destinations_found(self, destination):
                outer.publish('success', destination)

        destinations_getter.add_subscriber(logger,
                                           DestinationsGetterSubscriber())
        destinations_getter.\
            perform(passengers_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)


class ListPassengerOriginsWorkflow(Publisher):
    def perform(self, logger, passengers_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        origins_getter = PassengerOriginsGetter()

        class OriginsGetterSubscriber(object):
            def origins_found(self, passengers):
                outer.publish('success', passengers)

        origins_getter.add_subscriber(logger, OriginsGetterSubscriber())
        origins_getter.\
            perform(passengers_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
