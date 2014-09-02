#!/usr/bin/env python

import time

import web
from web.session import Store


def _key(key):
    return 'webpy-session:' + key

_sessions = 'webpy-sessions'


class RedisStore(Store):
    def __init__(self, redis):
        self._redis = redis

    def __contains__(self, key):
        return self._redis.exists(_key(key))

    def __getitem__(self, key):
        value = self._redis.hget(_key(key), 'value')
        if value:
            value = self.decode(value)
        self[key] = value
        return value

    def __setitem__(self, key, value):
        atime = time.time()
        self._redis.zadd(_sessions, key, atime)
        self._redis.hmset(_key(key), dict(time=atime,
                                          value=self.encode(value)))

    def __delitem__(self, key):
        self._redis.zrem(_sessions, key)
        self._redis.delete(_key(key))

    def cleanup(self, timeout):
        now = time.time()
        for key in self._redis.zrangebyscore(_sessions, '-inf', now - timeout):
            del self[key]
