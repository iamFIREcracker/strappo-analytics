#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.users import UsersGetter
from app.pubsub.users import ByAppVersionUsersGrouper


class ListUsersWorkflow(Publisher):
    def perform(self, logger, users_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        users_getter = UsersGetter()

        class UsersGetterSubscriber(object):
            def users_found(self, users):
                outer.publish('success', users)

        users_getter.add_subscriber(logger, UsersGetterSubscriber())
        users_getter.\
            perform(users_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)


class ListUserVersionsWorkflow(Publisher):
    def perform(self, logger, users_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        users_getter = UsersGetter()
        users_grouper = ByAppVersionUsersGrouper()

        class UsersGetterSubscriber(object):
            def users_found(self, users):
                users_grouper.perform(users)

        class UsersGrouperSubscriber(object):
            def users_grouped(self, users):
                outer.publish('success', users)

        users_getter.add_subscriber(logger, UsersGetterSubscriber())
        users_grouper.add_subscriber(logger, UsersGrouperSubscriber())
        users_getter.\
            perform(users_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
