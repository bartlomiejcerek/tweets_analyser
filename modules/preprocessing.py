#!/usr/bin/env python
# coding: utf-8

# ## 1. Call function _transform(tweets__raw)_ -> _tweets__raw_ is dataframe with tweets' data from file 'tweets.csv'.
# ## 2. Function _transform(tweets__raw)_ returns dataframe, which contains rows corresponding consecutive tweets and colums with extracted features.
# ## 3. Features list:
# * 'author',
# * 'encoded_tweet_long' -> all words in tweet represented as numbers (list of integers),
# * 'encoded_tweet_short' -> words in tweet without stopwords (taken from nltk package) represented as numbers (list of integers),
# * 'letters_nr',
# * 'urls_nr',
# * 'hashtag_nr',
# * 'mentioned_nr' -> e.g. @SelenaGomez,
# * 'exclamations_nr',
# * 'emojis_nr',
# * 'perc_of_upper' -> percentage of upper case letters,
# * 'words_nr' -> number of all words in tweet,
# * 'average_word_len',
# * 'std_dev_word_len' -> standard deviation of word's length,
# * 'min_word_len',
# * 'max_word_len',
# * 'time' -> time of tweet posting represented as number of minutes elapsed from midnight (integer),
# * 'weekday' -> weekday represented as numeric value e.g. Monday = 1 (inetger).

# In[909]:


#Imports and installations
#!pip install emoji
#!pip install keras
#!pip install regex
#import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()


# In[910]:


#Libraries
import pandas as pd
import os
import re
import string
import nltk
import datetime
import statistics as stat
from keras.preprocessing.text import Tokenizer
import emoji
import regex
import pickle


# In[911]:


#Additional downloads
#nltk.download('stopwords')
#nltk.download('wordnet')


# In[912]:


#Download dataset (use in Colab)
#%%capture
#if not os.path.isfile('tweets.csv'):
    #!wget 'https://drive.google.com/uc?export=download&id=17F1luxwaaE4vrhlFsHbOFjSoYhsThuAJ' -O tweets.csv


# In[913]:


#Create data frame
#tweets_raw = pd.read_csv('../data/tweets.csv')
#print("Number of tweets and their features: ", tweets_raw.shape)
#tweets_raw.head()


# In[914]:


#Show general info
#tweets_raw.info()


# In[915]:


#Tweets per person 
#tweets_raw['author'].value_counts()


# In[916]:


# 149 contains: #, @ i https
# 198 contains two #
# 114 contains two https

#tweet_nr = 149
#tweet = tweets_raw['content'][tweet_nr]
#print(tweet)


# In[917]:


def find_urls(text):
    "finds all URLs in the given text and returns the list of them"
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


# In[918]:


def nr_of_urls(text):
    return len(find_urls(text))


# In[919]:


def remove_urls(text):
    return re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)


# In[920]:


def find_mentioned(text):
    "finds all mentions in the given text and returns the list of them. Ommits emails."
    # this line removes email adresses
    text = re.sub("[\w]+@[\w]+\.[c][o][m]", "", text)
    mentions = re.findall('@([a-zA-Z0-9]{1,15})', text)
    return mentions


# In[921]:


def count_mentioned(text):
    return len(find_mentioned(text))


# In[922]:


def remove_mentions_and_emails(text):
    text = re.sub("[\w]+@[\w]+\.[c][o][m]", "", text)
    text = re.sub("@([a-zA-Z0-9]{1,15})", "", text)
    return text


# In[923]:


def find_hashtags(text):
    "finds all hashtags in the given text and returns the list of them. Will catch other #."
    #return list(part[1:] for part in text.split() if part.startswith('#')) # this version won't catch hashtags with no blank spaces before them
    return re.findall(r"#(\w+)", text)


# In[924]:


def count_hashtags(text):
    return len(find_hashtags(text))


# In[925]:


def remove_hashtags(text):
    return re.sub(r"#(\w+)", '', text)


# In[926]:


