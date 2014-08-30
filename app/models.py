#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from app.weblib.db import Boolean
from app.weblib.db import declarative_base
from app.weblib.db import relationship
from app.weblib.db import uuid
from app.weblib.db import Boolean
from app.weblib.db import Column
from app.weblib.db import DateTime
from app.weblib.db import Float
from app.weblib.db import ForeignKey
from app.weblib.db import Integer
from app.weblib.db import String
from app.weblib.db import Text
from app.weblib.db import Time
from app.weblib.db import text



Base = declarative_base()


class Trace(Base):
    __tablename__ = 'trace'

    id = Column(String, default=uuid, primary_key=True)
    user_id = Column(String)
    level = Column(String)
    date = Column(String)
    message = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow,
                     onupdate=datetime.utcnow)

    @property
    def created_day(self):
        return self.created.date()

    def __repr__(self):
        data = u'<Trace id=%(id)s, user_id=%(user_id)s, '\
                'level=%(level)s, date=%(date)s, '\
                'message=%(message)s>' % self.__dict__
        return data.encode('utf-8')


