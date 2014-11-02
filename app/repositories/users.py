#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from sqlalchemy import func
from sqlalchemy.sql.expression import false
from weblib.db import expunged

from app.models import Base
from app.models import Trace
from app.models import User


UserEnriched = namedtuple('UserEnriched',
                          'user app_version last_active'.split())


class UsersRepository(object):
    @staticmethod
    def _all(limit, offset):
        return (Base.session.query(User,
                                   Trace.app_version,
                                   Trace.date).
                select_from(User).
                join('traces').
                filter(User.deleted == false()).
                order_by(Trace.date.desc()).
                group_by(User.id).
                having(Trace.date == func.max(Trace.date)).
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [UserEnriched(expunged(r[0], User.session), r[1], r[2])
                for r in UsersRepository._all(limit, offset)]
