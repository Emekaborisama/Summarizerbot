

import torch
from transformers import *
from summarizer import Summarizer, TransformerSummarizer
from textwrap import wrap
import tweepy as tp
import pandas as pd
import numpy as np
import re
from threadtotext import thready

import logging
import os
from time import sleep

logger = logging.getLogger()

# Start writing code here...import tweepy as tp
auth = tp.OAuthHandler('pIZw54XtvVuGZM4TTJYHZrFX1', '6x1ohdPHRdFnSrUGUo6qbEup3O7eiVk5mMNpnFXcWrLQPNVhTC')
auth.set_access_token('1305611268447928320-F1l1dmnitjvqankinOLIdmDSzDAuqr', 'nmrdw9UwyGbff2Vp11MSbBvaQH2qONJuyPsGbak12V1dR')
api = tp.API(auth)

try:
    api.verify_credentials()
    print("Authentication done")
except:
    print("Error during authentication")




def clean(text):
    textii = text.replace('<br>', '')
    out = re.sub(r'\d+', ' ', textii)
    out = out.replace('^RT[\s]+', '')
    out = out.replace('[^\w\s]','')
    out4 = out.lower()
    return out4



def tweet_mention():
    tweets = api.mentions_timeline(count = 1)
    for tweet in tweets:
        url =  'https://twitter.com/' + tweet.id_str+ '/status/' + str(tweet.in_reply_to_status_id)
        texti = thready(url)
        text = clean(texti)
        model = TransformerSummarizer(transformer_type="XLNet",transformer_model_key="xlnet-base-cased")
        full = ''.join(model(text, min_length=60, ratio = 0.3))
    try:
        tweetiii = api.update_status(full, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata = True)
        print('done with the one tweet update....')       
    except:
        print('Doing the thread update...........')
        anothers = wrap(full, 270)
        anothers[0]
        print('Doing the thread update...........')
        reply0_tweet = anothers[0]
        reply1_tweet = anothers[1]
        tweeti = api.update_status('1/2 \n'+ reply0_tweet, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata = True)
        api.update_status('2/2 \n'+reply1_tweet, in_reply_to_status_id = tweeti.id, auto_populate_reply_metadata=True)
        print("done with thread")


    
while True:
    tweet_mention()
    sleep(10)



    