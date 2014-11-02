#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import true
from weblib.db import func

from app.models import Base
from app.models import DriveRequest
from app.models import User


class DriveRequestsRepository(object):
    @staticmethod
    def rides_given(user_id, start_date, stop_date):
        return (Base.session.query(func.count()).
                select_from(DriveRequest).
                join('driver', 'user').
                filter(User.id == user_id).
                filter(DriveRequest.accepted == true()).
                filter(DriveRequest.created >= start_date).
                filter(DriveRequest.updated < stop_date).
                first())[0]
