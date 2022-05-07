
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
from transformers.modeling_bert import BertModel, BertForMaskedLM
from summarizer import Summarizer, TransformerSummarizer

def model():
    GPT2_model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")
    print(GPT2_model)

model()