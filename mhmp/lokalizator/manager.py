#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from twisted.internet.threads import deferToThread
from twisted.internet import task, reactor

from cStringIO import StringIO
from simplejson import load, dumps
from urllib import urlopen, urlencode
from uuid import uuid4

__all__ = ['Manager']

class Manager(object):
    """The main application logic."""

    def __init__(self, geo_config):
        """Store connection and prepare blob store."""
        self.query = geo_config['query']
        self.blobs = {}


    def store_blob(self, blob, keep=600):
        """Store blob for given period of time under a generated name."""

        name = uuid4().hex
        self.blobs[name] = blob

        reactor.callLater(keep, self.discard_blob, name)

        return name


    def open_blob(self, name):
        try:
            return StringIO(self.blobs[name])
        except KeyError:
            return None


    def discard_blob(self, name):
        try:
            del self.blobs[name]
        except KeyError:
            pass


    def lookup(self, addresses):
        req = {'records': []}

        for i, address in enumerate(addresses):
            req['records'].append({
                'attributes': {
                    'OBJECTID': i,
                    'SingleLine': address,
                },
            })

        data = urlencode({'addresses': dumps(req), 'outSR': '4326', 'f': 'pjson'})
        fp = urlopen(self.query, data)
        resp = load(fp)
        fp.close()

        coords = [None] * len(addresses)

        for loc in resp['locations']:
            rid = loc['attributes']['ResultID']
            lat = loc['location']['y']
            lon = loc['location']['x']
            coords[rid] = (lat, lon)

        return coords


# vim:set sw=4 ts=4 et:
