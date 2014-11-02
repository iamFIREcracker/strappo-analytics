#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from weblib.pubsub import Publisher


EnrichedDriverEarlyBirdPerk = namedtuple('EnrichedDriverEarlyBirdPerk',
                                         'perk rides_given'.split())


class DriverPerksGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('perks_found',
                     repository.all_driver_perks(limit, offset))


class EligibleDriverPerksWithNameGetter(Publisher):
    def perform(self, repository, perk_name):
        self.publish('perks_found',
                     repository.eligible_driver_perks_with_name(perk_name))


class DriverErlyBirdPerkEnricher(Publisher):
    def perform(self, drivers_repository, perks):
        self.publish('perks_enriched',
                     [EnrichedDriverEarlyBirdPerk(p,
                                                  drivers_repository.
                                                  rides_given(p.user_id,
                                                              p.created,
                                                              p.valid_until))
                      for p in perks])


class PassengerPerksGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('perks_found',
                     repository.all_passenger_perks(limit, offset))
