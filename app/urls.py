#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.controllers import IndexController
from app.controllers import LoginController
from app.controllers.drivers import ListDriversController
from app.controllers.traces import ListTracesController


URLS = (
    '/login', LoginController,

    '/', IndexController,

    '/drivers', ListDriversController,
    '/traces', ListTracesController,
)
