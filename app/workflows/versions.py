#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.versions import VersionsGetter
from app.pubsub.versions import VersionsSorter


class ListVersionsWorkflow(Publisher):
    def perform(self, logger, repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        versions_getter = VersionsGetter()
        versions_sorter = VersionsSorter()

        class VersionsGetterSubscriber(object):
            def versions_found(self, versions):
                versions_sorter.perform(versions)

        class VersionsSorterSubscriber(object):
            def versions_sorted(self, versions):
                outer.publish('success', versions)

        versions_getter.add_subscriber(logger, VersionsGetterSubscriber())
        versions_sorter.add_subscriber(logger, VersionsSorterSubscriber())
        versions_getter.\
            perform(repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
