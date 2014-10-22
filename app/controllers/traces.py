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
        ret = Future()

        class ListTracesSubscriber(object):
            def success(self, traces):
                ret.set(web.ctx.render.traces(traces=traces))

        traces.add_subscriber(logger, ListTracesSubscriber())
        traces.perform(web.ctx.logger, TracesRepository,
                       web.input(limit=1000, offset=0))
        return ret.get()
