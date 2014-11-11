#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from itertools import groupby

from weblib.pubsub import Publisher


UsersGroup = namedtuple('UsersGroup', 'app_version users'.split())


class UsersGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('users_found', repository.all(limit, offset))


def keyfunc(user):
    if user.app_version is None or user.app_version == '':
        return (0, 0, 0)
    return tuple([int(v) for v in user.app_version.split('.')])


def sort(versions):
    return sorted(versions, key=keyfunc, reverse=True)


def group(users):
    return groupby(users, key=keyfunc)


class ByAppVersionUsersGrouper(Publisher):
    def perform(self, versions):
        self.publish('users_grouped',
                     [UsersGroup(k, list(g))
                      for (k, g) in group(sort(versions))])
