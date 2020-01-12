# -*- coding: utf-8 -*-
from gui import app
from flask import render_template, url_for, session, flash, redirect
from gui.forms import ManualForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    form = ManualForm()
    if form.validate_on_submit():
        flash('Succesfully taken form.')
        return redirect(url_for('index'))
    return render_template('manual.html', form=form)
    