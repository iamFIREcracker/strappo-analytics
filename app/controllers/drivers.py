#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

import app.weblib
from app.controllers import ParamAuthorizableController
from app.repositories.drivers import DriversRepository
from app.repositories.drive_requests import DriveRequestsRepository
from app.repositories.passengers import PassengersRepository
from app.tasks import NotifyPassengerDriveRequestPending
from app.tasks import NotifyPassengerDriveRequestCancelledTask
from app.tasks import NotifyPassengersDriverDeactivatedTask
from app.weblib.pubsub import Future
from app.weblib.pubsub import LoggingSubscriber
from app.weblib.request_decorators import api
from app.weblib.request_decorators import authorized
from app.weblib.utils import jsonify
from app.workflows.drivers import AddDriverWorkflow
from app.workflows.drivers import EditDriverWorkflow
from app.workflows.drivers import HideDriverWorkflow
from app.workflows.drivers import DeactivateDriverWorkflow
from app.workflows.drivers import UnhideDriverWorkflow
from app.workflows.drivers import ViewDriverWorkflow
from app.workflows.drive_requests import AddDriveRequestWorkflow
from app.workflows.drive_requests import CancelDriveOfferWorkflow


class AddDriverController(ParamAuthorizableController):
    @api
    @authorized
    def POST(self):
        logger = LoggingSubscriber(web.ctx.logger)
        add_driver = AddDriverWorkflow()
        ret = Future()

        class AddDriverSubscriber(object):
            def invalid_form(self, errors):
                web.ctx.orm.rollback()
                ret.set(jsonify(success=False, errors=errors))
            def success(self, driver_id):
                web.ctx.orm.commit()
                url = '/1/drivers/%(id)s/view' % dict(id=driver_id)
                raise app.weblib.created(url)

        add_driver.add_subscriber(logger, AddDriverSubscriber())
        add_driver.perform(web.ctx.gettext, web.ctx.orm, web.ctx.logger,
                           web.ctx.redis, web.input(), DriversRepository,
                           self.current_user)
        return ret.get()


class DeactivateDriverController(ParamAuthorizableController):
    @api
    @authorized
    def POST(self, driver_id):
        logger = LoggingSubscriber(web.ctx.logger)
        deactivate_driver = DeactivateDriverWorkflow()

        class DeactivateDriverSubscriber(object):
            def not_found(self, driver_id):
                raise web.notfound()
            def unauthorized(self):
                raise web.unauthorized()
            def success(self):
                web.ctx.orm.commit()
                raise web.ok()

        deactivate_driver.add_subscriber(logger,
                                         DeactivateDriverSubscriber())
        deactivate_driver.perform(web.ctx.logger, web.ctx.orm,
                                  DriversRepository, driver_id,
                                  self.current_user,
                                  NotifyPassengersDriverDeactivatedTask)


class CancelDriveOfferController(ParamAuthorizableController):
    @api
    @authorized
    def POST(self, driver_id, drive_request_id):
        logger = LoggingSubscriber(web.ctx.logger)
        cancel_drive_offer = CancelDriveOfferWorkflow()

        class CancelDriveOfferSubscriber(object):
            def not_found(self, driver_id):
                web.ctx.orm.rollback()
                raise web.notfound()
            def unauthorized(self):
                web.ctx.orm.rollback()
                raise web.unauthorized()
            def success(self):
                web.ctx.orm.commit()
                raise app.weblib.nocontent()

        cancel_drive_offer.add_subscriber(logger, CancelDriveOfferSubscriber())
        cancel_drive_offer.perform(web.ctx.orm, web.ctx.logger,
                                   DriversRepository, self.current_user.id,
                                   driver_id, DriveRequestsRepository,
                                   drive_request_id,
                                   NotifyPassengerDriveRequestCancelledTask)