def count_letters(text):
    return len(text)


# In[927]:


def count_exclamation(text):
    return text.count('!')


# In[928]:


def percent_of_upper(text):
    upper = len(re.findall(r'[A-Z]', text))
    if len(text) == 0:
        return 0
    else:
        return upper / len(text)


# In[929]:


def extract_emojis(text):
    "finds all emoji in the given text and returns the list of them"
    clean_text = regex.findall(r'\X', text)
    return [word for word in clean_text if any(char in emoji.UNICODE_EMOJI for char in word)]


# In[930]:


def remove_emojis(text):
    return text.encode('ascii', 'ignore').decode('ascii')


# In[931]:


punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

def remove_punct(text):
    text  = "".join([char for char in text if char not in punctuation])
    text = re.sub('[0-9]+', '', text)
    return text


# In[932]:


def tokenization(text):
    text = re.split('\W+', text)
    return text


# In[933]:


stopword = nltk.corpus.stopwords.words('english')

def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text


# In[934]:


ps = nltk.PorterStemmer()

def stemming(text):
    text = [ps.stem(word) for word in text]
    return text


# In[935]:


wn = nltk.WordNetLemmatizer()

def lemmatizer(text):
    text = [wn.lemmatize(word) for word in text]
    return text


# In[936]:


def leave_words(text):
    "takes text as list of words. returns list deleting strange things ;)"
    return [word for word in text if re.search('[a-zA-Z]', word) is not None]


# In[937]:


def calculate_word_length_list(words_list):
    return list(map(len, words_list))


# In[938]:


def calculate_average_word_length(words_list):
    words_len_list = calculate_word_length_list(words_list)
    if len(words_len_list) <= 1:
        return 0
    else:
        return stat.mean(words_len_list)


# In[939]:


def calculate_std_deviation_word_length(words_list):
    words_len_list = calculate_word_length_list(words_list)
    if len(words_len_list) <= 1:
        return 0
    else:
        return stat.stdev(words_len_list)


# In[940]:


def calculate_max_word_length(words_list):
    words_len_list = calculate_word_length_list(words_list)
    if len(words_len_list) <= 1:
        return 0
    else:
        return max(words_len_list)


# In[941]:


def calculate_min_word_length(words_list):
    words_len_list = calculate_word_length_list(words_list)
    if len(words_len_list) <= 1:
        return 0
    else:
        return min(words_len_list)


# In[942]:


def split_date_time(date_time):
    "takes date as string. return list in form: [day, month, year, hour, minute], every element is converted to int"
    date_time_split = re.sub("[^\w]", " ",  date_time).split()
    return list(map(int, date_time_split))


# In[943]:


def calculate_time(date_time):
    "takes date as string. returns time in minutes elapsed from midnight"
    date_time_split = split_date_time(date_time)
    return date_time_split[3]*60 + date_time_split[4]


# In[944]:


def calculate_weekday(date_time):
    "takes date as string. returns weekday"
    date_time_split = split_date_time(date_time)
    return datetime.date(date_time_split[2],date_time_split[1],date_time_split[0]).weekday()


# In[945]:


def transform_for_words_long_coding(text):
    t = remove_emojis(text)
    t = remove_urls(t)
    t = remove_hashtags(t)
    t = remove_mentions_and_emails(t)
    t = remove_punct(t)
    t = tokenization(t.lower())
    t = leave_words(t)
    return t


# In[946]:


def transform_for_words_short_coding(text):
    t = transform_for_words_long_coding(text)
    t = remove_stopwords(t)
    t = stemming(t)
    t = lemmatizer(t)
    return t


# In[947]:


def create_tokenizer(texts, type):
    transformed_texts = []
    for t in texts:
        if type == "long":
            transformed_texts.append(transform_for_words_long_coding(t))
        elif type == "short":
            transformed_texts.append(transform_for_words_short_coding(t))
        else:
            print("Incorrect tokenizer type. Must be 'long' or 'short'.")
    # create the tokenizer
    tok = Tokenizer()
    # fit the tokenizer on words
    tok.fit_on_texts(transformed_texts)
    return tok


