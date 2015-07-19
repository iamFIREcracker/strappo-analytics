#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import false
from strappon.models import Base
from strappon.models import Payment
from strappon.models import Trace
from strappon.models import User
from strappon.models import UserPosition
from strappon.repositories.users import UsersRepository as BaseUsersRepository
from weblib.db import expunged


UserEnriched = namedtuple('UserEnriched',
                          'user app_version last_active region'.split())

UserWithCredits = namedtuple('UserWithCredits',
                             'user profit_credits profit_bonus_credits loss_credits loss_bonus_credits total_balance'.split())


class UsersRepository(BaseUsersRepository):
    @staticmethod
    def all(limit, offset):
        return all(limit, offset)

    @staticmethod
    def all_acs_ids(limit, offset):
        return all_acs_ids(limit, offset)

    @staticmethod
    def all_with_credits():
        return all_with_credits()


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


def _all_with_credits():
    Profit = aliased(Payment)
    Loss = aliased(Payment)
    return (Base.session.query(User,
                               func.coalesce(func.sum(Profit.credits),
                                             0.0),
                               func.coalesce(func.sum(Profit.bonus_credits),
                                             0.0),
                               func.coalesce(func.sum(Loss.credits),
                                             0.0),
                               func.coalesce(func.sum(Loss.bonus_credits),
                                             0.0)).
            select_from(User).
            outerjoin(Profit, Profit.payee_user_id == User.id).
            outerjoin(Loss, Loss.payer_user_id == User.id).
            filter(User.deleted == false()).
            group_by(User.id))


def all_with_credits():
    def create(row):
        total_balance = row[1] + row[2] - (row[3] + row[4])
        return UserWithCredits(row[0], row[1], row[2], row[3], row[4],
                               total_balance)
    return [create(r) for r in _all_with_credits()]
