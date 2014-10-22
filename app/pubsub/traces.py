#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import Publisher


class TracesGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('traces_found', repository.all(limit, offset))
