"""
These two functions help take twitter data and turn it into a
workable corpus for NLP
"""

import pandas as pd
import numpy as np
import pickle
import json
import seaborn as sns
import matplotlib as plt


def txt_to_df(txt_path):
    """
    Powerhouse function to take raw scraped twitter data
    into a DataFrame of just the tweet texts

    Args:
        txt_path: The path for the saved file containing
            the tweet data in json format

    Returns:
        A DataFrame containing just the raw tweet texts
    """
    path = txt_path
    tweets_file = open(path, "r")
    tweets_data = []
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    tweet = pd.DataFrame(tweets_data)
    tweet = tweet[tweet["lang"] == "en"]
    try:
        tweet = tweet[["full_text", "created_at", "retweeted_status"]]
        tweet["long_text"] = tweet["full_text"]
        tweet["long_text"] = tweet.apply(ext_rt, axis=1)
        tweet["long_text"] = tweet.apply(rm_links, axis=1)
        tweet["year"] = pd.to_datetime(tweet["created_at"])
        tweet["year"] = tweet.apply(to_year, axis=1)
        return tweet[["long_text", "year"]]
    except:
        try:
            tweet["long_text"] = tweet["content"]
            tweet["long_text"] = tweet.apply(rm_links, axis=1)
            tweet["year"] = pd.to_datetime(tweet["date"])
            tweet["year"] = tweet.apply(to_year, axis=1)
            return tweet[["long_text", "year"]]
        except:
            return tweet[["long_text", "year"]]


def snscrape_to_df(txt_path):
    path = txt_path
    tweets_file = open(path, "r")
    tweets_data = []
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    tweet = pd.DataFrame(tweets_data)
    tweet = tweet[tweet["lang"] == "en"]
    tweet["long_text"] = tweet["content"]
    return tweet[["long_text"]]


def ext_rt(row):
    try:
        if type(row["retweeted_status"]) == dict:
            return row["retweeted_status"]["extended_tweet"]["full_text"]
        else:
            return row["long_text"]
    except:
        return row["long_text"]


def to_year(row):
    return row["year"].year


def rm_links(row):
    text = row["long_text"]
    text = re.sub(r"https:\S*", "", text)
    row["long_text"] = text
    return row["long_text"]


def display_topics(model, feature_names, no_top_words, topic_names=None):
    for ix, topic in enumerate(model.components_):
        if not topic_names or not topic_names[ix]:
            print("\nTopic ", ix)
        else:
            print("\nTopic: '", topic_names[ix], "'")
        print(
            ", ".join(
                [
                    feature_names[i]
                    for i in topic.argsort()[: -no_top_words - 1 : -1]
                ]
            )
        )


def scatter(x, colors, num_topics):
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", num_topics))

    # We create a scatter plot.
    f = plt.figure(figsize=(10, 10))
    ax = plt.subplot(aspect="equal")
    sc = ax.scatter(
        x[:, 0], x[:, 1], lw=0, s=30, c=palette[colors.astype(np.int)]
    )
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.axis("off")
    ax.axis("tight")

    # We add the labels for each digit.
    txts = []
    for i in range(num_topics):
        # Position of each label.
        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, str(i), fontsize=24)
        # txt.set_path_effects([
        #     PathEffects.Stroke(linewidth=5, foreground="w"),
        #     PathEffects.Normal()])
        txts.append(txt)

    return f, ax, sc, txts


# Let's make visualizing the data a bit easier

# def txt_to_df(txt_path):
#     """
#     Powerhouse function to take raw scraped twitter data
#     into a DataFrame of just the tweet texts

#     Args:
#         txt_path: The path for the saved file containing
#             the tweet data in json format

#     Returns:
#         A DataFrame containing just the raw tweet texts
#     """
#     path = txt_path
#     tweets_file = open(path, "r")
#     tweets_data = []
#     for line in tweets_file:
#         try:
#             tweet = json.loads(line)
#             tweets_data.append(tweet)
#         except:
#             continue
#     tweet = pd.DataFrame(tweets_data)
#     tweet = tweet[tweet["lang"] == "en"]
#     try:
#         tweet = tweet[["full_text","created_at","retweeted_status"]]
#         tweet["long_text"] = tweet["full_text"]
#         tweet["long_text"] = tweet.apply(ext_rt, axis=1)
#         tweet["year"] = pd.to_datetime(tweet["created_at"])
#         tweet["year"] = tweet.apply(to_year, axis=1)
#         return tweet[["long_text", "year"]]
#     except:
#         try:
#             tweet["long_text"] = tweet['content']
#             tweet["year"] = pd.to_datetime(tweet["date"])
#             tweet["year"] = tweet.apply(to_year, axis=1)
#             return tweet[["long_text", "year"]]
#         except:
#             return tweet[["long_text", "year"]]


