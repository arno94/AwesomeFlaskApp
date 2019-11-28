#!/usr/bin/env python3

import pymongo
import random
import sys
from flask import redirect

from models.question import Question

conn = pymongo.MongoClient()    # connect to localhost

db = conn['quizApp']    # select database
pointsCollection = db['points']

def getAvgScorePercent(username):
    pontok_osszege = getSumOfPoints(username)
    kerdesek_osszege = getNumberOfQuestions(username)
        
    avg_score_percent = (pontok_osszege / kerdesek_osszege) * 100
    avg_score_percent = round(avg_score_percent,2) 
    return avg_score_percent

def getNumberOfQuestions(username):
    kerdesek_osszege = 0
    kerdesek = pointsCollection.find({"username": username},{"_id":0,"questionNumber":1})
    for doc in kerdesek:
        kerdesek_osszege = kerdesek_osszege + doc["questionNumber"]
    return kerdesek_osszege

def getSumOfPoints(username):
    pontok_osszege = 0
    pontok = pointsCollection.find({"username": username},{"_id":0,"points":1})
    for doc in pontok:
        pontok_osszege = pontok_osszege + doc["points"]
    return pontok_osszege
