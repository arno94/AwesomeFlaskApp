#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask import redirect, url_for, session
import os
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

import pymongo
import quiz
import sys

conn = pymongo.MongoClient() 

db = conn['quizApp'] 
testCollection = db['quiz'] 
usersCollection = db['users']
pointsCollection = db['points']

quizdata = 0
questions = []
questionIndex = -1
answers = []
solved_quiz = 0
avg_score_percent = 0
rank = 0

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
    error = None
    name = request.form['username']
    password = request.form['password']
    user = usersCollection.find_one({'username': request.form['username']})

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_name'] = user['username']
        session["logged_in"]=True

        return render_template('index.html')

    error="Wrong username or password."
    return render_template('login.html',error_log=error)

@app.route('/register', methods = ['POST'])
def doRegister():
    name = request.form.get('username')
    password = request.form.get ('password')
    password_hash = generate_password_hash(password)
    user = {'username': name, 'password': password_hash }
    if usersCollection.find({'username': name}).count() > 0:
        error='Username already in use'
        return render_template('login.html',error_reg=error)
    usersCollection.insert_one(user)
    session['logged_in'] = True
    session["user_name"] = name
    return redirect(url_for('index'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        usersCollection.delete_one({"username" : session["user_name"]})
        pointsCollection.delete_one({"username" : session["user_name"]})
        statisticsCollection.delete_one({"username" : session["user_name"]})
        session.clear()
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
    else:
        questionNumber = int(quizdata.get("questionNumber"))
        currentQuestion = questions[questionNumber]
        myAnswer = request.form.get('answer')
        answers.append(myAnswer == currentQuestion.correct_answer)

    questionNumber = int(quizdata.get("questionNumber")) + 1
    if(questionNumber >=  int(quizdata.get("questionCount"))):
        return redirect(url_for('result'))

    quizdata["questionNumber"] =  questionNumber
    currentQuestion = questions[questionNumber]
    return render_template('quiz.html',quizdata = quizdata, question = currentQuestion)

@app.route('/result')
def result():
    points = sum(answers)

    solved_quiz = pointsCollection.find({"username" : session["user_name"]}).count() + 1
    session["solved_quiz"] = solved_quiz
    
    name = session["user_name"]

    test = {'username': name, 'points': points,'questionNumber': int(quizdata.get("questionNumber"))+1 }
    pointsCollection.insert_one(test)
    answers.clear()

    pontok_osszege = 0
    pontok = pointsCollection.find({"username": session["user_name"]},{"_id":0,"points":1})
    for doc in pontok:
        pontok_osszege = pontok_osszege + doc["points"]
    
    kerdesek_osszege = 0
    kerdesek = pointsCollection.find({"username": session["user_name"]},{"_id":0,"questionNumber":1})
    for doc in kerdesek:
        kerdesek_osszege = kerdesek_osszege + doc["questionNumber"]
        
    avg_score_percent = (pontok_osszege / kerdesek_osszege) * 100
    avg_score_percent = round(avg_score_percent,2) 
    session["avg_score_percent"] = avg_score_percent

    return render_template('result.html', answers = answers, points = points)

@app.route('/statistics',methods = ['POST'])
def statistics():
    return render_template('statistics.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)    # listen on localhost ONLY
#    app.run(debug=True, host='0.0.0.0')    # listen on all public IPs
