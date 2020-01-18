# -*- coding: utf-8 -*-
from gui import app
from flask import render_template, url_for, session, flash, redirect
from gui.forms import ManualForm

#Datamanagment
import numpy as np 
import pandas as pd


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
    form_dict = session.get('form', None)
    
    df = pd.DataFrame(form_dict, index=[0])
    titles = ['NaN', 'Raw Data']
    
    return render_template('manual_output.html', tables=[df.to_html()], titles =titles)
    