#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from app.repositories.versions import VersionsRepository
from app.request_decorators import authorized
from app.weblib.pubsub import Future
from app.weblib.pubsub import LoggingSubscriber
from app.workflows.versions import ListVersionsWorkflow


class ListVersionsController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        versions = ListVersionsWorkflow()
        ret = Future()

        class ListVersionsSubscriber(object):
            def success(self, versions):
                ret.set(web.ctx.render.versions(versions=versions))

        versions.add_subscriber(logger, ListVersionsSubscriber())
        versions.perform(web.ctx.logger, VersionsRepository,
                         web.input(limit=1000, offset=0))
        return ret.get()
