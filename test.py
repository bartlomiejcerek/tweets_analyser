# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:54:49 2020

@author: Bartek
"""

import pickle
from modules.preprocessing import transform_row
#from modules.classifires import predict_tweet


# PARAMETERS
# open a file, where you stored the pickled data
file = open('data/tweets_parameters', 'rb')

# dump information to that file
tweets_parameters = pickle.load(file)
padding = True

#Make my tweet
my_tweet_parameters = {}
my_tweet_parameters["text"] = "Thats my new tweet that can contain new words like asafFHJJDD"
my_tweet_parameters["author"] = None
my_tweet_parameters["nr_of_shares"] = 999
my_tweet_parameters["nr_of_likes"] = 111
my_tweet_parameters["date_time"] = "12/01/2017 19:52"
  
trasformed_tweet = transform_row(my_tweet_parameters, tweets_parameters, padding)

print(trasformed_tweet)

#pred = predict_tweet(trasformed_tweet, 'rbfSVC')   
#print(pred)


