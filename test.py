# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:54:49 2020

@author: Bartek
"""

import pickle
from modules.preprocessing import transform_row
from modules.classifires import predict_tweet


# PARAMETERS
# open a file, where you stored the pickled data
file = open('../data/tweets_parameters', 'rb')

# dump information to that file
tweets_parameters = pickle.load(file)
tokenizer_long = tweets_parameters['tokenizer_long']
tokenizer_short = tweets_parameters['tokenizer_short']
char_codes = tweets_parameters['char_codes']
max_words_nr_long = tweets_parameters['max_words_nr_long']
max_words_nr_short = tweets_parameters['max_words_nr_short']
max_chars_nr_long = tweets_parameters['max_chars_nr_long']
padding = True

#Make my tweet
text = "Thats my new tweet that can contain new words like asafFHJJDD"
author = None 
nr_of_shares = 999
nr_of_likes = 111
date_time = '12/01/2017 19:52'
  
trasformed_tweet = transform_row(text, author, nr_of_shares, nr_of_likes, date_time, tokenizer_long, tokenizer_short, char_codes, max_words_nr_long, max_words_nr_short, max_chars_nr_long, padding)

pred = predict_tweet(trasformed_tweet, 'rbfSVC')   
print(pred)


