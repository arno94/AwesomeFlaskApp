#!/usr/bin/env python3

from flask import Flask, render_template
app = Flask(__name__)

import pymongo

conn = pymongo.MongoClient()    # connect to localhost

db = conn['quizApp']    # select database
testCollection = db['quiz']   # select collection
statisticsCollection = db['statistics']
# quiz
# statistics


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

if __name__ == "__main__":
    app.run(debug=True)    # listen on localhost ONLY
#    app.run(debug=True, host='0.0.0.0')    # listen on all public IPs
