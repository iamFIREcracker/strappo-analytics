#!/usr/bin/env python
# -*- coding: utf-8 -*-

from strappon.pubsub import ACSSessionCreator
from strappon.pubsub import ACSUserIdsNotifier
from strappon.pubsub.payments import PaymentForPromoCodeCreator
from strappon.pubsub.promo_codes import PromoCodeWithNameGetter
from strappon.pubsub.promo_codes import PromoCodeActivator
from strappon.pubsub.promo_codes import PromoCodeSerializer
from strappon.pubsub.users import UserWithIdGetter
from strappon.pubsub.users import UsersACSUserIdExtractor
from weblib.pubsub import LoggingSubscriber
from weblib.pubsub import Publisher
from weblib.pubsub import Future

from app.pubsub.users import AllACSIdsGetter
from app.pubsub.users import UsersGetter
from app.pubsub.users import UsersWithCreditsGetter
from app.pubsub.users import ByAppVersionUsersGrouper
from app.pubsub.users import ByBalanceUsersSorter
from app.pubsub.users import ByRegionUsersGrouper


class RefillUserWorkflow(Publisher):
    def perform(self, orm, logger, user_id, name, promo_codes_repository,
                payments_repository):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        promo_code_getter = PromoCodeWithNameGetter()
        promo_code_activator = PromoCodeActivator()
        payment_creator = PaymentForPromoCodeCreator()
        promo_code_future = Future()

        class PromoCodeGetterSubscriber(object):
            def promo_code_not_found(self, name):
                outer.publish('not_found', name)

            def promo_code_found(self, promo_code):
                promo_code_future.set(promo_code)
                promo_code_activator.perform(promo_codes_repository,
                                             user_id, promo_code.id)

        class PromoCodeActivatorSubscriber(object):
            def user_promo_code_activated(self, user_promo_code):
                orm.add(user_promo_code)
                payment_creator.perform(payments_repository,
                                        user_id, promo_code_future.get())

        class PaymentsCreatorSubscriber(object):
            def payment_created(self, payment):
                orm.add(payment)
                outer.publish('success', payment)

        promo_code_getter.add_subscriber(logger,
                                         PromoCodeGetterSubscriber())
        promo_code_activator.add_subscriber(logger,
                                            PromoCodeActivatorSubscriber())
        payment_creator.add_subscriber(logger, PaymentsCreatorSubscriber())
        promo_code_getter.perform(promo_codes_repository, name)


class ListUsersWorkflow(Publisher):
    def perform(self, logger, users_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        users_getter = UsersGetter()

        class UsersGetterSubscriber(object):
            def users_found(self, users):
                outer.publish('success', users)

        users_getter.add_subscriber(logger, UsersGetterSubscriber())
        users_getter.\
            perform(users_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)


class ListUserCreditsWorkflow(Publisher):
    def perform(self, logger, users_repository):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        users_getter = UsersWithCreditsGetter()
        users_sorter = ByBalanceUsersSorter()

        class UsersGetterSubscriber(object):
            def users_found(self, users):
                users_sorter.perform(users)

        class UsersSorterSubscriber(object):
            def users_sorted(self, users):
                outer.publish('success', users)

        users_getter.add_subscriber(logger, UsersGetterSubscriber())
        users_sorter.add_subscriber(logger, UsersSorterSubscriber())
        users_getter.perform(users_repository)


class ListUserRegionsWorkflow(Publisher):
    def perform(self, logger, users_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        users_getter = UsersGetter()
        users_grouper = ByRegionUsersGrouper()

        class UsersGetterSubscriber(object):
            def users_found(self, users):
                users_grouper.perform(users)

        class UsersGrouperSubscriber(object):
            def users_grouped(self, users):
                outer.publish('success', users)

        users_getter.add_subscriber(logger, UsersGetterSubscriber())
        users_grouper.add_subscriber(logger, UsersGrouperSubscriber())
        users_getter.\
            perform(users_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)


class ListUserVersionsWorkflow(Publisher):
    def perform(self, logger, users_repository, params):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        users_getter = UsersGetter()
        users_grouper = ByAppVersionUsersGrouper()

        class UsersGetterSubscriber(object):
            def users_found(self, users):
                users_grouper.perform(users)

        class UsersGrouperSubscriber(object):
            def users_grouped(self, users):
                outer.publish('success', users)

        users_getter.add_subscriber(logger, UsersGetterSubscriber())
        users_grouper.add_subscriber(logger, UsersGrouperSubscriber())
        users_getter.\
            perform(users_repository,
                    int(params.limit) if params.limit != '' else 1000,
                    int(params.offset) if params.offset != '' else 0)


class SendMessageToUserWorkflow(Publisher):
    def perform(self, logger, users_repository, user_id, push_adapter,
                channel, payload):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        user_getter = UserWithIdGetter()
        acs_ids_extractor = UsersACSUserIdExtractor()
        acs_session_creator = ACSSessionCreator()
        acs_notifier = ACSUserIdsNotifier()
        user_ids_future = Future()

        class UserGetterSubscriber(object):
            def user_not_found(self, user_id):
                outer.publish('user_not_found', user_id)

            def user_found(self, user):
                acs_ids_extractor.perform([user])

        class ACSUserIdsExtractorSubscriber(object):
            def acs_user_ids_extracted(self, user_ids):
                user_ids_future.set(user_ids)
                acs_session_creator.perform(push_adapter)

        class ACSSessionCreatorSubscriber(object):
            def acs_session_not_created(self, error):
                outer.publish('failure', error)

            def acs_session_created(self, session_id):
                acs_notifier.perform(push_adapter, session_id, channel,
                                     user_ids_future.get(), payload)

        class ACSNotifierSubscriber(object):
            def acs_user_ids_not_notified(self, error):
                outer.publish('failure', error)

            def acs_user_ids_notified(self):
                outer.publish('success')

        user_getter.add_subscriber(logger, UserGetterSubscriber())
        acs_ids_extractor.add_subscriber(logger,
                                         ACSUserIdsExtractorSubscriber())
        acs_session_creator.add_subscriber(logger,
                                           ACSSessionCreatorSubscriber())
        acs_notifier.add_subscriber(logger, ACSNotifierSubscriber())
        user_getter.perform(users_repository, user_id)


class SendBroadcastMessageWorkflow(Publisher):
    def perform(self, logger, users_repository, push_adapter,
                channel, payload):
        outer = self  # Handy to access ``self`` from inner classes
        logger = LoggingSubscriber(logger)
        acs_ids_getter = AllACSIdsGetter()
        acs_session_creator = ACSSessionCreator()
        acs_notifier = ACSUserIdsNotifier()
        acs_ids_future = Future()

        class ACSIdsGetterSubscriber(object):
            def acs_ids_found(self, acs_ids):
                acs_ids_future.set(acs_ids)
                acs_session_creator.perform(push_adapter)

        class ACSSessionCreatorSubscriber(object):
            def acs_session_not_created(self, error):
                outer.publish('failure', error)

            def acs_session_created(self, session_id):
                acs_notifier.perform(push_adapter, session_id, channel,
                                     acs_ids_future.get(), payload)

        class ACSNotifierSubscriber(object):
            def acs_user_ids_not_notified(self, error):
                outer.publish('failure', error)

            def acs_user_ids_notified(self):
                outer.publish('success')

        acs_ids_getter.add_subscriber(logger, ACSIdsGetterSubscriber())
        acs_session_creator.add_subscriber(logger,
                                           ACSSessionCreatorSubscriber())
        acs_notifier.add_subscriber(logger, ACSNotifierSubscriber())
        acs_ids_getter.perform(users_repository, 1000000, 0)
