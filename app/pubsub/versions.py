#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.weblib.pubsub import Publisher


class VersionsGetter(Publisher):
    def perform(self, repository, limit, offset):
        self.publish('versions_found', repository.all(limit, offset))


def sort(versions):
    def key_extractor(version):
        if version.app_version is None or version.app_version == '':
            return [0, 0, 0]
        return [int(v) for v in version.app_version.split('.')]
    return sorted(versions, key=key_extractor, reverse=True)


class VersionsSorter(Publisher):
    def perform(self, versions):
        self.publish('versions_sorted', sort(versions))


if __name__ == '__main__':
    print sorted((0, 0, 0))
