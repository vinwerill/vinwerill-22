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
import geptdb as geptDB

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

@app.before_request
def before_request():
    if 'DYNO' in os.environ:
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get('is_auth') is None:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
def index():
    login_failed = ''
    if request.method == 'POST':
        # log.info(request.form)
        dict_roles = {
            'general': 'cc2d3eefaac683c8f5b7499459c3675409e3ca75c60eb8048eecb0afa1f345d4',
            'student': '70fbd79510328e4b69838e515763f47cfc31bb83eb39c5cefb18df273f3f6dbe',
            'teacher': '0c827b12d3527f2fc7dbdb0dcc2dce3d41505e9fe78a1e98fcd45adebb140ec5',
        }
        if 'selRole' in request.form and 'txtPassword' in request.form:
            the_role = request.form.get('selRole')
            if the_role in dict_roles and request.form.get('txtPassword') == dict_roles[the_role]:
                session['is_auth'] = True
                session['role_name'] = the_role
                session['account'] = the_role
                return redirect(url_for('home'))
            elif the_role not in dict_roles:
                login_failed = '登入失敗：身份識別錯誤'
            else:
                login_failed = '登入失敗：通行密碼錯誤'
        else:
            return redirect(url_for('denied'))
    return render_template('login-home.html', login_failed=login_failed, cyear=cyear, nowid=nowid())

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/x-icon')

@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'robots.txt', mimetype='text/plain')

@app.route('/denied')
def denied():
    return render_template("denied.html", cyear=cyear, nowid=nowid())

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", cyear=cyear, nowid=nowid()), 404

@app.route('/home')
@login_required
def home():
    # log.info(session)
    return render_template('home.html', cyear=cyear, dtnow=dtnow(), nowid=nowid())

@app.route('/flaskweb')
@login_required
def flaskweb():
    return render_template('flaskweb/flaskweb.html', nowid=nowid())

@app.route('/opendata')
@login_required
def opendata():
    return render_template('opendata/opendata.html', nowid=nowid())

@app.route('/scraper')
@login_required
def scraper():
    from templates.scraper import forexr
    list_banks = []
    for bno, bank in forexr.banks.items():
        get_rate = bank['info']['func']
        bank_name = bank['info']['name']
        # browser = None
        url = get_rate(None, False)
        list_banks.append((bank_name, url))
    return render_template('scraper/scraper.html', nowid=nowid(), list_banks=list_banks)

@app.route('/documents')
@login_required
def documents():
    return render_template('chapters/documents.html', nowid=nowid())

@app.route('/firebase')
@login_required
def firebase():
    return render_template('firebase/firebase.html', nowid=nowid())

@app.route('/heroku')
@login_required
def heroku():
    return render_template('chapters/heroku.html', nowid=nowid())

@app.route('/flaskweb/movies/<act_id>', methods=['GET', 'POST'])
@login_required
def movies(act_id):
    movies = open(os.path.join(SITE_ROOT, 'templates/flaskweb/movies.json'), encoding='utf-8').read()
    list_movies = json.loads(movies)
    return render_template('flaskweb/movies.html', nowid=nowid(), act_id=act_id, list_movies=list_movies)

@app.route('/opendata/cramschool/')
@login_required
def cramschool():
    return render_template('opendata/cramschool.html', nowid=nowid())

@app.route('/opendata/cramschool/<qlimit>', methods=['GET', 'POST'])
@login_required
def cramschoollist(qlimit):
    from templates.opendata import cramschool
    json_data = cramschool.fetch(int(qlimit))
    return {'jsonData':json_data}

@app.route('/opendata/kinmen_tourist_spot/')
@login_required
def kinmen_tourist_spot():
    return render_template('opendata/kinmen_tourist_spot.html', nowid=nowid())

