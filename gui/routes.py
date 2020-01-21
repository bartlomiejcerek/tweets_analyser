# -*- coding: utf-8 -*-
from gui import app
from flask import render_template, url_for, session, flash, redirect
from gui.forms import ManualForm
from modules.preprocessing import transform_row

#Datamanagment
import numpy as np 
import pandas as pd
import pickle


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    form = ManualForm()
    if form.validate_on_submit():
        #Create dict to save in session
        form_dict = {'content':form.content.data, 
                     'likes':str(form.likes.data), 
                     'shares':str(form.shares.data), 
                     'datetime':form.datetime.data}
        session['form'] = form_dict
        return redirect(url_for('manual_output'))
    return render_template('manual.html', form=form)
    
@app.route('/manaul_output')
def manual_output():
    titles = ['NaN', 'Raw Data', 'Processed']
    
    form_dict = session.get('form', None)
    raw_df = pd.DataFrame(form_dict, index=[0])
    
    print(str(raw_df['datetime'][0]))
    
    #Tweet transform
    file = open('data/tweets_parameters', 'rb')

    # dump information to that file
    tweets_parameters = pickle.load(file)
    padding = True
    
    #Make my tweet
    my_tweet_parameters = {}
    my_tweet_parameters["text"] = str(raw_df['content'][0])
    my_tweet_parameters["author"] = None
    my_tweet_parameters["nr_of_shares"] = int(raw_df['shares'][0])
    my_tweet_parameters["nr_of_likes"] = int(raw_df['likes'][0])
    my_tweet_parameters["date_time"] = "12/01/2018 19:52"
      
    trasformed_tweet = transform_row(my_tweet_parameters, tweets_parameters, padding)
    trasformed_tweet = [str(i) for i in trasformed_tweet[1:]]
    
    par_names = ['en_long', 'en_short', '    en_all_chars_padded', 'no_let', 'urls_no', 'hashtag_no',' ment_no', \
                 '!_no', '#_no', 'perc_of_up', 'no_words', 'average_word_len', \
                 'std_dev_word_len', 'min_word_len', 'max_word_len', 'time',' weekday']
    
    tweet_dict = dict(zip(par_names,trasformed_tweet))
    tweet_df = pd.DataFrame(data =tweet_dict, index=[0])
    
    return render_template('manual_output.html', tables=[raw_df.to_html(), tweet_df.to_html()], titles = titles)
    