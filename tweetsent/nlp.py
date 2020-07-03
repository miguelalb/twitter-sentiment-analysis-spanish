from google.cloud import language_v1
from google.cloud.language_v1 import enums
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re 
import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
class SentimentCustom():
    """
    Initializes my own custom made Sentiment Analysis object. 
    I trained this model using Tensorflow with an accuracy on validation set of 80% 
    # Parameters during training:
    vocab_size = 10000
    embedding_dim = 16
    max_length = 100
    trunc_type='post'
    padding_type='post'
    oov_tok = "<OOV>"
    """
    from tensorflow import keras
    model_path = os.path.join(basedir, 'ml_model/my_model.h5')
    tokenizer_path = os.path.join(basedir, 'ml_model/tokenizer.pickle')

    reconstructed_model = keras.models.load_model(model_path)
    tokenizer = pickle.load(open(tokenizer_path, 'rb'))
    
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())

    def analyze_sentiment(self, text):
        tweet = [self.clean_tweet(text)]
        sequences = self.tokenizer.texts_to_sequences(tweet)
        padded = pad_sequences(sequences, maxlen=100, padding='post', truncating='post')
        return self.reconstructed_model.predict(padded)




class Sentiment():
    """ 
    Initializes a Sentiment Analysis object.
    ---------------
    Steps:
    1. Call get_language_serv_client method to get an instance of the client.
    2. Select the document type (is it a text or an html?) using the 
    select_document_type method.
    3. Select the preferred encoding type with the select_encoding_type method.
    Default is 'UTF32'.
    4. Analyze overall sentiment with analyze_overall_sentiment method or
    analyze each sentence sentiment with analyze_sentence_sentiment method. 

    """

    def get_language_serv_client(self):
        return language_v1.LanguageServiceClient()

    def select_document_type(self,type_='text'):
        ''' 
        Defines type of document.
        Available types: choose 'text' for PLAIN_TEXT or 'html' for HTML.
        Default is text.
        '''
        type_ = str(type_).lower()
        if 'text' in type_:
            return enums.Document.Type.PLAIN_TEXT
        elif 'html' in type_:
            return enums.Document.Type.HTML
        else:
            return "Please choose between 'text' or 'html' for the type_"
    
    def select_encoding_type(self, encoding_type='UTF32'):
        ''' 
        Defines the encoding type for the document. 
        Default is 'UTF32'.
        Available encoding types: NONE, UTF8, UTF16, UTF32
        '''
        encoding_type = str(encoding_type).lower()
        if 'utf32' in encoding_type:
            return enums.EncodingType.UTF32
        elif 'utf16' in encoding_type:
            return enums.EncodingType.UTF16
        elif 'utf8' in encoding_type:
            return enums.EncodingType.UTF8
        elif 'none' in encoding_type:
            return enums.EncodingType.NONE
        else:
            return "Please choose a correct encoding_type (NONE, UTF8, UTF16, UTF32)."
    
    def analyze_overall_sentiment(self, text_content, lan, type_='text'):
        ''' 
        Get overall sentiment and returns a tuple with 
        sentiment score and sentiment score magnitude.
        '''
        client = self.get_language_serv_client()
        type_ = self.select_document_type(type_)
        document = {"content": text_content, "type": type_, "language": lan}
        encoding_type = self.select_encoding_type('UTF32')
        response = client.analyze_sentiment(document, encoding_type=encoding_type)
        return response.document_sentiment.score, response.document_sentiment.magnitude
    
    def  analyze_sentence_sentiment(self, text_content, lan, type_='text'):
        ''' 
        Get sentiment for each sentence on the text and 
        returns a dictionary in pandas dataframe style, the
        dictionary has 3 keys which could be interpreted as columns:
        - sentence_text: The sentence text.
        - sentiment_score: The sentiment score for that sentence.
        - sentiment_magnitude: The sentiment score magnitude for that sentence.
        '''
        client = self.get_language_serv_client()
        type_ = self.select_document_type(type_)
        document = {"content": text_content, "type": type_, "language": lan}
        encoding_type = self.select_encoding_type('UTF32')
        response = client.analyze_sentiment(document, encoding_type=encoding_type)
        data = {'sentence': [],
                'sentiment_score': [], 
                'sentiment_magnitude': [],
                #'main_entity': [],
                #'entity_sent_score': [],
                #'entity_sent_magnitude': []
                }
    
        for sentence in response.sentences:
            data['sentence'].append(sentence.text.content)
            data['sentiment_score'].append(sentence.sentiment.score)
            data['sentiment_magnitude'].append(sentence.sentiment.magnitude)
            # # Trying with entities: # #
            #entities = self.analyze_entity_sentiment(str(sentence),'es')
            # I only want the index of the entity with highest salience:
            #salience = entities['entity_salience']
            #max_salience_i = salience.index(max(salience))
            #data['main_entity'].append(entities['entity'][max_salience_i])
            #data['entity_sent_score'].append(entities['sentiment_score'][max_salience_i])
            #ata['entity_sent_magnitude'].append(entities['sentiment_magnitude'][max_salience_i])
            
            
        return data

    def analyze_entity_sentiment(self, text_content, lan, type_='text'):
        ''' 
        Get sentiment for each entity on the text and 
        returns a dictionary in pandas dataframe style, the
        dictionary has 6 keys which could be interpreted as columns:
        - entity: The entity identified by the ML Algorithm.
        = entity_type: The type of entity (Noum, Place, etc.)
        - entity_salience: How much this entity stands out from the rest of the text. 
        - sentiment_score: The sentiment score for that entity.
        - sentiment_magnitude: The sentiment score magnitude for that entity.
        '''
        client = self.get_language_serv_client()
        type_ = self.select_document_type(type_)
        document = {"content": text_content, "type": type_, "language": lan}
        encoding_type = self.select_encoding_type('UTF32')
        response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
        data = {'entity': [],
                'entity_type': [],
                'entity_salience': [],
                'sentiment_score': [], 
                'sentiment_magnitude': []
                }
    
        for entity in response.entities:
            data['entity'].append(entity.name)
            data['entity_type'].append(enums.Entity.Type(entity.type).name)
            data['entity_salience'].append(entity.salience)
            sentiment = entity.sentiment
            data['sentiment_score'].append(sentiment.score)
            data['sentiment_magnitude'].append(sentiment.magnitude) 
        
        return data
        


    

    def analyze_sentiment(self, text_content, lan):
        """  
        Analyze Sentiment in a string. 
        Text= The text to analyze. 
        """

        client = self.get_language_serv_client()
        # Available types: PLAIN_TEXT, HTML
        type_ = self.select_document_type('text')

        # Optional. If not specified, the language is automatically detected.
        # For list of supported languages:
        # https://cloud.google.com/natural-language/docs/languages
        document = {"content": text_content, "type": type_, "language": lan}

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = self.select_encoding_type()

        response = client.analyze_sentiment(document, encoding_type=encoding_type)

        return response.document_sentiment.score
        
