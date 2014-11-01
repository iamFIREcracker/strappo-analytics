#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import LoggingSubscriber
from app.weblib.pubsub import Publisher

from app.pubsub.feedbacks import FeedbacksGetter


class ListFeedbacksWorkflow(Publisher):
    def perform(self, logger, feedbacks_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        feedbacks_getter = FeedbacksGetter()

        class FeedbacksGetterSubscriber(object):
            def feedbacks_found(self, feedbacks):
                outer.publish('success', feedbacks)

        feedbacks_getter.add_subscriber(logger, FeedbacksGetterSubscriber())
        feedbacks_getter.\
            perform(feedbacks_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)
