#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.models import DriverPerk
from app.models import PassengerPerk
from app.weblib.db import expunged
from app.weblib.db import joinedload_all

from sqlalchemy.sql.expression import false


class PerksRepository(object):
    STANDARD_DRIVER_NAME = 'driver_standard'
    STANDARD_PASSENGER_NAME = 'passenger_standard'

    @staticmethod
    def _all_driver_perks(limit, offset):
        return (DriverPerk.query.
                filter(DriverPerk.deleted == false()).
                filter(DriverPerk.name != PerksRepository.STANDARD_DRIVER_NAME).
                order_by(DriverPerk.created.desc()).
                limit(limit).
                offset(offset))

    @staticmethod
    def all_driver_perks(limit, offset):
        return [expunged(r, DriverPerk.session)
                for r in PerksRepository._all_driver_perks(limit, offset)]

    @staticmethod
    def _all_passenger_perks(limit, offset):
        return (PassengerPerk.query.
                filter(PassengerPerk.deleted == false()).
                filter(PassengerPerk.name != PerksRepository.STANDARD_PASSENGER_NAME).
                order_by(PassengerPerk.created.desc()).
                limit(limit).
                offset(offset))

    @staticmethod
    def all_passenger_perks(limit, offset):
        return [expunged(r, PassengerPerk.session)
                for r in PerksRepository._all_passenger_perks(limit, offset)]


if __name__ == '__main__':
    print list(PerksRepository._all_driver_perks(10000, 0))
    print list(PerksRepository._all_passenger_perks(10000, 0))
