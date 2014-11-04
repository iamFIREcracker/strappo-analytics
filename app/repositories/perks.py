#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from datetime import date

from sqlalchemy.sql.expression import false
from sqlalchemy.sql.expression import true
from strappon.models import ActiveDriverPerk
from strappon.models import Base
from strappon.models import DriveRequest
from strappon.models import DriverPerk
from strappon.models import EligibleDriverPerk
from strappon.models import PassengerPerk
from strappon.models import User
from weblib.db import and_
from weblib.db import exists
from weblib.db import expunged
from weblib.db import func
from weblib.db import joinedload
from weblib.db import joinedload_all


EnrichedEligibleDriverPerk = namedtuple('EnrichedEligibleDriverPerk',
                                        'perk rides_given'.split())


class PerksRepository(object):
    STANDARD_DRIVER_NAME = 'driver_standard'
    STANDARD_PASSENGER_NAME = 'passenger_standard'
    EARLY_BIRD_DRIVER_NAME = 'driver_early_bird'

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
    def _eligible_driver_perks_with_name(name):
        return (Base.session.query(EligibleDriverPerk).
                options(joinedload_all('user')).
                join('perk').
                join('user').
                filter(EligibleDriverPerk.deleted == false()).
                filter(EligibleDriverPerk.valid_until >= date.today()).
                filter(DriverPerk.name == name).
                filter(~exists().
                       where(and_(ActiveDriverPerk.perk_id ==
                                  EligibleDriverPerk.perk_id,
                                  ActiveDriverPerk.user_id ==
                                  EligibleDriverPerk.user_id))).
                order_by(EligibleDriverPerk.created.desc()).
                group_by(User.id, EligibleDriverPerk.id))

    @staticmethod
    def eligible_driver_perks_with_name(name):
        return [expunged(p, Base.session)
                for p in PerksRepository.
                _eligible_driver_perks_with_name(name)]


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
    print PerksRepository.eligible_driver_perks_with_name('driver_early_bird')
