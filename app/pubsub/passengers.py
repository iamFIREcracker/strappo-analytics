#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.pubsub import Publisher


class PassengersGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('passengers_found', repository.all(limit, offset))


class PassengerDestinationsGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('destinations_found',
                     repository.destinations(limit, offset))


class PassengerOriginsGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('origins_found', repository.origins(limit, offset))