# def snscrape_to_df(txt_path):
#     path = txt_path
#     tweets_file = open(path, "r")
#     tweets_data = []
#     for line in tweets_file:
#         try:
#             tweet = json.loads(line)
#             tweets_data.append(tweet)
#         except:
#             continue
#     tweet = pd.DataFrame(tweets_data)
#     tweet = tweet[tweet["lang"] == "en"]
#     tweet["long_text"] = tweet["content"]
#     return tweet[["long_text"]]

# def ext_rt(row):
#     try:
#         if type(row["retweeted_status"]) == dict:
#             return row["retweeted_status"]["extended_tweet"]["full_text"]
#         else:
#             return row["long_text"]
#     except:
#         return row["long_text"]

# def to_year(row):
#     return row["year"].year

# def rm_links(row):
#     text = row["long_text"]
#     text = re.sub(r'https:\S*', '', text)
#     row["long_text"] = text


### PRE YEARS ###
# def txt_to_df(txt_path):
#     """
#     Powerhouse function to take raw scraped twitter data
#     into a DataFrame of just the tweet texts

#     Args:
#         txt_path: The path for the saved file containing
#             the tweet data in json format

#     Returns:
#         A DataFrame containing just the raw tweet texts
#     """
#     path = txt_path
#     tweets_file = open(path, "r")
#     tweets_data = []
#     for line in tweets_file:
#         try:
#             tweet = json.loads(line)
#             tweets_data.append(tweet)
#         except:
#             continue
#     tweet = pd.DataFrame(tweets_data)
#     tweet = tweet[tweet["lang"] == "en"]
#     try:
#         tweet = tweet[
#             [
#                 "text",
#                 "created_at",
#                 "truncated",
#                 "extended_tweet",
#                 "retweeted_status",
#             ]
#         ]
#         tweet["long_text"] = tweet.apply(ext_tweets, axis=1)
#         tweet["long_text"] = tweet.apply(ext_rt, axis=1)
#         tweet["year"] = pd.to_datetime(tweet["created_at"])
#         tweet["year"] = tweet.apply(to_year, axis=1)
#         return tweet[["long_text", "year"]]
#     except:
#         try:
#             tweet["long_text"] = tweet.apply(ext_rt2, axis=1)
#             tweet["year"] = pd.to_datetime(tweet["year"])
#             tweet["year"] = tweet.apply(to_year, axis=1)
#             return tweet[["long_text"]]
#         except:
#             return tweet[["long_text"]]


# def snscrape_to_df(txt_path):
#     path = txt_path
#     tweets_file = open(path, "r")
#     tweets_data = []
#     for line in tweets_file:
#         try:
#             tweet = json.loads(line)
#             tweets_data.append(tweet)
#         except:
#             continue
#     tweet = pd.DataFrame(tweets_data)
#     tweet = tweet[tweet["lang"] == "en"]
#     tweet["long_text"] = tweet["content"]
#     return tweet[["long_text"]]


# def ext_tweets(row):
#     """
#     Helper function to determined truncated tweets and
#     then return the full tweet

#     Args:
#         row: the row a larger DataFrame consisting of all
#             tweet information

#     Returns:
#         A new row with the full tweet text
#     """
#     if row["truncated"] == True:
#         return row["extended_tweet"]["full_text"]
#     else:
#         return row["text"]


# def ext_rt(row):
#     try:
#         if type(row["retweeted_status"]) == dict:
#             return row["retweeted_status"]["extended_tweet"]["full_text"]
#         else:
#             return row["long_text"]
#     except:
#         return row["long_text"]


# def ext_rt2(row):
#     try:
#         if type(row["retweeted_status"]) == dict:
#             return row["retweeted_status"]["full_text"]
#         else:
#             return row["full_text"]
#     except:
#         return row["full_text"]


# def to_year(row):
#     return row["year"].year
