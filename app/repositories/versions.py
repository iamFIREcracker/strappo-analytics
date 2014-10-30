#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from app.models import Base
from app.models import Trace
from app.weblib.db import expunged

from sqlalchemy import func


VersionEnriched = namedtuple('VersionEnriched', 'app_version active_users'.split())


class VersionsRepository(object):
    @staticmethod
    def _all(limit, offset):
        return (Base.session.query(Trace.app_version,
                                   func.count(func.distinct(Trace.user_id))).
                select_from(Trace).
                group_by(Trace.app_version).
                limit(limit).
                offset(offset))

    @staticmethod
    def all(limit, offset):
        return [VersionEnriched(t[0], t[1])
                for t in VersionsRepository._all(limit, offset)]
