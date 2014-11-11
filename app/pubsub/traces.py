#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.pubsub import Publisher


class TracesGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('traces_found', repository.all(limit, offset))


class TracesByUserIdGetter(Publisher):
    def perform(self, repository, user_id, limit, offset):
        self.publish('traces_found', repository.all_by_user_id(user_id,
                                                               limit, offset))