# In[948]:


def create_char_codes(texts, type):
    transformed_texts = []
    for t in texts:
        if type == "long":
            transformed_texts.append(transform_for_words_long_coding(t))
        elif type == "short":
            transformed_texts.append(transform_for_words_short_coding(t))
        else:
            print("Incorrect tokenizer type. Must be 'long' or 'short'.")
    char_list = [c for t in transformed_texts for s in t for c in s]
    unique_chars = sorted(set(char_list))
    return {u:i for i, u in enumerate(unique_chars)}


# In[949]:


def get_max_words_nr(texts, type):
    if type == "long":
        return max([len( transform_for_words_long_coding(t) ) for t in texts])
    elif type == "short":
        return max([len( transform_for_words_short_coding(t) ) for t in texts])
    elif type == "char":
        return max([len( t.replace(" ", "") ) for t in texts])
    else:
        return None


# In[950]:


def add_padding(list_to_extend, basic_len, extended_len):
    if basic_len > extended_len:
        del list_to_extend[basic_len:]
    else:
        list_to_extend.extend([0]*(extended_len - basic_len))
    return list_to_extend


# In[951]:


def transform_row(tweet_param_dict, data_param_dict, padding):
    "takes tweet text, nr of shares and nr of likes and returns extracted features"
    #unpack dictionaries
    text = tweet_param_dict["text"]
    author = tweet_param_dict["author"]
    nr_of_shares = tweet_param_dict["nr_of_shares"]
    nr_of_likes = tweet_param_dict["nr_of_likes"]
    date_time = tweet_param_dict["date_time"]
    tokenizer_long = data_param_dict["tokenizer_long"]
    tokenizer_short = data_param_dict["tokenizer_short"]
    char_codes = data_param_dict["char_codes"]
    max_words_nr_long = data_param_dict["max_words_nr_long"]
    max_words_nr_short = data_param_dict["max_words_nr_short"]
    max_chars_nr_long = data_param_dict["max_chars_nr_long"]
    
    #get features
    nr_of_letters = count_letters(text)
    urls_list = find_urls(text)
    urls_nr = len(urls_list)
    hashtag_list = find_hashtags(text)
    hashtag_nr = len(hashtag_list)
    mentioned_list = find_mentioned(text)
    mentioned_nr = len(mentioned_list)
    exclamations_nr = count_exclamation(text)
    emojis_list = extract_emojis(text)
    emojis_nr = len(emojis_list)
    t = remove_emojis(text)
    t = remove_urls(t)
    t = remove_hashtags(t)
    t = remove_mentions_and_emails(t)
    t = remove_punct(t)
    perc_of_upper = percent_of_upper(t)
    t = tokenization(t.lower())
    t = leave_words(t)
    nr_of_words = len(t)
    average_word_len = calculate_average_word_length(t)
    std_dev_word_len = calculate_std_deviation_word_length(t)
    min_word_len = calculate_min_word_length(t)
    max_word_len = calculate_max_word_length(t)
    # first character and words coding
    encoded_tweet_long = tokenizer_long.texts_to_sequences([t])[0]
    if padding and len(encoded_tweet_long) < max_words_nr_long:
        encoded_tweet_long = add_padding(encoded_tweet_long, len(encoded_tweet_long), max_words_nr_long)
    encoded_tweet_chars = [char_codes[c] for s in t for c in s]
    if padding and len(encoded_tweet_chars) < max_chars_nr_long:
        encoded_tweet_chars = add_padding(encoded_tweet_chars, len(encoded_tweet_chars), max_chars_nr_long)
    t = remove_stopwords(t)
    t = stemming(t)
    t = lemmatizer(t)
    # second character and words coding
    encoded_tweet_short = tokenizer_short.texts_to_sequences([t])[0]
    if padding and len(encoded_tweet_short) < max_words_nr_short:
        encoded_tweet_short = add_padding(encoded_tweet_short, len(encoded_tweet_short), max_words_nr_short)
    time = calculate_time(date_time)
    weekday = calculate_weekday(date_time)
    if author == 'justinbieber':
        author = 1
    else:
        author = 0
    return [author, encoded_tweet_long, encoded_tweet_short, encoded_tweet_chars, nr_of_letters, urls_nr, hashtag_nr, mentioned_nr, \
            exclamations_nr, emojis_nr, perc_of_upper, nr_of_words, average_word_len, \
            std_dev_word_len, min_word_len, max_word_len, time, weekday]


