#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from weblib.db import expunged
from weblib.db import joinedload_all

from app.models import Base
from app.models import Feedback


FeedbackEnriched = namedtuple('FeedbackEnriched',
                              'feedback'.split())


class FeedbacksRepository(object):
    @staticmethod
    def _all(limit, offset):
        options = [joinedload_all('user')]
        return (Base.session.query(Feedback).
                options(*options).
                select_from(Feedback).
                join('user').
                order_by(Feedback.created.desc()).
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [FeedbackEnriched(t)
                for t in FeedbacksRepository._all(limit, offset)]
