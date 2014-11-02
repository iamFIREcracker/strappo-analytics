#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from weblib.db import Boolean
from weblib.db import declarative_base
from weblib.db import relationship
from weblib.db import uuid
from weblib.db import Boolean
from weblib.db import Column
from weblib.db import DateTime
from weblib.db import Float
from weblib.db import ForeignKey
from weblib.db import Integer
from weblib.db import String
from weblib.db import Text
from weblib.db import Time
from weblib.db import text


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(String, default=uuid, primary_key=True)
    acs_id = Column(String)  # XXX Should be not nullable
    facebook_id = Column(String)  # XXX Should be not nullable
    name = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    email = Column(String, nullable=True)
    locale = Column(String, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)

    traces = relationship('Trace', uselist=True, cascade='expunge')

    @property
    def created_day(self):
        return self.created.date()


class Driver(Base):
    __tablename__ = 'driver'

    id = Column(String, default=uuid, primary_key=True)
    user_id = Column(String, ForeignKey('user.id'))
    car_make = Column(String)
    car_model = Column(String)
    car_color = Column(String)
    license_plate = Column(String)
    telephone = Column(String)
    hidden = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)

    user = relationship('User', uselist=False, cascade='expunge')

    @property
    def created_day(self):
        return self.created.date()


class Passenger(Base):
    __tablename__ = 'passenger'

    id = Column(String, default=uuid, primary_key=True)
    user_id = Column(String, ForeignKey('user.id'))
    origin = Column(Text)
    origin_latitude = Column(Float)
    origin_longitude = Column(Float)
    destination = Column(Text)
    destination_latitude = Column(Float)
    destination_longitude = Column(Float)
    distance = Column(Float, nullable=False, server_default=text('0'))
    seats = Column(Integer)
    matched = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)

    user = relationship('User', uselist=False, cascade='expunge')

    @property
    def created_day(self):
        return self.created.date()


class Trace(Base):
    __tablename__ = 'trace'

    id = Column(String, default=uuid, primary_key=True)
    user_id = Column(String, ForeignKey('user.id'))
    app_version = Column(String)
    level = Column(String)
    date = Column(String)
    message = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)

    user = relationship('User', uselist=False)

    @property
    def created_day(self):
        return self.created.date()


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(String, default=uuid, primary_key=True)
    user_id = Column(String, ForeignKey('user.id'))
    message = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)

    user = relationship('User', uselist=False)

    @property
    def created_day(self):
        return self.created.date()


class DriverPerk(Base):
    __tablename__ = 'driver_perk'

    id = Column(String, default=uuid, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False, nullable=False)
    name = Column(String, nullable=False)
    eligible_for = Column(Integer, nullable=False)
    active_for = Column(Integer, nullable=False)
    fixed_rate = Column(Float, nullable=False)
    multiplier = Column(Float, nullable=False)


class EligibleDriverPerk(Base):
    __tablename__ = 'eligible_driver_perk'

    id = Column(String, default=uuid, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False, nullable=False)
    user_id = Column(String, ForeignKey('user.id'), nullable=True)
    perk_id = Column(String, ForeignKey('driver_perk.id'), nullable=True)
    valid_until = Column(DateTime, nullable=False)

    perk = relationship('DriverPerk', uselist=False, cascade='expunge')


class ActiveDriverPerk(Base):
    __tablename__ = 'active_driver_perk'

    id = Column(String, default=uuid, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False, nullable=False)
    user_id = Column(String, ForeignKey('user.id'), nullable=True)
    perk_id = Column(String, ForeignKey('driver_perk.id'), nullable=True)
    valid_until = Column(DateTime, nullable=False)

    perk = relationship('DriverPerk', uselist=False, cascade='expunge')


class PassengerPerk(Base):
    __tablename__ = 'passenger_perk'

    id = Column(String, default=uuid, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False, nullable=False)
    name = Column(String, nullable=False)
    eligible_for = Column(Integer, nullable=False)
    active_for = Column(Integer, nullable=False)
    fixed_rate = Column(Float, nullable=False)
    multiplier = Column(Float, nullable=False)


class EligiblePassengerPerk(Base):
    __tablename__ = 'eligible_passenger_perk'

    id = Column(String, default=uuid, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False, nullable=False)
    user_id = Column(String, ForeignKey('user.id'), nullable=True)
    perk_id = Column(String, ForeignKey('passenger_perk.id'), nullable=True)
    valid_until = Column(DateTime, nullable=False)

    perk = relationship('PassengerPerk', uselist=False, cascade='expunge')


class ActivePassengerPerk(Base):
    __tablename__ = 'active_passenger_perk'

    id = Column(String, default=uuid, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)
    deleted = Column(Boolean, default=False, nullable=False)
    user_id = Column(String, ForeignKey('user.id'), nullable=True)
    perk_id = Column(String, ForeignKey('passenger_perk.id'), nullable=True)
    valid_until = Column(DateTime, nullable=False)

    perk = relationship('PassengerPerk', uselist=False, cascade='expunge')
