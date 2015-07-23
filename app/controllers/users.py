#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import web

from weblib.adapters.push.titanium import TitaniumPushNotificationsAdapter
from weblib.pubsub import Future
from weblib.pubsub import LoggingSubscriber
from strappon.repositories.payments import PaymentsRepository
from strappon.repositories.promo_codes import PromoCodesRepository

from app.repositories.users import UsersRepository
from app.request_decorators import authorized
from app.workflows.users import ListUsersWorkflow
from app.workflows.users import ListUserCreditsWorkflow
from app.workflows.users import ListUserRegionsWorkflow
from app.workflows.users import ListUserVersionsWorkflow
from app.workflows.users import RefillUserWorkflow
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


class ListUserCreditsController():
    def GET(self):
        logger = LoggingSubscriber(web.ctx.logger)
        users = ListUserCreditsWorkflow()
        ret = Future()

        class ListUserCreditsSubscriber(object):
            def success(self, users):
                ret.set(web.ctx.render.credits(back=web.ctx.path,
                                               users=users))

        users.add_subscriber(logger, ListUserCreditsSubscriber())
        users.perform(web.ctx.logger, UsersRepository)
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
        users.perform(web.ctx.logger, UsersRepository)
        return ret.get()


class RefillUserController():
    def POST(self):
        logger = LoggingSubscriber(web.ctx.logger)
        params = web.input(user_id='', alert='')
        channel = web.config.TITANIUM_NOTIFICATION_CHANNEL
        refill_user = RefillUserWorkflow()
        send_message = SendMessageToUserWorkflow()
        ret = Future()

        class RefillUserSubscriber(object):
            def not_found(self, name):
                raise ValueError('Promo not found: ' + name)

            def success(self, payment):
                web.ctx.orm.commit()
                send_message.perform(web.ctx.logger,
                                     UsersRepository,
                                     params.user_id,
                                     TitaniumPushNotificationsAdapter(),
                                     channel,
                                     json.dumps({
                                         'channel': channel,
                                         'slot': 'bonus',
                                         'credits': payment.bonus_credits,
                                         'sound': 'default',
                                         'vibrate': True,
                                         'icon': 'notificationicon',
                                         'alert': params.alert,
                                     }))

        class SendMessageToUserSubscriber(object):
            def user_not_found(self, user_id):
                raise web.notfound

            def failure(self, error):
                raise ValueError(error)

            def success(self):
                raise web.seeother(params.back)

        refill_user.add_subscriber(logger, RefillUserSubscriber())
        send_message.add_subscriber(logger, SendMessageToUserSubscriber())
        refill_user.perform(web.ctx.orm, web.ctx.logger,
                            params.user_id, PromoCodesRepository.NEW_USER,
                            PromoCodesRepository,
                            PaymentsRepository)
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
