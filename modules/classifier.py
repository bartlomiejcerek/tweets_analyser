# -*- coding: utf-8 -*-

import io
import pandas as pd
import numpy as np
import time
import pickle

#Just for colab
#from google.colab import files
#uploaded = files.upload()

#feature_df = pd.read_csv(io.BytesIO(uploaded['twitter_dat.txt']), sep=';', index_col=0)
#feature_df

#Preparing binary classifier
not_justin = feature_df['author'] != 'justinbieber'
feature_df['author'][not_justin] = 'not Justin :('
feature_df['author'][feature_df['author'] == 'justinbieber']

#Changing data type
import ast 

def change_str_col_with_list_type(column):
  list_type_col = []
  for row in column:
    list_type_col.append(ast.literal_eval(row))
  return list_type_col

#Data split
from sklearn.model_selection import train_test_split

#1st approach - all the data
# X = change_str_col_with_list_type(feature_df['encoded_tweet_long'])
# y = feature_df['author']

#2nd approach - equal data set for Bieber and others
not_justin_sample = feature_df[not_justin].sample(n=2000)
justin_sample = feature_df[feature_df['author'] == 'justinbieber']

sample = pd.concat([not_justin_sample, justin_sample])

# sample = pd.DataFrame(np.hstack((not_justin_sample, justin_sample))index=np.hstack((not_justin_sample.index, justin_sample.index)))

##Features
file_feature = open('../data/tweets_features', 'rb')
X = pickle.load(file_feature)

#X = change_str_col_with_list_type(sample['encoded_tweet_short'])
y = sample['author']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
print(X)

# def show_summary(predrictions, y_test):
#   acc = accuracy_score(pred, y_test)
#   cm = confusion_matrix(y_test, pred)
#   f = np.sum(cm, axis =1)
#   cm = cm / f *100
#   print('Accuracy: {:.2f}%'.format(acc*100))
#   print(predrictions)
#   fig, ax = plt.subplots(figsize=(8,6), dpi = 100)
#   ax = sns.heatmap(cm, annot=True, ax = ax, fmt='.2f')

#Naive Bayes
#encoded_tweet_long as param
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt 

clf = MultinomialNB()
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
acc = accuracy_score(pred, y_test)
cm = confusion_matrix(y_test, pred)
f = np.sum(cm, axis =1)
cm = cm / f *100
print('Accuracy: {:.2f}%'.format(acc*100))
fig, ax = plt.subplots(figsize=(8,6), dpi = 100)
ax = sns.heatmap(cm, annot=True, ax = ax, fmt='.2f')

# from sklearn import svm
# import numpy as np
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import confusion_matrix
# import seaborn as sns
# import matplotlib.pyplot as plt 
# # print('done')
# # X_train = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
# # y_train = np.array([1, 1, 2, 2])
# # X_test = [[-0.8, -1]]
# # y_test = [1]

# clf2 = svm.SVC(kernel='linear', C = 1.0)
clf2 = svm.LinearSVC(C=0.84, max_iter=10000,dual = False, random_state=0)
clf2.fit(X_train,y_train)
pred2 = clf2.predict(X_test)
acc2 = accuracy_score(pred2, y_test)
cm2 = confusion_matrix(y_test, pred2)
f2 = np.sum(cm2, axis =1)
cm2 = cm2 / f2 *100
print('Accuracy: {:.2f}%'.format(acc2*100))
fig, ax = plt.subplots(figsize=(8,6), dpi = 100)
ax = sns.heatmap(cm2, annot=True, ax = ax, fmt='.2f')

from sklearn import neighbors
clf3 = neighbors.KNeighborsClassifier()
clf3.fit(X_train, y_train)
pred3 = clf3.predict(X_test)
acc3 = accuracy_score(pred3, y_test)
cm3 = confusion_matrix(y_test, pred3)
f3 = np.sum(cm3, axis =1)
cm3 = cm3 / f3 *100
print('Accuracy: {:.2f}%'.format(acc3*100))
fig, ax = plt.subplots(figsize=(8,6), dpi = 100)
ax = sns.heatmap(cm3, annot=True, ax = ax, fmt='.2f')

