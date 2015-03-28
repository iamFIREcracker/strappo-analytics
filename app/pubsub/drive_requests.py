#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.pubsub import Publisher


class CompletedDriveRequestsGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('drive_requests_found', repository.all_completed(limit,
                                                                      offset))
