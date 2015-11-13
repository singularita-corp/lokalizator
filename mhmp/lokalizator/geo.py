#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from twisted.internet import reactor
from twisted.internet.threads import blockingCallFromThread

from itertools import islice
from cStringIO import StringIO
from csv import reader, writer

__all__ = ['geocode_file']


def geocode_file(manager, fp, col):
    r = reader(fp)

    head = r.next()
    rows = list(r)

    head.insert(col + 1, head[col] + ' lon')
    head.insert(col + 1, head[col] + ' lat')

    req = [row[col] for row in rows]
    resp = blockingCallFromThread(reactor, manager.lookup, req)

    for i, row in enumerate(rows):
        lat, lon = resp[i] or ('', '')
        row.insert(col + 1, lon)
        row.insert(col + 1, lat)

    fp = StringIO()
    w = writer(fp)

    for row in [head] + rows:
        w.writerow(row)

    return fp.getvalue()


# vim:set sw=4 ts=4 et:
