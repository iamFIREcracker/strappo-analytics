#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import Publisher


class DriverPerksGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('perks_found',
                     repository.all_driver_perks(limit, offset))


class PassengerPerksGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('perks_found',
                     repository.all_passenger_perks(limit, offset))
