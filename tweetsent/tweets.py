from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweetsent.nlp import Sentiment, SentimentCustom
import os

import numpy as np
import pandas as pd
import re

import altair as alt


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(os.environ.get('TWITTER_CONSUMER_API_KEY'), os.environ.get('TWITTER_CONSUMER_API_SECRET'))
        auth.set_access_token(os.environ.get('TWITTER_ACCESS_TOKEN'), os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))
        return auth

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    #def clean_tweet(self, tweet):
    #    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        sent = SentimentCustom()
        analysis = sent.analyze_sentiment(tweet)
        score = analysis[0][0]
        if score >= 0.6:
            return "Positivo", score
        elif (score >= 0.3) and (score <= 0.6):
            return "Neutral", score
        elif score < 0.3:
            return "Negativo", score
        else:
            return "Check Custom Model Threshold"

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['Fecha'] = np.array([tweet.created_at for tweet in tweets])
        df['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['Retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['Seguidores'] = np.array([tweet.user.followers_count for tweet in tweets])
        df['TweetLink'] = np.array([f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}" for tweet in tweets])

        return df
    
    
    
class TweetMethods():
    # # # METHODS AND FUNCTIONS # # #
    
    # # DATAFRAME # #
    def get_tweeter_api(self):
        ''' 
        Instantiates Tweeter API object.
        '''
        twitter_client = TwitterClient()
        api = twitter_client.get_twitter_client_api()
        return api
        
    def load_tweets(self,screen_name, cant_tweets):
        ''' 
        Loads tweets from a user.
        '''
        try:
            api = self.get_tweeter_api()
            tweet_analyzer = TweetAnalyzer()
            tweets = api.user_timeline(screen_name=screen_name, count=cant_tweets)
            df = tweet_analyzer.tweets_to_data_frame(tweets)
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df2 = df.set_index('Fecha', drop=True)
            df2 = df2[['Tweets', 'Likes', 'Retweets', 'TweetLink']]
            return df, df2
        except:
            return None

    def load_mentions(self,termino, cant_mentions):
        ''' 
        Loads metions about a user specified term.
        '''
        termino = str(termino).lower()
        tweet_analyzer = TweetAnalyzer()
        api = self.get_tweeter_api()
        tweets = api.search(q=termino, count=cant_mentions)
        df = tweet_analyzer.tweets_to_data_frame(tweets)
        df['Sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet)[0] for tweet in df['Tweets']])
        df['Score'] = np.array([round(float(tweet_analyzer.analyze_sentiment(tweet)[1]), 4) for tweet in df['Tweets']])
        return df

    def get_sentiment(self,df):
        try:
            tweet_analyzer = TweetAnalyzer()
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df1 = df.set_index('Fecha', drop=True)
            df1 = df1[['Tweets', 'Likes', 'Retweets', 'Seguidores','Sentiment', 'Score', 'TweetLink']]
            return df1
        except:
            return None
    
    def get_resumen(self, df):
        try:
            base = df.groupby([pd.Grouper(key='Fecha', freq='H'), 'Sentiment']).size().unstack('Sentiment').fillna(0)
            return base
        except:
            return None
    
    def neg_mayorimp(self, df):
        try:
            filt_seguidores = df['Seguidores'] > 10
            filt_retweets = df["Retweets"] > 1
            filt_neg = df["Sentiment"] == 'Negativo'
            mayor_imp = df[filt_seguidores & filt_retweets & filt_neg].sort_values(by='Seguidores', ascending=False)
            return mayor_imp
        except:
            return None
    # # GRAPHS # # #
    def Viz_likes_retweets(self, df):
        try:
            likes_retweets = df[['Fecha', 'Likes', 'Retweets']].melt(id_vars=['Fecha'])
            chart = alt.Chart(likes_retweets).mark_line().encode(
                x='Fecha',
                y='value',
                color='variable'
            ).properties(
                width='container'
            ).interactive()
            return chart.to_dict()
        except:
            return None

    def Viz_sent_acc_hora(self, df):
        try:
            base = df.groupby([pd.Grouper(key='Fecha', freq='H'), 'Sentiment']).size().unstack('Sentiment').fillna(0)
            byday = base.copy()
            byday['Fecha'] = base.index
            byday = byday[['Fecha', 'Positivo','Negativo', 'Neutral']]
            melted = byday.melt(id_vars=['Fecha'], value_vars=['Positivo', 'Negativo', 'Neutral'])
            chart = alt.Chart(melted).mark_bar(size=35).encode(
                x=alt.X('Fecha:O', axis=alt.Axis(title='Periodo/Hora')),
                y=alt.Y('value:Q', axis=alt.Axis(title='Sentimiento')),
                color=alt.Color('Sentiment', scale=alt.Scale(scheme='blues'))
                ).properties(
                    width='container'
                ).interactive()
            return chart.to_dict()
        except:
            return None
    
    
    