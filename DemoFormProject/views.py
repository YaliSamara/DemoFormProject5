"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DemoFormProject import app
from DemoFormProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from DemoFormProject.Models.QueryFormStructure import QueryFormStructure 
from DemoFormProject.Models.QueryFormStructure import LoginFormStructure 
from DemoFormProject.Models.QueryFormStructure import UserRegistrationFormStructure 
from DemoFormProject.Models.QueryFormStructure import cotaminationform

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 


@app.route('/')
@app.route('/home')
def home():
    """בהקדם אעלה הערות"""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """בהקדם אעלה הערות"""
    return render_template(
        'contact.html',
        title='about me:',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """בהקדם אעלה הערות."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/Album')
def Album():
    """בהקדם אעלה הערות"""
    return render_template(
        'PictureAlbum.html',
        title='Pictures',
        year=datetime.now().year,
        message='Welcome to my picture album'
    )



# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('/query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )


@app.route('/Data')
def Data():
    """Renders the about page."""
    return render_template(
        'Data.html',
        title='Restoration of contaminated land',
        year=datetime.now().year,
        message='Land pollution table every year'
    )

@app.route('/DataSet')
def DataSet():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\cltxls4.csv'),encoding="utf-8")
    df=df.sample(10)

    raw_data_table = df.to_html(classes = 'table table-hover')
    """Renders the about page."""
    return render_template(
        'DataSet.html',
        title='DataSet-table',
        year=datetime.now().year,
        raw_data_table = raw_data_table,
        message='Restoration of contaminated land.'
    )




@app.route('/DataModel')
def DataModel():

    """בהקדם אעלה הערות """
    return render_template(
        'DataModel.html',
        title='This is my Data Model page abou UFO',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )


@app.route('/DataSet1')
def DataSet1():

    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\Data\\capitals.csv'))
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'DataSet1.html',
        title='This is Data Set 1 page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )
@app.route('/login')
def login():
    """בהקדם אעלה הערות"""
    return render_template(
        'login.html',
        title='login page:',
        year=datetime.now().year,
        message='Your login page.'
    )
    


@app.route('/query' , methods = ['GET' , 'POST'])
def query():

    print("Restoration of contaminated land")

    form1 = cotaminationform()
    #כל המשתנים שהמשתמש נותן לי וזה מוגדר ב 
    chart = ''

   
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/cltxls4.csv'))


    if request.method == 'POST':
        level = form1.contamination.data 
        # מוגדר בעמוד האחר

        df = df[['רשות מקומית ','דרגת זיהום לפני שיקום']]
        # רק העמודות עם התבחינים האלו יופיעו ושאר העמודות לא
        l_rashut = list(set(df['רשות מקומית ']))
        # מציג את התבחין של הרשות מקומית כשורה ולא כעמודה בטבלה
        new_df = pd.DataFrame() 
        # בונה טבלה חדשה שבה נכניס דברים
        new_df['Monicipality'] = l_rashut
        # זה סוגי הדרגות שנכנס לטבלה החדשה Monicipality 
        total_df=new_df.groupby(['Monicipality']).count() 
        # רושם את כלל סכום הדרגות שהיו ברשויות  
        l_no_cont =[]
        for mon in l_rashut:
            n = df.loc[(df['רשות מקומית '] == mon) & ((df['דרגת זיהום לפני שיקום'] == 'אין זיהום') | (df['דרגת זיהום לפני שיקום'] == ' אין זיהום')) ].shape[0]
            # סכום הרשויות שבהן לא היו זיהום
            l_no_cont.append(n)
            # משכלל את סכום רשויות אלה
        new_df['No Cont'] = l_no_cont
        #  No Cont מכניס לטבלה החדשה שעשינו אפשרות של  
        l_no_cont =[]
        for mon in l_rashut:
            n = df.loc[(df['רשות מקומית '] == mon) & (df['דרגת זיהום לפני שיקום'] == 'קל')].shape[0]
            # סכום הרשויות שבהן דרגת הזיהום הייתה קלה
            l_no_cont.append(n)
            # משכלל את סכום הרשויות האלה
        new_df['Light Cont'] = l_no_cont
        #Light Cont מכניס לטבלה החדשה עוד אפשרויות של   
        l_no_cont =[]
        for mon in l_rashut:
            n = df.loc[(df['רשות מקומית '] == mon) & ((df['דרגת זיהום לפני שיקום'] == 'בינוני') | (df['דרגת זיהום לפני שיקום'] == ' בינוני')) ].shape[0]
            #סכום הרשויות שבהן דרגת הזיהום היא בינונית 
            l_no_cont.append(n)
            # משכלל את סכום הרשויות האלה
        new_df['Medium Cont'] = l_no_cont
        #  Medium Cont מוסיף לטבלה עוד אפשרות של  
        l_no_cont =[]
        for mon in l_rashut:
            n = df.loc[(df['רשות מקומית '] == mon) & (df['דרגת זיהום לפני שיקום'] == 'כבד')].shape[0]
            #סכום הרשויות שבהן דרגת הזיהום היא כבדה
            l_no_cont.append(n)
            #משכלל את סכום הרשויות האלה
        new_df['Heavy Cont'] = l_no_cont
        #  Heavy Cont מוסיף לטבלה עוד אפשרות של 

        new_df[level] = new_df[level] / (new_df['Heavy Cont'] + new_df['Light Cont'] + new_df['No Cont'])
        #Level =  סכום דרגת הזיהום לפני 
        #יחס דרגת הסיכום לפני בין סכום כל הדרגות בכל הרשויות אחרי  
    
        new_df=new_df.fillna(value=0)
        #במקום שיהיה רשום לרשות שאין לה דרגת זיהום יהיה רשום 0
        new_df=new_df[['Monicipality',level]]
        
        new_df['Monicipality']= new_df['Monicipality'].apply(lambda x:x[::-1])
        #הופך את האותיות בשביל שהמילה תהיה ברורה וקריאה
        new_df = new_df.set_index('Monicipality')


        fig1 = plt.figure()
        ax = fig1.add_subplot(111)
        new_df.plot(ax = ax , kind='barh')
        chart = plot_to_img(fig1)
        # מציג את זה כגרף

    
    return render_template(
        'query1.html',
       
        form1 = form1,
        chart = chart
    )

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String







