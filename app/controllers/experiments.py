#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.traces import TracesRepository
from app.request_decorators import authorized
from app.workflows.experiments import ViewOpenAccountExperimentWorkflow


class ViewOpenAccountExperimentController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        view_experiment = ViewOpenAccountExperimentWorkflow()
        ret = Future()

        class ViewOpenAccountExperimentSubscriber(object):
            def success(self, data):
                ret.set(web.ctx.render.open_account(groups=data))

        view_experiment.add_subscriber(logger,
                                       ViewOpenAccountExperimentSubscriber())
        view_experiment.perform(web.ctx.logger, TracesRepository)
        return ret.get()
