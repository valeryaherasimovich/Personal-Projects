import requests
import json
import textblob
import nltk
import math
import sklearn.metrics
import sklearn.tree
import sklearn.neighbors
import sklearn.neural_network
import sklearn.model_selection
import joblib
#This code will train machine learning models to classify online reviews of products. Some of the reviews will be about hazardous products and the machine learning models will help identify them and most serious product complains.
nltk.download("punkt")
response = requests.get("https://dgoldberg.sdsu.edu/515/appliance_reviews.json")
uniqueWords = []
relevantWords = []
bigList = []
aList = []
if response:
  data = json.loads(response.text)
  for review in data:
    reviewText = review["Review"]
    reviewText = reviewText.lower()
    aList.append(review["Safety hazard"])
    blob = textblob.TextBlob(reviewText)
    words = blob.words
    for word in words:
      if word not in uniqueWords:
        uniqueWords.append(word)
  for word in uniqueWords:
    a = 0
    b = 0
    c = 0
    d = 0
    for review in data:
      reviewText = review["Review"]
      reviewText = reviewText.lower()
      if word in reviewText and review["Safety hazard"] == 1:
        a = a + 1
      elif word in reviewText and review["Safety hazard"] == 0:
        b = b + 1
      elif word not in reviewText and review["Safety hazard"] == 1:
        c = c + 1
      elif word not in reviewText and review["Safety hazard"] == 0:
        d = d + 1
    #Relevance score
    try:
      relevance = (math.sqrt(a + b + c + d) * ((a * d) - (c * b))) / (math.sqrt((a + b) * (c + d)))
    except:
      relevance = 0
    if relevance >= 4000:
      relevantWords.append(word)
  for review in data:
    reviewText = review["Review"]
    reviewText = reviewText.lower()
    myList = []
    for word in relevantWords:
      if word in reviewText:
        myList.append(1)
      else:
        myList.append(0)
    bigList.append(myList)
  #Machine Learning models
  x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(bigList, aList, test_size = 0.2)
  #Decision tree
  dt_clf = sklearn.tree.DecisionTreeClassifier()
  dt_clf = dt_clf.fit(x_train, y_train)
  dt_predictions = dt_clf.predict(x_test)
  dt_accuracy = sklearn.metrics.accuracy_score(y_test, dt_predictions)
  print("Decision Tree Accuracy:", dt_accuracy)
  #K nearest neighbors
  knn_clf = sklearn.neighbors.KNeighborsClassifier(5)
  knn_clf = knn_clf.fit(x_train, y_train)
  knn_predictions = knn_clf.predict(x_test)
  knn_accuracy = sklearn.metrics.accuracy_score(y_test, knn_predictions)
  print("K-Nearest Neighbors Accuracy:", knn_accuracy)
  #Neural network
  nn_clf = sklearn.neural_network.MLPClassifier()
  nn_clf = nn_clf.fit(x_train, y_train)
  nn_predictions = nn_clf.predict(x_test)
  nn_accuracy = sklearn.metrics.accuracy_score(y_test, nn_predictions)
  print("Neural Network Accuracy:", nn_accuracy)

  accuracyList = [dt_accuracy, knn_accuracy, nn_accuracy]
  accuracy = max(accuracyList)
  #Decide which model is performing best and save to file
  if accuracy == dt_accuracy:
    print("Decision Tree model performed best; saved to model.joblib")
    joblib.dump(dt_clf, "model.joblib")
  elif accuracy == knn_accuracy:
    print("K-Nearest Neighbors model performed best; saved to model.joblib")
    joblib.dump(knn_clf, "model.joblib")
  elif accuracy == nn_accuracy:
    print("Neural Network model performed best; saved to model.joblib")
    joblib.dump(nn_clf, "model.joblib")

else:
  print("Sorry, connection lost.")
