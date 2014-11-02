#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.pubsub import Publisher


class FeedbacksGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('feedbacks_found', repository.all(limit, offset))
