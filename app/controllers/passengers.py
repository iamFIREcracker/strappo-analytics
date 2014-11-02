#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.passengers import PassengersRepository
from app.request_decorators import authorized
from app.workflows.passengers import ListPassengersWorkflow
from app.workflows.passengers import ListPassengerDestinationsWorkflow
from app.workflows.passengers import ListPassengerOriginsWorkflow


class ListPassengersController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        passengers = ListPassengersWorkflow()
        ret = Future()

        class ListPassengersSubscriber(object):
            def success(self, passengers):
                ret.set(web.ctx.render.passengers(passengers=passengers))

        passengers.add_subscriber(logger, ListPassengersSubscriber())
        passengers.perform(web.ctx.logger, PassengersRepository,
                           web.input(limit=1000, offset=0))
        return ret.get()


class ListPassengerDestinationsController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        destinations = ListPassengerDestinationsWorkflow()
        ret = Future()

        class ListPassengerDestinationsSubscriber(object):
            def success(self, destinations):
                ret.set(web.ctx.render.destinations(destinations=destinations))

        destinations.add_subscriber(logger,
                                    ListPassengerDestinationsSubscriber())
        destinations.perform(web.ctx.logger, PassengersRepository,
                             web.input(limit=1000, offset=0))
        return ret.get()


class ListPassengerOriginsController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        origins = ListPassengerOriginsWorkflow()
        ret = Future()

        class ListPassengerOriginsSubscriber(object):
            def success(self, origins):
                ret.set(web.ctx.render.origins(origins=origins))

        origins.add_subscriber(logger,
                               ListPassengerOriginsSubscriber())
        origins.perform(web.ctx.logger, PassengersRepository,
                        web.input(limit=1000, offset=0))
        return ret.get()
