#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask import redirect, url_for, session
import os
app = Flask(__name__)

import pymongo
import quiz
import sys

conn = pymongo.MongoClient()    # connect to localhost

db = conn['quizApp']    # select database
testCollection = db['quiz']   # select collection
statisticsCollection = db['statistics']
usersCollection = db['users']
# quiz
# statistics

quizdata = 0
questions = []
questionIndex = -1

def initData():
    global quizdata
    global questions
    global questionIndex

    quizdata = 0
    questions = []
    questionIndex = -1

@app.route('/', methods = ['POST','GET'])
def login():
    if not session.get("logged_in"):
        return render_template('login.html')
    else:
        return redirect(url_for('index'))

@app.route('/login', methods = ['POST'])
def doLogin():
    name = request.form.get('username')
    password = request.form.get ('password')
    user = {'username': (name), 'password': password }
    if usersCollection.find_one(user):
        session["logged_in"]=True
        session["user_name"] = name
        return render_template('index.html')
    return render_template('login.html')

@app.route('/register', methods = ['POST'])
def doRegister():
    name = request.form.get('username')
    password = request.form.get ('password')
    user = {'username': (name), 'password': password }
    usersCollection.insert_one(user)
    session['logged_in'] = True
    return redirect(url_for('index'))

@app.route('/index', methods = ['POST','GET'])
def index():
    if not session.get("logged_in"):
        return render_template('login.html')
    initData()

    return render_template('index.html')

@app.route('/logout', methods = ['POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

#print(questionCount,file=sys.stderr)

@app.route('/quiz', methods = ['POST','GET'])
def doQuiz():
    if not session.get("logged_in"):
        return render_template('login.html')
    global quizdata
    global questions
    global questionIndex

    if(quizdata == 0):
        quizdata = {'nickname':request.form.get('nickname'),
            'questionCount': int(request.form.get('questionCount')),
            'questionNumber': int(request.form.get('questionNumber'))
        }
        questions = quiz.createQuiz(quizdata)

    questionNumber = int(quizdata.get("questionNumber")) + 1
    if(questionNumber >=  int(quizdata.get("questionCount"))):
        return redirect(url_for('result'))

    quizdata["questionNumber"] =  questionNumber
    currentQuestion = questions[questionNumber]
    return render_template('quiz.html',quizdata = quizdata, question = currentQuestion)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)    # listen on localhost ONLY
#    app.run(debug=True, host='0.0.0.0')    # listen on all public IPs
