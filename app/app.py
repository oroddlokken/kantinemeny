#!/usr/bin/env python3

import os.path
import json
import time
from datetime import datetime

from flask import Flask, render_template, jsonify, request

from kantinemeny import Kantinemeny, Cafeterias

app = Flask(__name__)


# Cache menus, by default they are cached for 300 seconds
MENU_VALID_TIME = 300
menus = {}
cafeterias_map = Cafeterias("fetch")

day_map = {
    'Monday': 'mandag',
    'Tuesday': 'tirsdag',
    'Wednesday': 'onsdag',
    'Thursday': 'torsdag',
    'Friday': 'fredag',
    'Saturday': 'lørdag',
    'Sunday': 'søndag'
}


class Stats(object):
    startup = time.time()
    visits = {
        "api": 0,
        "page": 0
    }


def get_menu(location, filename):
    timestamp = time.time()

    if not menus.get(location, None) or (
            timestamp - menus[location].timestamp >= MENU_VALID_TIME):
        try:
            menus[location] = Kantinemeny(location, filename)
        except BaseException:
            if not menus.get(location, None):
                raise

    return menus[location]


@app.route('/kantiner/')
def cafeterias():
    return render_template("kantiner.html",
                           cafeterias_map=cafeterias_map.list)


@app.route('/', defaults={'shortname': 'nostegaten58'})
@app.route('/api/', defaults={'shortname': 'nostegaten58',
                              'json_response': True})
@app.route('/<shortname>/')
@app.route('/api/<shortname>/', defaults={'json_response': True})
def index(shortname, json_response=False):
    location = cafeterias_map[shortname.lower()]

    location_name = location["location"]
    filename = location["filename"]

    menu = get_menu(location_name, filename)

    dt = datetime.now()
    menu_age = dt.timestamp() - menu.timestamp

    if json_response:
        dt = datetime.now()
        dayname_eng = dt.strftime("%A")
        return jsonify({'supper': menu.soups,
                        'varmmat': menu.hot_dishes,
                        'dager': menu.days,
                        'meny_sist_sjekket_siden_i_sekunder': menu_age,
                        'meny': menu.filename,
                        'dagnavn': day_map[dayname_eng]
                        })

    return render_template('index.html',
                           location_name=location_name,
                           menu=menu,
                           start=Stats.startup,
                           shortname=shortname,
                           visitor_ip=request.remote_addr,
                           fetched='{0:.2f}'.format(menu_age))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Launch a local test '
                                     'Flask server with debugging.')
    parser.add_argument('-p', '--port', dest='port', type=int, default=5753,
                        help='Specify the port the interface instance should '
                        'listen on. Default: 5753')
    parser.add_argument('-i', '--bind', dest='host', default='0.0.0.0',
                        help='Specify the IP the instance should '
                        'listen on. Default: 0.0.0.0')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True, threaded=True)
