import os
import csv
import requests as req
from flask import Flask, request, jsonify
import tweepy
from keras.models import load_model
#from keras.preprocessing.sequence import pad_sequences
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
import pickle
import tensorflow as tf
# from flask.ext.cors import CORS, cross_origin
#import joblib
tf.compat.v1.disable_v2_behavior()
from flask import make_response
# --------------------------------------
# BASIC APP SETUP
# --------------------------------------
app = Flask(__name__, instance_relative_config=True)

# Config
app_settings = os.getenv("APP_SETTINGS", "main.config.DevelopmentConfig")
app.config.from_object(app_settings)

# Extensions
from flask_cors import CORS,cross_origin

CORS(app)

# Keras stuff
model = load_model("main/Sentiment_CNN_model.h5")
MAX_SEQUENCE_LENGTH = 300

# loading tokenizer
with open("main/tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)


def predict(text, include_neutral=True):
    # Tokenize text
    x_test = pad_sequences(
        tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH
    )
    # Predict
    score = model.predict([x_test])[0]
    if score >= 0.4 and score <= 0.6:
        label = "Neutral"
    if score <= 0.4:
        label = "Negative"
    if score >= 0.6:
        label = "Positive"

    return {"label": label, "score": float(score)}


@app.route("/")
def index():
    return "Hello"
@app.route("/analyzehashtag", methods=["GET"])
def analyzehashtag():
    positive = 0
    neutral = 0
    negative = 0
    keyword=request.args.get("text")
    if keyword.isnumeric():
        tweets = []
        with open("main/text_emotion.csv", newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tweet_dict = {}
                tweet_dict["text"] = row["content"]
                tweet_dict["tweet_id"] = row["tweet_id"]
                tweets.append(tweet_dict)
        filtered_tweets = [tweet for tweet in tweets if keyword in tweet["tweet_id"]]
        for tweet in filtered_tweets:            
            prediction = predict(tweet["text"])
            if prediction["label"] == "Positive":
                positive += 1
            if prediction["label"] == "Neutral":
                neutral += 1
            if prediction["label"] == "Negative":
                negative += 1
        return jsonify({"positive": positive, "neutral": neutral, "negative": negative})
    elif keyword[0]=='@':
        name=keyword[1:]
        tweets = []
        with open("main/text_emotion.csv", newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tweet_dict = {}
                tweet_dict["text"] = row["content"]
                tweet_dict["author"] = row["author"]
                tweets.append(tweet_dict)
        filtered_tweets = [tweet for tweet in tweets if name in tweet["author"]]
        for tweet in filtered_tweets:            
            prediction = predict(tweet["text"])
            if prediction["label"] == "Positive":
                positive += 1
            if prediction["label"] == "Neutral":
                neutral += 1
            if prediction["label"] == "Negative":
                negative += 1
        return jsonify({"positive": positive, "neutral": neutral, "negative": negative})
    else:
        tweets = []
        with open("main/twitter_dataset.csv", newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tweets.append(row['text'])
        with open("main/text_emotion.csv", newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tweets.append(row['content'])
        filtered_tweets = [tweet for tweet in tweets if keyword in tweet]
        for tweet in filtered_tweets:
            prediction = predict(tweet)
            if prediction["label"] == "Positive":
                positive += 1
            if prediction["label"] == "Neutral":
                neutral += 1
            if prediction["label"] == "Negative":
                negative += 1
        return jsonify({"positive": positive, "neutral": neutral, "negative": negative})

    
@app.route("/gettweets", methods=["GET"])
def gettweets():
    tweets = []
    keyword = request.args.get("text")
    if keyword.isnumeric():
        with open("main/text_emotion.csv", newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tweet_dict = {}
                tweet_dict["text"] = row["content"]
                tweet_dict["username"] = row["author"]
                tweet_dict["tweet_id"] = row["tweet_id"]
                tweets.append(tweet_dict)
        filtered_tweets = [tweet for tweet in tweets if keyword in tweet["tweet_id"]]

        filtered_tweet_predictions = []
        for tweet in filtered_tweets:
            temp = {}
            temp["text"] = tweet["text"]
            temp["username"] = tweet["username"]
            prediction = predict(tweet["text"])
            temp["label"] = prediction["label"]
            temp["score"] = prediction["score"]
            filtered_tweet_predictions.append(temp)

        return jsonify({"results": filtered_tweet_predictions})
    elif keyword[0]=='@':
        name=keyword[1:]
        with open("main/text_emotion.csv", newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tweet_dict = {}
                tweet_dict["text"] = row["content"]
                tweet_dict["username"] = row["author"]
                
                tweets.append(tweet_dict)
        filtered_tweets = [tweet for tweet in tweets if name in tweet["username"]]

        filtered_tweet_predictions = []
        for tweet in filtered_tweets:
            temp = {}
            temp["text"] = tweet["text"]
            temp["username"] = tweet["username"]
            prediction = predict(tweet["text"])
            temp["label"] = prediction["label"]
            temp["score"] = prediction["score"]
            filtered_tweet_predictions.append(temp)

        return jsonify({"results": filtered_tweet_predictions})
    else :
        with open("main/twitter_dataset.csv", newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tweet_dict = {}
                tweet_dict["text"] = row["text"]
                tweet_dict["username"] = row["name"]
                tweets.append(tweet_dict)
    with open("main/text_emotion.csv", newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tweet_dict = {}
            tweet_dict["text"] = row["content"]
            tweet_dict["username"] = row["author"]
            tweets.append(tweet_dict)
    filtered_tweets = [tweet for tweet in tweets if keyword in tweet["text"]]

    filtered_tweet_predictions = []
    for tweet in filtered_tweets:
        temp = {}
        temp["text"] = tweet["text"]
        temp["username"] = tweet["username"]
        prediction = predict(tweet["text"])
        temp["label"] = prediction["label"]
        temp["score"] = prediction["score"]
        filtered_tweet_predictions.append(temp)

    return jsonify({"results": filtered_tweet_predictions})
