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

web.config.DATABASE_URL = config.DATABASE_URL

web.config.TITANIUM_KEY = config.TITANIUM_KEY
web.config.TITANIUM_LOGIN = config.TITANIUM_LOGIN
web.config.TITANIUM_PASSWORD = config.TITANIUM_PASSWORD
web.config.TITANIUM_NOTIFICATION_CHANNEL = config.TITANIUM_NOTIFICATION_CHANNEL

web.config.SECRET = config.SECRET


def app_factory():
    """App factory."""
    import weblib.db
    import weblib.gettext
    import weblib.redis
    from weblib.app_processors import load_logger
    from weblib.app_processors import load_path_url
    from weblib.app_processors import load_render
    from weblib.app_processors import load_and_manage_orm

    from app.urls import URLS

    views = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'views')
    app = web.application(URLS, globals())

    app.add_processor(web.loadhook(load_logger))
    app.add_processor(web.loadhook(load_path_url))
    app.add_processor(web.loadhook(load_render(views)))
    app.add_processor(load_and_manage_orm(weblib.db.create_session()))

    return app