class ViewDriverController(ParamAuthorizableController):
    @api
    @authorized
    def GET(self, driver_id):
        logger = LoggingSubscriber(web.ctx.logger)
        view_driver = ViewDriverWorkflow()
        ret = Future()

        class ViewDriverSubscriber(object):
            def not_found(self, driver_id):
                raise web.notfound()
            def unauthorized(self):
                raise web.unauthorized()
            def success(self, blob):
                ret.set(jsonify(driver=blob))

        view_driver.add_subscriber(logger, ViewDriverSubscriber())
        view_driver.perform(web.ctx.logger, DriversRepository, driver_id,
                            self.current_user.id)
        return ret.get()


class EditDriverController(ParamAuthorizableController):
    @api
    @authorized
    def POST(self, driver_id):
        logger = LoggingSubscriber(web.ctx.logger)
        edit_driver = EditDriverWorkflow()
        ret = Future()

        class EditDriverSubscriber(object):
            def invalid_form(self, errors):
                web.ctx.orm.rollback()
                ret.set(jsonify(success=False, errors=errors))
            def not_found(self, driver_id):
                web.ctx.orm.rollback()
                raise web.notfound()
            def unauthorized(self):
                web.ctx.orm.rollback()
                raise web.unauthorized()
            def success(self):
                web.ctx.orm.commit()
                raise app.weblib.nocontent()

        edit_driver.add_subscriber(logger, EditDriverSubscriber())
        edit_driver.perform(web.ctx.orm, web.ctx.logger, web.input(),
                            DriversRepository, driver_id, self.current_user.id)
        return ret.get()


class HideDriverController(ParamAuthorizableController):
    @api
    @authorized
    def POST(self, driver_id):
        logger = LoggingSubscriber(web.ctx.logger)
        hide_driver = HideDriverWorkflow()

        class HideDriverSubscriber(object):
            def not_found(self, driver_id):
                web.ctx.orm.rollback()
                raise web.notfound()
            def unauthorized(self):
                web.ctx.orm.rollback()
                raise web.unauthorized()
            def success(self):
                web.ctx.orm.commit()
                raise app.weblib.nocontent()

        hide_driver.add_subscriber(logger, HideDriverSubscriber())
        hide_driver.perform(web.ctx.orm, web.ctx.logger, DriversRepository,
                            driver_id, self.current_user.id)


class UnhideDriverController(ParamAuthorizableController):
    @api
    @authorized
    def POST(self, driver_id):
        logger = LoggingSubscriber(web.ctx.logger)
        unhide_driver = UnhideDriverWorkflow()
        ret = Future()

        class UnhideDriverSubscriber(object):
            def invalid_form(self, errors):
                web.ctx.orm.rollback()
                ret.set(jsonify(success=False, errors=errors))
            def not_found(self, driver_id):
                web.ctx.orm.rollback()
                raise web.notfound()
            def unauthorized(self):
                web.ctx.orm.rollback()
                raise web.unauthorized()
            def success(self):
                web.ctx.orm.commit()
                raise app.weblib.nocontent()

        unhide_driver.add_subscriber(logger, UnhideDriverSubscriber())
        unhide_driver.perform(web.ctx.orm, web.ctx.logger, DriversRepository,
                              driver_id, self.current_user.id)
        return ret.get()


class AcceptPassengerController(ParamAuthorizableController):
    @api
    @authorized
    def POST(self, driver_id, passenger_id):
        logger = LoggingSubscriber(web.ctx.logger)
        add_drive_request = AddDriveRequestWorkflow()

        class AddDriveRequestSubscriber(object):
            def not_found(self, driver_id):
                web.ctx.orm.rollback()
                raise web.notfound()
            def unauthorized(self):
                web.ctx.orm.rollback()
                raise web.unauthorized()
            def success(self):
                web.ctx.orm.commit()
                raise app.weblib.nocontent()

        add_drive_request.add_subscriber(logger, AddDriveRequestSubscriber())
        add_drive_request.perform(web.ctx.gettext, web.ctx.orm, web.ctx.logger,
                                  web.input(), self.current_user,
                                  DriversRepository, driver_id,
                                  PassengersRepository, passenger_id,
                                  DriveRequestsRepository,
                                  NotifyPassengerDriveRequestPending)
