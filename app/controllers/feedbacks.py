#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.feedbacks import FeedbacksRepository
from app.request_decorators import authorized
from app.workflows.feedbacks import ListFeedbacksWorkflow


class ListFeedbacksController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        feedbacks = ListFeedbacksWorkflow()
        ret = Future()

        class ListFeedbacksSubscriber(object):
            def success(self, feedbacks):
                ret.set(web.ctx.render.feedbacks(feedbacks=feedbacks))

        feedbacks.add_subscriber(logger, ListFeedbacksSubscriber())
        feedbacks.perform(web.ctx.logger, FeedbacksRepository,
                          web.input(limit=1000, offset=0))
        return ret.get()
