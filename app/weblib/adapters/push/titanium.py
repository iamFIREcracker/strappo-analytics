#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2

import web


class TitaniumPushNotificationsAdapter(object):
    """Defines an adapter of the Titanium push notification system."""

    NOTIFY_TOKENS_URL = 'https://api.cloud.appcelerator.com/v1/push_notification/notify_tokens.json?key=%(key)s'

    def notify_tokens(self, channel, tokens, payload):
        url = self.NOTIFY_TOKENS_URL % dict(key=web.config.TITANIUM_KEY)
        data = urllib.urlencode(dict(channel=channel,
                                     to_tokens=','.join(tokens),
                                     payload=payload))
        try:
            response = urllib2.urlopen(url, data)
        except urllib2.HTTPError as e:
            return (None, ('Unable to contact the server', url, data, str(e)))
        else:
            return (response, None)