# In[952]:


def get_data_parameters(tweets_raw):
    data_parameters = {}
    data_parameters['tokenizer_long'] = create_tokenizer(tweets_raw['content'], "long")
    data_parameters['tokenizer_short'] = create_tokenizer(tweets_raw['content'], "short")
    data_parameters['char_codes'] = create_char_codes(tweets_raw['content'], "long")
    data_parameters['max_words_nr_long'] = get_max_words_nr(tweets_raw['content'], "long")
    data_parameters['max_words_nr_short'] = get_max_words_nr(tweets_raw['content'], "short")
    data_parameters['max_chars_nr_long'] = get_max_words_nr(tweets_raw['content'], "char")
    return data_parameters


# In[953]:


def transform(tweets_raw):
    tweets_parameters = get_data_parameters(tweets_raw)
    #print(tokenizer_short.word_index)
    features_list = []
    for index, row in tweets_raw.iterrows():
        tweet_param_dict = {}
        tweet_param_dict["text"] = row['content']
        tweet_param_dict["author"] = row['author']
        tweet_param_dict["nr_of_shares"] = row['number_of_shares']
        tweet_param_dict["nr_of_likes"] = row['number_of_likes']
        tweet_param_dict["date_time"] = row['date_time']
        features_list.append(transform_row(tweet_param_dict, tweets_parameters, True))
    return pd.DataFrame(features_list, columns = ['author', 'encoded_tweet_long', 'encoded_tweet_short', 'encoded_tweet_chars', 'nr_of_letters', 'urls_nr', \
                                                  'hashtag_nr', 'mentioned_nr', 'exclamations_nr', 'emojis_nr', 'perc_of_upper', \
                                                  'nr_of_words', 'average_word_len', 'std_dev_word_len', 'min_word_len', 'max_word_len', \
                                                  'time', 'weekday']) 


# In[954]:


########################################
### CREATING DATAFRAME WITH FEATURES ###
########################################

#nr_of_tweets, par = tweets_raw.shape # number of tweets to take features
#feature_df = transform(tweets_raw)
#print(len(feature_df))


# In[955]:

def tranform_and_write_to_file(tweets_raw)
    feature_df = transform(tweets_raw)
    # open a file, where you want to store the data
    file = open('../data/tweets_features', 'wb')
    # dump information to that file
    pickle.dump(feature_df, file)
    # close the file
    file.close()


# In[957]:

def calculate_parameters_and_write_to_file(tweets_raw):
    tweets_parameters = get_data_parameters(tweets_raw)
    # open a file, where you want to store the data
    file = open('../data/tweets_parameters', 'wb')
    # dump information to that file
    pickle.dump(tweets_parameters, file)
    # close the file
    file.close()
    
############# USAGE EXAMPLE ####################
'''which_tweet = 4
tweet_param_dict = {}
tweet_param_dict["text"] = tweets_raw['content'][which_tweet]
tweet_param_dict["author"] = tweets_raw['author'][which_tweet]
tweet_param_dict["nr_of_shares"] = tweets_raw['number_of_shares'][which_tweet]
tweet_param_dict["nr_of_likes"] = tweets_raw['number_of_likes'][which_tweet]
tweet_param_dict["date_time"] = tweets_raw['date_time'][which_tweet]

data_param_dict = get_data_parameters(tweets_raw)

transform_row(tweet_param_dict, data_param_dict, True)'''
