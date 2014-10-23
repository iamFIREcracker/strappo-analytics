#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.models import User
from app.weblib.db import expunged
from app.weblib.db import joinedload_all

from sqlalchemy.sql.expression import false


class UsersRepository(object):
    @staticmethod
    def _all(limit, offset):
        options = []
        return (User.query.options(*options).
                filter(User.deleted == false()).
                order_by(User.created.desc()).
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [expunged(t, User.session)
                for t in UsersRepository._all(limit, offset)]
