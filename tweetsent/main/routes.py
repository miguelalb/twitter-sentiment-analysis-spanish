from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from tweetsent import db
from tweetsent.nlp import Sentiment
from tweetsent.auth.email import send_password_reset_email
from tweetsent.tweets import TwitterClient, TweetAnalyzer, TweetMethods
from tweetsent.main.forms import TweetsForm, MentionsForm
from tweetsent.models import User
from tweetsent.main import bp

import json
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


## TODO ##
# # USER PROFILE # #



# # LANDING PAGE # #
@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Sentiment Analysis Twitter')

# # APP # #
df = None
mayor_imp = None
resumen = None
viz = json.dumps({"a":1})

@bp.route('/app', methods=['GET', 'POST'])
@login_required
def main():
    global df
    global mayor_imp
    global resumen
    global viz
    
    fnc = TweetMethods() # Funcions
    
    # Instantiating form to fetch Tweets:
    form1 = TweetsForm()
    form1.screen_name.choices = [('luisabinader', 'Luis Abinader'),
                                ('Gonzalo2020RD', 'Gonzalo Castillo'),
                                ('LeonelFernandez', 'Leonel Fernandez')]
    
    # Instantiating form to fetch Mentions and Sentiment:
    form2 = MentionsForm()
    form2.terminos.choices = [('luis abinader', 'Luis Abinader'), ('prm', 'PRM'),
        ('partido revolucionario moderno', 'Partido Revolucionario Moderno'),
        ('gonzalo castillo', 'Gonzalo Castillo'), ('leonel fernandez', 'Leonel Fernandez')
        ]
    
    # validating input from user:
    # for tweets:
    if form1.validate_on_submit():
        df1, df = fnc.load_tweets(form1.screen_name.data[0], form1.cant_tweets.data)
        temp = fnc.Viz_likes_retweets(df1)
        if temp is not None:
            viz = temp
        else:
            viz = json.dumps({})
        mayor_imp = None
        resumen = None
        return redirect(url_for('main.main'))
    
    # for mentions:
    if form2.validate_on_submit():
        print(f"Terminos:{form2.terminos.data}, Cant: {form2.cant_mentions.data}")
        df = fnc.load_mentions(form2.terminos.data, form2.cant_mentions.data)
        print(f"Shape of initial df {df.shape}")
        df2 = fnc.get_sentiment(df)
        resumen = fnc.get_resumen(df)
        mayor_imp = fnc.neg_mayorimp(df2)
        temp = fnc.Viz_sent_acc_hora(df)
        print(f"Temp: {temp}")
        print()
        if temp is not None:
            viz = json.dumps(temp)
        else:
            viz = json.dumps({})
        df = df2
        return redirect(url_for('main.main'))
    
    return render_template('main.html', table=df, table2=resumen, table3=mayor_imp, viz=viz,
                             form1=form1, form2=form2, title='App')