#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from app import app_factory
from weblib.logging import create_logger


app = app_factory()


def nointernalerror():
    create_logger().exception('Holy shit!')
    raise web.internalerror('Holy shit!')
app.internalerror = nointernalerror

app = app.wsgifunc()
