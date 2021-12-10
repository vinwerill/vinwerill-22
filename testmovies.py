import os
import sys
import random
import time
import urllib.request
# import xmltodict
import json
from datetime import date, timedelta
from functools import wraps
# from geptdb import GEPTDB
from werkzeug.local import LocalProxy
from flask import Flask, render_template, send_from_directory
from flask import session, request, redirect, url_for, current_app
import utils

app = Flask(__name__)
log = LocalProxy(lambda: current_app.logger)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
# SHA-256 from 'flask20210112'
app.config['SECRET_KEY'] = '18f4173d24f63dd99d2700aad88002c61c864f83255f5c76da4a0002db1f31c4'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
cyear = date.today().year
nowid = lambda: utils.get_nowid()
dtnow = lambda: utils.get_datetime()
# db = GEPTDB()

@app.route('/flaskweb/movies/<act_id>', methods=['GET', 'POST'])
def movies(act_id):
    movies = open(os.path.join(SITE_ROOT, 'templates/flaskweb/movies.json'), encoding='utf-8').read()
    list_movies = json.loads(movies)
    print(list_movies)
    # return render_template('flaskweb/movies.html', nowid=nowid(), act_id=act_id, list_movies=list_movies)
movies(all)