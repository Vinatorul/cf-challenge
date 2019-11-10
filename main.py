import os
import sys
import datetime
import time
import functools
import hashlib
import random
import secret
import requests
from sqlalchemy import Column, Integer, String, DateTime
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('cf-challange.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
#app.config['SERVER_NAME'] = # NAME
#app.config['SERVER_PORT'] = # Port
db = SQLAlchemy(app)

def print_err(s):
    print(s, file=sys.stderr)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('include/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('include/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('include/fonts', path)

def get_data(cfdata):
    contest = cfdata['contest']
    problems = cfdata['problems']
    problems_count = len(problems)
    rows = cfdata['rows']
    result = 'Информация по контесту ' + contest['name']
    if contest['phase'] == 'FINISHED':
        result += '(Завершен)'
    result += '<table class="table">'
    result += '<tr>'
    result += '<th scope="col">Участник</th>' 
    for i in range(problems_count):
        result += '<th scope="col">' + chr(i + ord("A")) + '</th>'
    result += '<th scope="col">Челлендж</th>'
    result += '</tr>'

    for r in rows:
        result += '<tr>'
        result += '<th scope="row">'
        handle = r['party']['members'][0]['handle']
        result += handle + '\n'
        result += '</td>'
        problem_res = r['problemResults']
        total_solved = 0
        for pr in problem_res:
            result += '<td>'
            if pr['points'] > 0:
                total_solved += 1
                result += '+'
                if pr['rejectedAttemptCount'] > 0:
                    result += str(pr['rejectedAttemptCount'])
            else:
                if pr['rejectedAttemptCount'] > 0:
                    result += '-' + str(pr['rejectedAttemptCount'])
            result += '</td>'
        result += '<td>'
        if total_solved / problems_count > 0.8:
            result += 'выполнен'
        else:
            result += 'не выполнен'
        result += '</td>'
        result += '</tr>'
    result += '</table>'
    return result

@app.route('/', methods = ["GET", "POST"])
def root():
    cfdata = ""
    if request.method == 'POST':
        contestId = request.form['contestId']
        rnd = str(random.randrange(100000, 1000000))
        tm = str(int(time.time()))
        params = ['apiKey=' + secret.cfpubkey, 'contestId=' + str(contestId), 'time=' + tm]
        req = '/contest.standings?'
        hs = rnd + req + '&'.join(params) + '#' + secret.cfsecretkey
        hs = hs.encode('utf-8')
        hs = str(hashlib.sha512(hs).hexdigest())
        ref = "https://codeforces.com/api" + req + "&".join(params)
        ref += '&apiSig=' + rnd + hs
        response = requests.get(ref)
        cfdata = get_data(response.json()['result']) 

    with open('include/index.html', 'r', encoding="utf-8") as page:
        data=page.read()
    data = data.replace('%CF_DATA%', cfdata)
    return data 
