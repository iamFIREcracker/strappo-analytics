#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import Publisher


class UsersGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('users_found', repository.all(limit, offset))
