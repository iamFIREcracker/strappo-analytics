#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from app.models import Base
from app.models import Driver
from app.models import User
from app.models import Trace
from app.weblib.db import expunged
from app.weblib.db import joinedload_all

from sqlalchemy import func
from sqlalchemy.sql.expression import true


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
                group_by(Driver).
                order_by('last_active DESC').
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [DriverEnriched(expunged(t[0], Driver.session), t[1])
                for t in DriversRepository._all(limit, offset)]
