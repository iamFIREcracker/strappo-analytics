#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import false
from sqlalchemy.sql.expression import true
from strappon.models import Base
from strappon.models import DriveRequest
from strappon.models import Passenger
from strappon.models import User
from weblib.db import expunged
from weblib.db import func
from weblib.db import joinedload_all


def _all_completed(limit, offset):
    options = [joinedload_all('driver.user'),
               joinedload_all('passenger.user')]
    return (DriveRequest.query.options(*options).
            filter(DriveRequest.accepted == true()).
            filter(DriveRequest.cancelled == false()).
            filter(DriveRequest.active == false()).
            filter(Passenger.matched == true()).
            order_by(DriveRequest.updated.desc()).
            limit(limit).
            offset(offset))


def all_completed(limit, offset):
    return [expunged(d, DriveRequest.session)
            for d in _all_completed(limit, offset)]


def rides_given(user_id, start_date, stop_date):
    return (Base.session.query(func.count()).
            select_from(DriveRequest).
            join('driver', 'user').
            filter(User.id == user_id).
            filter(DriveRequest.accepted == true()).
            filter(DriveRequest.created >= start_date).
            filter(DriveRequest.updated < stop_date).
            first())[0]


class DriveRequestsRepository(object):

    @staticmethod
    def all_completed(limit, offset):
        return all_completed(limit, offset)

    @staticmethod
    def rides_given(user_id, start_date, stop_date):
        return rides_given(user_id, start_date, stop_date)
