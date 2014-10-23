#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.traces import TracesByUserIdGetter


class ListTracesWorkflow(Publisher):
    def perform(self, logger, repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        traces_getter = TracesByUserIdGetter()

        class TracesGetterSubscriber(object):
            def traces_found(self, traces):
                outer.publish('success', traces)

        traces_getter.add_subscriber(logger, TracesGetterSubscriber())
        traces_getter.\
            perform(repository,
                    params.user_id,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
