#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.pubsub import LoggingSubscriber
from weblib.pubsub import Publisher

from app.pubsub.traces import ByAppVersionTracesSorter
from app.pubsub.traces import OpenAccountTracesGetter


class ViewOpenAccountExperimentWorkflow(Publisher):
    def perform(self, logger, traces_repository):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        traces_getter = OpenAccountTracesGetter()
        traces_sorter = ByAppVersionTracesSorter()

        class TracesGetterSubscriber(object):
            def traces_found(self, traces):
                traces_sorter.perform(traces)

        class TracesSorterSubscriber(object):
            def traces_sorted(self, traces):
                outer.publish('success', traces)

        traces_getter.add_subscriber(logger, TracesGetterSubscriber())
        traces_sorter.add_subscriber(logger, TracesSorterSubscriber())
        traces_getter.perform(traces_repository)
