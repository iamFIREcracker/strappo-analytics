#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from app.repositories.traces import TracesRepository
from app.request_decorators import authorized
from app.weblib.pubsub import Future
from app.weblib.pubsub import LoggingSubscriber
from app.workflows.traces import ListTracesWorkflow


class ListTracesController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        traces = ListTracesWorkflow()
        params = web.input(user_id='', limit=1000, offset=0)
        ret = Future()

        class ListTracesSubscriber(object):
            def success(self, traces):
                ret.set(web.ctx.render.traces(user_id=params.user_id,
                                              traces=traces))

        traces.add_subscriber(logger, ListTracesSubscriber())
        traces.perform(web.ctx.logger, TracesRepository, params)
        return ret.get()
