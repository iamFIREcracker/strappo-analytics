#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from app.models import Base
from app.models import Trace
from app.models import User
from app.weblib.db import expunged

from sqlalchemy import func
from sqlalchemy.sql.expression import false


UserEnriched = namedtuple('UserEnriched', 'user last_active'.split())


class UsersRepository(object):
    @staticmethod
    def _all(limit, offset):
        return (Base.session.query(User,
                                   func.max(Trace.date).label('last_active')).
                select_from(User).
                join('traces').
                filter(User.deleted == false()).
                group_by(User).
                order_by('last_active DESC').
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [UserEnriched(expunged(t[0], User.session), t[1])
                for t in UsersRepository._all(limit, offset)]
