#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.controllers import IndexController
from app.controllers import LoginController
from app.controllers.drivers import ListDriversController
from app.controllers.feedbacks import ListFeedbacksController
from app.controllers.passengers import ListPassengerDestinationsController
from app.controllers.passengers import ListPassengerOriginsController
from app.controllers.passengers import ListPassengersController
from app.controllers.drive_requests \
    import ListCompletedDriveRequestsController
from app.controllers.perks import ActivateDriverPerkController
from app.controllers.perks import ListPerksController
from app.controllers.perks import ViewDriverEarlyBirdController
from app.controllers.traces import ListTracesController
from app.controllers.users import ListUserRegionsController
from app.controllers.users import ListUserVersionsController
from app.controllers.users import SendMessageToUserController
from app.controllers.users import SendBroadcastMessageController
from app.controllers.users import ListUsersController


URLS = (
    '/login', LoginController,

    '/', IndexController,

    '/drivers', ListDriversController,

    '/feedbacks', ListFeedbacksController,

    '/passengers', ListPassengersController,
    '/passengers/origins', ListPassengerOriginsController,
    '/passengers/destinations', ListPassengerDestinationsController,

    '/perks', ListPerksController,
    '/perks/drivers/(.+)/activate', ActivateDriverPerkController,
    '/perks/drivers/driver_early_bird/view', ViewDriverEarlyBirdController,

    '/traces', ListTracesController,

    '/users', ListUsersController,
    '/users/send_message', SendMessageToUserController,
    '/users/send_message/broadcast', SendBroadcastMessageController,
    '/users/regions', ListUserRegionsController,
    '/users/versions', ListUserVersionsController,

    '/egg', ListCompletedDriveRequestsController,
)
