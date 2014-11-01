#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.controllers import IndexController
from app.controllers import LoginController
from app.controllers.drivers import ListDriversController
from app.controllers.feedbacks import ListFeedbacksController
from app.controllers.passengers import ListPassengerDestinationsController
from app.controllers.passengers import ListPassengerOriginsController
from app.controllers.passengers import ListPassengersController
from app.controllers.traces import ListTracesController
from app.controllers.users import ListUserVersionsController
from app.controllers.users import ListUsersController


URLS = (
    '/login', LoginController,

    '/', IndexController,

    '/drivers', ListDriversController,

    '/feedbacks', ListFeedbacksController,

    '/passengers', ListPassengersController,
    '/passengers/origins', ListPassengerOriginsController,
    '/passengers/destinations', ListPassengerDestinationsController,

    '/traces', ListTracesController,

    '/users', ListUsersController,
    '/users/versions', ListUserVersionsController,
)
