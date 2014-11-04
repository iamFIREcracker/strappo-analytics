#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from sqlalchemy import func
from sqlalchemy.sql.expression import true
from strappon.models import Base
from strappon.models import Driver
from strappon.models import User
from strappon.models import Trace
from weblib.db import expunged
from weblib.db import joinedload_all


DriverEnriched = namedtuple('DriverEnriched', 'driver last_active'.split())


class DriversRepository(object):
    @staticmethod
    def _all(limit, offset):
        options = [joinedload_all('user')]
        return (Base.session.query(Driver,
                                   func.max(Trace.date).label('last_active')).
                options(*options).
                select_from(Driver).
                join('user', 'traces').
                filter(Driver.active == true()).
                group_by(User.id).
                order_by('last_active DESC').
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [DriverEnriched(expunged(t[0], Driver.session), t[1])
                for t in DriversRepository._all(limit, offset)]
