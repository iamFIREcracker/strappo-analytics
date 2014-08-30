#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import web

from . import config


web.config.debug = web.config.DEBUG = config.DEBUG

web.config.DEV = config.DEV

web.config.LOGGER_NAME = config.LOGGER_NAME
web.config.LOG_ENABLE = config.LOG_ENABLE
web.config.LOG_FORMAT = config.LOG_FORMAT

web.config.API_HOST = config.API_HOST



def app_factory():
    """App factory."""
    import weblib.db
    import weblib.gettext
    import weblib.redis
    from app.urls import URLS
    from app.weblib.app_processors import load_logger
    from app.weblib.app_processors import load_path_url
    from app.weblib.app_processors import load_render

    views = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'views')
    app = web.application(URLS, globals())

    app.add_processor(web.loadhook(load_logger))
    app.add_processor(web.loadhook(load_path_url))
    app.add_processor(web.loadhook(load_render(views)))

    return app
