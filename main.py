#!/usr/bin/env python3

from flask import Flask, render_template, request
app = Flask(__name__)

import pymongo
import quiz
import sys

conn = pymongo.MongoClient()    # connect to localhost

db = conn['quizApp']    # select database
testCollection = db['quiz']   # select collection
statisticsCollection = db['statistics']
# quiz
# statistics

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods = ['POST','GET'])
def doQuiz():
    quizdata = request.form
    questions = quiz.createQuiz(quizdata)
    print(quizdata,file=sys.stderr)
    currentQuestion = questions[int(quizdata.get("questionNumber"))]
    return render_template('quiz.html',quizdata = quizdata, question = currentQuestion)

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == "__main__":
    app.run(debug=True)    # listen on localhost ONLY
#    app.run(debug=True, host='0.0.0.0')    # listen on all public IPs
