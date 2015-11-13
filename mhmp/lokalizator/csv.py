#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from itertools import islice
from csv import reader
from re import match

__all__ = ['analyze_file']


def head_suggests_address(header):
    lower = header.lower()

    for kw in ['adresa', 'addr']:
        if kw in lower:
            return True

    return False

def row_suggests_address(row):
    return match(r'\w+ +\d+/\d+') and True


def shorten(text):
    text = text.decode('utf-8')

    if len(text) > 30:
        return text[:27] + '...'
    else:
        return text


def analyze_file(fp):
    """Extract headers and a few example rows from supplied CSV file."""

    r = reader(fp)

    head = r.next()
    rows = list(islice(r, 0, 5, 1))

    candidate = None

    for i, col in enumerate(head):
        if candidate is None and head_suggests_address(col):
            candidate = i

        head[i] = shorten(col)

    for row in rows:
        for i, col in enumerate(row):
            if candidate is None and row_suggests_address(col):
                candidate = i

            row[i] = shorten(col)

    return head, rows, candidate


# vim:set sw=4 ts=4 et:
