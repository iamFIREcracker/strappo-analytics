#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import Publisher


class DriversGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('drivers_found', repository.all(limit, offset))
