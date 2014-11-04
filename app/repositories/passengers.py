#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from sqlalchemy import func
from sqlalchemy.sql.expression import true
from strappon.models import Base
from strappon.models import Passenger
from strappon.models import User
from strappon.models import Trace
from weblib.db import expunged
from weblib.db import joinedload_all


PassengerEnriched = namedtuple('PassengerEnriched',
                               'passenger last_active'.split())
Destination = namedtuple('Destination', 'name popularity'.split())
Origin = namedtuple('Origin', 'name popularity'.split())


class PassengersRepository(object):
    @staticmethod
    def _all(limit, offset):
        options = [joinedload_all('user')]
        return (Base.session.query(Passenger,
                                   func.max(Trace.date).label('last_active')).
                options(*options).
                select_from(Passenger).
                join('user', 'traces').
                filter(Passenger.active == true()).
                group_by(User.id).
                order_by('last_active DESC').
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [PassengerEnriched(expunged(t[0], Passenger.session), t[1])
                for t in PassengersRepository._all(limit, offset)]

    @staticmethod
    def _destinations(limit, offset):
        return (Base.session.query(Passenger.destination,
                                   func.count().label('popularity')).
                select_from(Passenger).
                group_by(Passenger.destination).
                order_by('popularity DESC').
                limit(limit).
                offset(offset))

    @staticmethod
    def destinations(limit, offset):
        return [Destination(d[0], d[1])
                for d in PassengersRepository._destinations(limit, offset)]

    @staticmethod
    def _origins(limit, offset):
        return (Base.session.query(Passenger.origin,
                                   func.count().label('popularity')).
                select_from(Passenger).
                group_by(Passenger.origin).
                order_by('popularity DESC').
                limit(limit).
                offset(offset))

    @staticmethod
    def origins(limit, offset):
        return [Origin(d[0], d[1])
                for d in PassengersRepository._origins(limit, offset)]
