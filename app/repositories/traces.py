#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from sqlalchemy import or_
from sqlalchemy import case
from sqlalchemy.sql import func
from strappon.models import Base
from strappon.models import Trace
from weblib.db import expunged
from weblib.db import joinedload_all


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

    @staticmethod
    def all_for_open_account():
        return all_for_open_account()


def _all_for_open_account():
    return (Base.session.query(Trace.app_version,
                               func.count(),
                               func.sum(case([(Trace.message == "app:home.account:click", 1)], else_=0)),
                               func.sum(case([(Trace.message == "app:home_common.user_avatar:click", 1)], else_=0)),
                               func.sum(case([(Trace.message == "app:home_common.user_stars:click", 1)], else_=0)),
                               func.sum(case([(Trace.message == "app:home_common.user_balance:click", 1)], else_=0))).
            filter(or_(Trace.message == "app:home.account:click",
                       Trace.message == "app:home_common.user_avatar:click",
                       Trace.message == "app:home_common.user_stars:click",
                       Trace.message == "app:home_common.user_balance:click")).
            group_by(Trace.app_version))


OpenAccountData = namedtuple('OpenAccountData', 'app_version total nav avatar stars balance'.split())


def all_for_open_account():
    return [OpenAccountData(*d) for d in _all_for_open_account().all()]
