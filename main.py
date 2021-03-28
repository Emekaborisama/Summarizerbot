import os
#from autocorrect import Speller
#spell = Speller('en')
#from textwrap import wrap
import tweepy as tp
import pandas as pd
import numpy as np
import re
from app.threadtotext import thready
import emoji
import requests
import json
from transformers import *
from summarizer import Summarizer, TransformerSummarizer





import logging
import os
from time import sleep

logger = logging.getLogger()

# Start writing code here...import tweepy as tp
# Start writing code here...import tweepy as tp
auth = tp.OAuthHandler('5FecqRmreBqZqtpyBXdfPSffM', 'zEWFERzcCluMg4RUAtpm0V8Nu6fmv3CsqgDrafiESJaS58RZ9w')
auth.set_access_token('1305611268447928320-QBJuKUsGm3AWKaRcCA8ZlZCjOpgbPc', '0vvBoWr3d8IxlrfpLs57tznntDOBlUxf9CkKugo1AVtDa')
api = tp.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


try:
    api.verify_credentials()
    print("Authentication done")
except:
    print("Error during authentication")

import pymongo
import dns

client = pymongo.MongoClient("mongodb+srv://emekaboria:1kgJNTP2YpNe0CNM@cluster0.g6tlp.mongodb.net/tweetid?retryWrites=true&w=majority")
db = client.get_database('tweetid')
record = db.summa_collection




def strip_emoji(text):
    print(emoji.emoji_count(text))
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text
def clean(text):
    textii = re.sub("<br>", "", text)
    textiii = re.sub("><", "", textii)
    tt = re.sub(r"http\S+", "", textiii)
    #out = re.sub(r'\d+', ' ', tt)
    out = tt.replace('^RT[\s]+', '')
    out = out.replace('[^\w\s]','')
    outi = strip_emoji(out)
    #out4 = outi.lower()
    return outi



def reclean(text):
    cleantxt = re.sub('\n', "", text)
    cleantext = re.sub('<', "", cleantxt)
    texti = cleantext.encode('ascii', 'ignore').decode()
    return texti




def gpt_2(text):
  url = "https://summarizerapi3-emekaborisama.cloud.okteto.net/summariz"
  payload = json.dumps({
  "text": text['text']
  })
  headers = {
  'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  if response.status_code == 200:
    result = response.text
    return result
  else:
    result = "An error occur, pls try again"
    return result


GPT2_model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")

import random 
def record_tweet_summary(tweet, summary, tweetid):
    n = random.randint(0,220000000000000000)
    ref_id = n
    new_file = {
    'idd':n,
    'Tweets':tweet,
    'tweet_id': tweetid,
    'Summary':summary
    }
    record.insert_one(new_file)
    return ref_id

def tweet_mention():
    tweets = api.mentions_timeline(tweet_mode = 'extended', count = 1)
    for tweet in tweets:  
        #record_id = record.insert_one(str(tweet.id))
        url =  'https://twitter.com/' + tweet.id_str+ '/status/' + str(tweet.in_reply_to_status_id)
        texti = thready(url)
        text = clean(texti)
        #textii = {"text": text}
        full = ''.join(GPT2_model(text, min_length=50))
        #fu2 = gpt_2(text = textii)
        #if fu2 == 'An error occur, pls try again':
            #fu = fu2
            #print("error update")
        #else:
            #fu = fu2[13: -4]
        #full = fu
        ori_tweet_id = tweet.id
        #full2 = full
        ref_idd = record_tweet_summary(tweet = text, summary = full, tweetid=ori_tweet_id)
    try:
        api.update_status(full, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata = True)
        print('done with the one tweet update....')      
    except:
        print(ref_idd)
        send_user = 'https://summapi.herokuapp.com/summa/?ref_id='+str(ref_idd)
        api.update_status('Your summary exceeded our limit, so we created a link for your summary. Click the link to view your summary \n'+send_user, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata = True)
        print('done with the link tweet update....')      
    
    


"""while True:
  tweets = api.mentions_timeline(tweet_mode= 'extended', count = 1)
  for tweet in tweets:
    tweeti = tweet.id
    #findd = 1332483393288802310
    find_tweetid = record.find_one({"tweet_id":tweeti})
    if find_tweetid == None:
      print("none")
      tweet_mention()
    else:
      finda = find_tweetid['tweet_id']
      if tweeti == finda:
        print("found")
        #break
  sleep(5)"""

while True:
    try:
        tweets = api.mentions_timeline(count = 1)
        for tweet in tweets:
            tweet_text = re.sub('@[^\s]+','',tweet.text)
            if "compress" in tweet_text:
                print(True)
                tweeti = tweet.id
                #findd = 1332483393288802310
                find_tweetid = record.find_one({"tweet_id":tweeti})
                if find_tweetid == None:
                    print("none")
                    tweet_mention()
                else:
                    finda = find_tweetid['tweet_id']
                    if tweeti == finda:
                        print("found")
                        #break
                        sleep(5)
                    else:
                        print("nothing")
            else:
                print(False)
                tweet.favorite()
                tweet.retweet()
    except tp.TweepError:
        # If an exception occurs, generally if will be tweepy.RateLimitError and in that case the bot will sleep for 15 minutes.
        pass

        

