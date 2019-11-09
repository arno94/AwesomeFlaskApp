#!/usr/bin/env python3

import pymongo
import random
import sys
from flask import redirect

from models.question import Question

#print to console
# print(questionCount,file=sys.stderr)

conn = pymongo.MongoClient()    # connect to localhost

db = conn['quizApp']    # select database
quizCollection = db['quiz']   # select collection
statisticsCollection = db['statistics']

# quiz

# questionData : [questionNumber, questionCount]
def createQuiz(quizdata):
    questionData = [0, int(quizdata["questionCount"])]
    questionIndex = random.sample(range(0, quizCollection.count()), questionData[1])
    questions = []
    for i in questionIndex:
        question = quizCollection.find_one({"_id": i})
        questions.append(Question(question["question"], question["answers"]))
    return questions

def showNextQuestion(questionData, questions):
    questionData[0] = questionData[0] + 1
    question = questions[questionData[0]]
    return [questionData, question]
