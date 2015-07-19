#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from itertools import groupby

from weblib.pubsub import Publisher


UserAppVersionGroup = namedtuple('UserAppVersionGroup',
                                 'app_version users'.split())
UserRegionGroup = namedtuple('UserRegionGroup', 'region users'.split())


class UsersGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('users_found', repository.all(limit, offset))


class UsersWithCreditsGetter(Publisher):
    def perform(self, repository):
        self.publish('users_found', repository.all_with_credits())


def version(user):
    if user.app_version is None or user.app_version == '':
        return (0, 0, 0)
    return tuple([int(v) for v in user.app_version.split('.')])


class ByAppVersionUsersGrouper(Publisher):
    def perform(self, users):
        self.publish('users_grouped',
                     [UserAppVersionGroup(k, list(g))
                      for (k, g) in groupby(sorted(users,
                                                   key=version,
                                                   reverse=True),
                                            key=version)])


def region(user):
    return user.region


class ByRegionUsersGrouper(Publisher):
    def perform(self, users):
        self.publish('users_grouped',
                     [UserRegionGroup(k, list(g))
                      for (k, g) in groupby(sorted(users,
                                                   key=region),
                                            key=region)])


def total_balance(user):
    return user.total_balance


class ByBalanceUsersSorter(Publisher):
    def perform(self, users):
        self.publish('users_sorted', sorted(users, key=total_balance))


class AllACSIdsGetter(Publisher):
    def perform(self, users_repository, limit, offset):
        self.publish('acs_ids_found',
                     users_repository.all_acs_ids(limit, offset))
