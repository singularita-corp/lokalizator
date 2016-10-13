#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from traceback import print_exc
from twisted.internet import reactor
from twisted.internet.threads import blockingCallFromThread

from mhmp.lokalizator.csv import analyze_file
from mhmp.lokalizator.geo import geocode_file
from mhmp.lokalizator.manager import BackendError

import flask
import os

__all__ = ['make_website_app']

def make_website_app(manager, debug):
    """Construct website WSGI application."""

    app = flask.Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.secret_key = os.urandom(16)
    app.debug = debug

    @app.route('/lokalizator/')
    def index():
        return flask.render_template('main.html')


    @app.route('/lokalizator/upload', methods=['POST'])
    def pick_column():
        if 'csv' not in flask.request.files:
            flask.flash(u'Nevybrali jste žádný soubor!')
            return flask.redirect('/lokalizator/')

        data = flask.request.files['csv'].read()
        name = blockingCallFromThread(reactor, manager.store_blob, data, keep=600)
        fp = blockingCallFromThread(reactor, manager.open_blob, name)

        if fp is None:
            flask.flash(u'Nepodařilo se uložit soubor pro zpracování.')
            return flask.redirect('/lokalizator/')

        try:
            head, rows, candidate = analyze_file(fp)
        except:
            print_exc()
            flask.flash(u'Nepodařilo se analyzovat obsah souboru.')
            return flask.redirect('/lokalizator/')

        return flask.render_template('pick-column.html', **locals())

    @app.route('/lokalizator/process', methods=['POST'])
    def process():
        if 'name' not in flask.request.form or \
           'col'  not in flask.request.form:
            flask.flash(u'Co to proboha provádíte?!')
            return flask.redirect('/lokalizator/')

        name = flask.request.form['name']
        col = int(flask.request.form['col'])

        fp = blockingCallFromThread(reactor, manager.open_blob, name)
        if fp is None:
            flask.flash(u'Jejda, soubor tu už není. Příště zkuste sloupec vybrat rychleji...')
            return flask.redirect('/lokalizator/')

        try:
            data = geocode_file(manager, fp, col)
        except BackendError as e:
            print_exc()
            flask.flash(u'Systém pro překlad adres vrátil chybu:\n{}'.format(e.message))
            return flask.redirect('/lokalizator/')
        except:
            print_exc()
            flask.flash(u'Nastala chyba při zpracování souboru. Omlouváme se.')
            return flask.redirect('/lokalizator/')

        resp = flask.make_response(data)
        resp.headers['Content-Type'] = 'text/csv'
        resp.headers['Content-Disposition'] = 'attachment; filename=output.csv'
        return resp


    return app

# vim:set sw=4 ts=4 et:
