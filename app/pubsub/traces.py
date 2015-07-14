#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.pubsub import Publisher


class TracesGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('traces_found', repository.all(limit, offset))


class TracesByUserIdGetter(Publisher):
    def perform(self, repository, user_id, limit, offset):
        self.publish('traces_found', repository.all_by_user_id(user_id,
                                                               limit, offset))


class OpenAccountTracesGetter(Publisher):
    def perform(self, traces_repository):
        self.publish('traces_found', traces_repository.all_for_open_account())


def version(trace):
    if trace.app_version is None or trace.app_version == '':
        return (0, 0, 0)
    return tuple([int(v) for v in trace.app_version.split('.')])


class ByAppVersionTracesSorter(Publisher):
    def perform(self, traces):
        self.publish('traces_sorted',
                     sorted(traces, key=version, reverse=True))
