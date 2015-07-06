#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.sql.expression import false
from strappon.models import Base
from strappon.models import Trace
from strappon.models import User
from strappon.models import UserPosition
from strappon.repositories.users import UsersRepository as BaseUsersRepository
from weblib.db import expunged


UserEnriched = namedtuple('UserEnriched',
                          'user app_version last_active region'.split())


class UsersRepository(BaseUsersRepository):
    @staticmethod
    def all(limit, offset):
        return all(limit, offset)

    @staticmethod
    def all_acs_ids(limit, offset):
        return all_acs_ids(limit, offset)


def _all(limit, offset):
    return (Base.session.query(User,
                               Trace.app_version,
                               Trace.date,
                               UserPosition.region).
            select_from(User).
            join('traces').
            outerjoin('position').
            filter(User.deleted == false()).
            filter(or_(UserPosition.archived.is_(None),
                       UserPosition.archived == false())).
            order_by(Trace.date.desc()).
            group_by(User.id).
            having(Trace.date == func.max(Trace.date)).
            limit(limit).
            offset(offset))


def all(limit, offset):
    return [UserEnriched(expunged(r[0], User.session), r[1], r[2], r[3])
            for r in _all(limit, offset)]


def _all_acs_ids(limit, offset):
    return (Base.session.query(User.acs_id).
            select_from(User).
            filter(User.deleted == false()).
            limit(limit).
            offset(offset))


def all_acs_ids(limit, offset):
    return [r[0] for r in _all_acs_ids(limit, offset)]
