#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import web

from weblib.adapters.push.titanium import TitaniumPushNotificationsAdapter
from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber

from app.repositories.users import UsersRepository
from app.request_decorators import authorized
from app.workflows.users import ListUsersWorkflow
from app.workflows.users import ListUserRegionsWorkflow
from app.workflows.users import ListUserVersionsWorkflow
from app.workflows.users import SendMessageToUserWorkflow
from app.workflows.users import SendBroadcastMessageWorkflow


class ListUsersController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        users = ListUsersWorkflow()
        ret = Future()

        class ListUsersSubscriber(object):
            def success(self, users):
                ret.set(web.ctx.render.users(back=web.ctx.path,
                                             users=users))

        users.add_subscriber(logger, ListUsersSubscriber())
        users.perform(web.ctx.logger, UsersRepository,
                      web.input(limit=1000, offset=0))
        return ret.get()


class ListUserRegionsController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        users = ListUserRegionsWorkflow()
        ret = Future()

        class ListUserRegionsSubscriber(object):
            def success(self, users):
                ret.set(web.ctx.render.regions(groups=users))

        users.add_subscriber(logger, ListUserRegionsSubscriber())
        users.perform(web.ctx.logger, UsersRepository,
                      web.input(limit=1000, offset=0))
        return ret.get()


class ListUserVersionsController():
    @authorized
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        users = ListUserVersionsWorkflow()
        ret = Future()

        class ListUserVersionsSubscriber(object):
            def success(self, users):
                ret.set(web.ctx.render.versions(groups=users))

        users.add_subscriber(logger, ListUserVersionsSubscriber())
        users.perform(web.ctx.logger, UsersRepository,
                      web.input(limit=1000, offset=0))
        return ret.get()


class SendMessageToUserController():
    @authorized
    def POST(self):
        logger = LoggingSubscriber(web.ctx.logger)
        send_message = SendMessageToUserWorkflow()
        params = web.input(user_id='', alert='', m_title='', m_text='',
                           back='/')
        channel = web.config.TITANIUM_NOTIFICATION_CHANNEL
        ret = Future()

        class SendMessageToUserSubscriber(object):
            def user_not_found(self, user_id):
                raise web.notfound

            def failure(self, error):
                raise ValueError(error)

            def success(self):
                raise web.seeother(params.back)

        send_message.add_subscriber(logger, SendMessageToUserSubscriber())
        send_message.perform(web.ctx.logger,
                             UsersRepository,
                             params.user_id,
                             TitaniumPushNotificationsAdapter(),
                             channel,
                             json.dumps({
                                 'channel': channel,
                                 'slot': 'global',
                                 'sound': 'default',
                                 'vibrate': True,
                                 'icon': 'notificationicon',
                                 'alert': params.alert,
                                 'm_title': params.m_title,
                                 'm_text': params.m_text
                             }))
        return ret.get()


class SendBroadcastMessageController():
    @authorized
    def POST(self):
        logger = LoggingSubscriber(web.ctx.logger)
        send_message = SendBroadcastMessageWorkflow()
        params = web.input(alert='', m_title='', m_text='', back='/')
        channel = web.config.TITANIUM_NOTIFICATION_CHANNEL
        ret = Future()

        class SendMessageToUserSubscriber(object):
            def failure(self, error):
                raise ValueError(error)

            def success(self):
                raise web.seeother(params.back)

        send_message.add_subscriber(logger, SendMessageToUserSubscriber())
        send_message.perform(web.ctx.logger,
                             UsersRepository,
                             TitaniumPushNotificationsAdapter(),
                             channel,
                             json.dumps({
                                 'channel': channel,
                                 'slot': 'global',
                                 'sound': 'default',
                                 'vibrate': True,
                                 'icon': 'notificationicon',
                                 'alert': params.alert,
                                 'm_title': params.m_title,
                                 'm_text': params.m_text
                             }))
        return ret.get()