# classifier = svm.LinearSVC(max_iter=3, C=.05, random_state=0, loss='squared_hinge',penalty='l1',dual=False, fit_intercept=False, class_weight='balanced')
from sklearn import svm
clf4 = svm.SVC(kernel = 'rbf', max_iter=10000)
clf4.fit(X_train, y_train)
pred4 = clf4.predict(X_test)
acc4 = accuracy_score(pred4, y_test)
cm4 = confusion_matrix(y_test, pred4)
f4 = np.sum(cm4, axis =1)
cm4 = cm4 / f4 *100
print('Accuracy: {:.2f}%'.format(acc4*100))
fig, ax = plt.subplots(figsize=(8,6), dpi = 100)
ax = sns.heatmap(cm4, annot=True, ax = ax, fmt='.2f')

from sklearn.ensemble import RandomForestClassifier

clf5 = RandomForestClassifier(n_estimators = 1000, criterion='entropy', max_features=None)

clf5.fit(X_train, y_train)
pred5 = clf5.predict(X_test)
acc5 = accuracy_score(pred5, y_test)
cm5 = confusion_matrix(y_test, pred5)
f5 = np.sum(cm5, axis =1)
cm5 = cm5 / f5 *100
print('Accuracy: {:.2f}%'.format(acc5*100))
fig, ax = plt.subplots(figsize=(8,6), dpi = 100)
ax = sns.heatmap(cm5, annot=True, ax = ax, fmt='.2f')

from sklearn.svm import NuSVC
clf6 = NuSVC()
clf6.fit(X_train, y_train)
pred6= clf6.predict(X_test)
acc6 = accuracy_score(pred6, y_test)
cm6 = confusion_matrix(y_test, pred6)
f6 = np.sum(cm6, axis =1)
cm6 = cm6 / f6 *100
print('Accuracy: {:.2f}%'.format(acc6*100))
fig, ax = plt.subplots(figsize=(8,6), dpi = 100)
ax = sns.heatmap(cm6, annot=True, ax = ax, fmt='.2f')

#saving the models
clfP=pickle.dumps(clf,open('../data/clf.sav', 'wb'))
clfP2=pickle.dumps(clf2,open('../data/clf2.sav', 'wb'))
clfP3=pickle.dumps(clf3,open('../data/clf3.sav', 'wb'))
clfP4=pickle.dumps(clf4,open('../data/clf4.sav', 'wb'))
clfP5=pickle.dumps(clf5,open('../data/clf5.sav', 'wb'))


def predict_tweet(vector, classifier_type):
  # X_to_predict = change_str_col_with_list_type(vector['encoded_tweet_short'])
  X_to_predict = np.array(ast.literal_eval(vector)).reshape(1,26)
  if classifier_type == 'bayes':
    classifier = pickle.load(clfP)
  elif classifier_type == 'linearSVC':
    classifier = pickle.load(clfP2)   
  elif classifier_type == 'kneighbors':
    classifier = pickle.load(clfP3)
  elif classifier_type == 'rbfSVC':
    classifier = pickle.load(clfP4)
  elif classifier_type == 'randomForest':
    classifier = pickle.load(clfP5)
  prediction= classifier.predict(X_to_predict)
  return prediction

tweet_number = 2928    
vector = feature_df.iloc[tweet_number]['encoded_tweet_short']
classifier = 'randomForest'
print('Predicted author: %s; \nActual author: %s; \nClassifier: %s.\n' %(predict_tweet(vector, classifier)[0],feature_df.iloc[tweet_number][0], classifier))

tweet_number = 7322
vector = feature_df.iloc[tweet_number]['encoded_tweet_short']
classifier = 'bayes'
print('Predicted author: %s; \nActual author: %s; \nClassifier: %s.\n' %(predict_tweet(vector, classifier)[0],feature_df.iloc[tweet_number][0], classifier))

# clf = LogisticRegression(penalty='l2', tol=0.0001, C=1.0)