@app.route('/opendata/kinmen_tourist_spot/<qlimit>', methods=['GET', 'POST'])
@login_required
def kinmen_tourist_spotlist(qlimit):
    from templates.opendata import kinmen_tourist_spot
    json_data = kinmen_tourist_spot.fetch(int(qlimit))
    return {'jsonData':json_data[1:-1]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/gept', methods=['GET', 'POST'])
def gept():
    submit_result = ''
    password_hash = '73cd1b16c4fb83061ad18a0b29b9643a68d4640075a466dc9e51682f84a847f5'
    if request.method == 'POST':
        # log.info(request.form)
        if 'txtAccount' in request.form and 'txtPassword' in request.form:
            account = request.form.get('txtAccount')
            password = request.form.get('txtPassword')
            if account == 'admin' and utils.get_sha2(password, 1) == password_hash:
                session['is_auth'] = True
                session['role_name'] = account
            else:
                session['is_auth'] = geptDB.check_examinee(account, password)[0]
                session['role_name'] = 'user'
            # 檢查是否通過登入驗證
            if session.get('is_auth') == True:
                session['account'] = account
                session['portal'] = 'gept'
                return redirect(url_for('gept_sheets'))
            else:
                submit_result = '登入失敗：帳號或密碼錯誤'
        else:
            return redirect(url_for('denied'))
    return render_template('login-gept.html', submit_result=submit_result, cyear=cyear, nowid=nowid())

@app.route('/gept-words')
@login_required
def gept_words():
    return render_template('gept/gept-words.html', nowid=nowid())

@app.route('/gept_words_json/<word_level>', methods=['POST'])
@login_required
def gept_words_json(word_level):
    word_levels = ('w1', 'w2', 'w3')
    if word_level in word_levels:
        wlevel_index = word_levels.index(word_level)
        gept_words = open(os.path.join(app.root_path, 'templates/gept/gept-words.json')).read()
        json_data = json.loads(gept_words)
        return {'jsonData':json_data[wlevel_index]}
    return {'jsonData':''}

@app.route('/gept-sets')
@login_required
def gept_sets():
    gept_settings = geptDB.get_settings()
    return render_template('gept/gept-sets.html', nowid=nowid(), gept_settings=gept_settings,
        type_options=geptDB.type_options, type_questions=geptDB.type_questions)

@app.route('/gept_sets_save', methods=['POST'])
@login_required
def gept_sets_save():
    new_sets = {
        'selOptFB':int(request.form.get('selOptFB')),
        'selQnsFB':int(request.form.get('selQnsFB')),
        'selOptMC':int(request.form.get('selOptMC')),
        'selQnsMC':int(request.form.get('selQnsMC')),
    }
    geptDB.save_settings(**new_sets)
    gept_settings = geptDB.get_settings()
    return {'gept_settings':gept_settings}

@app.route('/gept-tests')
@login_required
def gept_tests():
    gept_settings = geptDB.get_settings()
    gept_examinees = geptDB.get_examinees()
    return render_template('gept/gept-tests.html', nowid=nowid(), gept_settings=gept_settings,
        word_levels=geptDB.word_levels, type_options=geptDB.type_options, type_questions=geptDB.type_questions)

@app.route('/gept_tests_save', methods=['POST'])
@login_required
def gept_tests_save():
    from random import shuffle
    chkw1 = int(request.form.get('chkW1'))
    chkw2 = int(request.form.get('chkW2'))
    chkw3 = int(request.form.get('chkW3'))
    check_wlevel = (chkw1, chkw2, chkw3)
    word_levels = dict(zip(list(geptDB.word_levels.keys()), check_wlevel))
    gept_words = open(os.path.join(app.root_path, 'templates/gept/gept-words.json')).read()
    json_data = json.loads(gept_words)

    # 擷取題型設定
    settings = geptDB.get_settings()
    # 重置測驗
    geptDB.reset_tests()

    for wlevel_index, wlevel in enumerate(word_levels.keys()):
        # 是否依級別設定測驗
        if word_levels[wlevel] == 1:
            list_words = []
            for wl_words in json_data[wlevel_index]:
                list_words.extend(wl_words['words'])
            # 新增測驗
            shuffle(list_words)
            dict_types = {
                'fill_in_the_blank':int(request.form.get('chkFB')),
                'multiple_choice':int(request.form.get('chkMC'))
            }
            geptDB.save_tests(wlevel, 3, list_words, settings, **dict_types)
    return {}

@app.route('/gept_tests_list', methods=['POST'])
@login_required
def gept_tests_list():
    gept_tests = geptDB.get_tests()
    for wlevel, types in gept_tests.items():
        for type_name, test_body in types.items():
            for test_id, questions in test_body.items():
                # 清空題目內容
                gept_tests[wlevel][type_name][test_id] = []
    return {'gept_tests':gept_tests}

@app.route('/gept-examinees')
@login_required
def gept_examinees():
    return render_template('gept/gept-examinees.html', nowid=nowid())

@app.route('/gept_examinees_save', methods=['POST'])
@login_required
def gept_examinees_save():
    examinee = request.form
    if examinee.get('act') == 'Save':
        geptDB.save_examinee(**examinee)
    elif examinee.get('act') == 'Drop':
        geptDB.drop_examinee(**examinee)
    gept_examinees = geptDB.get_examinees()
    return {'gept_examinees':gept_examinees}

@app.route('/gept-scores')
@login_required
def gept_scores():
    return render_template('gept/gept-scores.html', nowid=nowid())

@app.route('/gept-sheets')
@login_required
def gept_sheets():
    return render_template('gept/gept-sheets.html', nowid=nowid())

@app.route('/gept_sheets_read', methods=['POST'])
@login_required
def gept_sheets_read():
    test_args = geptDB.get_test_args(request.form)
    test_sheet = geptDB.read_test(**test_args)
    return {'test_sheet':test_sheet}

@app.route('/gept_sheets_score', methods=['POST'])
@login_required
def gept_sheets_score():
    examinee_id = session['account']
    # log.info(request.form)
    if session['role_name'] == 'user':
        ready_to_check = True
        test_args = geptDB.get_test_args(request.form)
        test_sheet = geptDB.read_test(**test_args)
        test_sheet_count = len(test_sheet)
        test_sheet_right = 0
        for i, question in enumerate(test_sheet):
            quid = 'q'+str(i)
            if quid in request.form:
                if str(question['ans']) == request.form[quid]:
                    # log.info('{}={}'.format(str(question['ans']), request.form[quid]))
                    test_sheet_right += 1
        # 計算分數
        test_sheet_score = int(100 / test_sheet_count * test_sheet_right)
        # 記錄分數
        geptDB.save_score(examinee_id, test_sheet_score, **test_args)
        # 成績列表
        scores_list = geptDB.get_score_examinee(examinee_id)
    else:
        ready_to_check = False
        test_sheet_score = 0
        scores_list = []
    return {'result':ready_to_check, 'score':test_sheet_score, 'scores_list':scores_list}

@app.route('/gept_scores_list_all', methods=['POST'])
@login_required
def gept_scores_list_all():
    gept_scores = geptDB.get_scores()
    return {'gept_scores':gept_scores}

@app.route('/gept_scores_list_examinee', methods=['POST'])
@login_required
def gept_scores_list_examinee():
    examinee_id = session['account']
    result = False
    scores_list = []
    if session['role_name'] == 'admin':
        result = True
    elif session['role_name'] == 'user':
        scores_list = geptDB.get_score_examinee(examinee_id)
        result = True
    return {'result':result, 'scores_list':scores_list}


    
    