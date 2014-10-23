#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.users import UsersGetter


class ListUsersWorkflow(Publisher):
    def perform(self, logger, users_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        users_getter = UsersGetter()

        class TracesGetterSubscriber(object):
            def users_found(self, traces):
                outer.publish('success', traces)

        users_getter.add_subscriber(logger, TracesGetterSubscriber())
        users_getter.\
            perform(users_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
