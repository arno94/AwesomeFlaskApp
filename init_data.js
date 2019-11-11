use quizApp;

db.quiz.drop();

db.quiz.insertOne({"_id": 0,
  "question": "1+1?",
  "answers":
    [
      "2",
      "3",
      "11"
    ]
});
db.quiz.insertOne({"_id": 1,
  "question": "2+2?",
  "answers":
    [
      "2",
      "3",
      "11"
    ]
});
db.quiz.insertOne({"_id": 2,
  "question": "3+3?",
  "answers":
    [
      "2",
      "3",
      "11"
    ]
});
db.quiz.insertOne({"_id": 3,
  "question": "4+4?",
  "answers":
    [
      "2",
      "3",
      "11"
    ]
});
db.quiz.insertOne({"_id": 4,
  "question": "5+5?",
  "answers":
    [
      "2",
      "3",
      "11"
    ]
});
db.quiz.insertOne({"_id": 5,
  "question": "6+6?",
  "answers":
    [
      "2",
      "3",
      "11"
    ]
});
