#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.models import Driver
from app.weblib.db import expunged
from app.weblib.db import joinedload_all

from sqlalchemy.sql.expression import true


class DriversRepository(object):
    @staticmethod
    def _all(limit, offset):
        options = [joinedload_all('user')]
        return (Driver.query.options(*options).
                filter(Driver.active == true()).
                order_by(Driver.created.desc()).
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [expunged(t, Driver.session)
                for t in DriversRepository._all(limit, offset)]
