#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weblib.db import expunged
from weblib.db import joinedload_all

from app.models import Trace


class TracesRepository(object):
    @staticmethod
    def _all(limit, offset):
        options = [joinedload_all('user')]
        return (Trace.query.options(*options).
                order_by(Trace.date.desc()).
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [expunged(t, Trace.session)
                for t in TracesRepository._all(limit, offset)]

    @staticmethod
    def _all_by_user_id(user_id, limit, offset):
        options = [joinedload_all('user')]
        return (Trace.query.options(*options).
                filter_by(user_id=user_id).
                order_by(Trace.date.desc()).
                limit(limit).
                offset(offset))

    @staticmethod
    def all_by_user_id(user_id, limit, offset):
        return [expunged(t, Trace.session)
                for t in TracesRepository._all_by_user_id(user_id,
                                                          limit, offset)]
