#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.models import Trace
from app.weblib.db import expunged
from app.weblib.db import joinedload_all


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
