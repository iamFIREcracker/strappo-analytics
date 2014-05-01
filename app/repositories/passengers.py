#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from app.models import Passenger
from app.models import User
from app.weblib.db import expunged
from app.weblib.db import joinedload


class PassengersRepository(object):
    @staticmethod
    def get(id):
        return expunged(Passenger.query.options(joinedload('user')).\
                                filter(User.deleted == False).\
                                filter(Passenger.id == id).\
                                filter(Passenger.active == True).\
                                first(),
                        Passenger.session)

    @staticmethod
    def copy(other):
        passenger = Passenger(id=other.id,
                              user_id=other.user_id,
                              origin=other.origin,
                              origin_latitude=other.origin_latitude,
                              origin_longitude=other.origin_longitude,
                              destination=other.destination,
                              destination_latitude=other.destination_latitude,
                              destination_longitude=other.destination_longitude,
                              seats=other.seats,
                              matched=other.matched,
                              active=other.active)
        return passenger

    @staticmethod
    def get_all_unmatched():
        return [expunged(p, Passenger.session)
                for p in Passenger.query.options(joinedload('user')).\
                        filter(User.deleted == False).\
                        filter(Passenger.active == True).\
                        filter(Passenger.matched == False)]

    @staticmethod
    def get_all_active():
        return [expunged(p, Passenger.session)
                for p in Passenger.query.options(joinedload('user')).\
                        filter(User.deleted == False).\
                        filter(Passenger.active == True)]

    @staticmethod
    def add(user_id, origin, destination, seats):
        id = unicode(uuid.uuid4())
        passenger = Passenger(id=id, user_id=user_id, origin=origin,
                              destination=destination, seats=seats,
                              matched=False, active=True)
        return passenger

    @staticmethod
    def deactivate(passenger_id):
        passenger = PassengersRepository.get(passenger_id)
        if passenger is None:
            return None
        else:
            passenger.active = False
            return passenger
