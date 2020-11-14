"""
These functions help take twitter data and turn it into a
workable corpus for NLP
"""

import pandas as pd
import numpy as np
import pickle
import json
import seaborn as sns
import matplotlib as plt
import re


def txt_to_df(txt_path):
    """
    Powerhouse function to take raw scraped twitter data
    into a DataFrame of just the tweet texts and years

    Args:
        txt_path: The path for the saved file containing
            the tweet data in json format

    Returns:
        A DataFrame containing just the raw tweet texts and years tweeted
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


def ext_rt(row):
    """
    Function to extract full retweet text
    For use in txt_to_df and .apply or .map functionality

    Args:
        row: row from dataframe

    Returns:
        Full text of a retweeted tweet
    """
    try:
        if type(row["retweeted_status"]) == dict:
            return row["retweeted_status"]["extended_tweet"]["full_text"]
        else:
            return row["long_text"]
    except:
        return row["long_text"]


def to_year(row):
    """
    Function to extract year
    For use in txt_to_df and .apply or .map functionality

    Args:
        row: row from dataframe

    Returns:
        Year a tweet was tweeted
    """
    return row["year"].year


def rm_links(row):
    """
    Function to remove links from tweets
    For use in txt_to_df and .apply or .map functionality

    Args:
        row: row from dataframe

    Returns:
        Tweet without links
    """
    text = row["long_text"]
    text = re.sub(r"https:\S*", "", text)
    row["long_text"] = text
    return row["long_text"]


def display_topics(model, feature_names, no_top_words, topic_names=None):
    """
    Helps display topics from a given NMF model

    Args:
        model: NMF model being discovered
        feature_names: Terms/tokens being used
            - can use _.get_feature_names() to help
        no_top_words: Number of topics being discovered
        topic_names: Optional to name each topic

    Returns:
        Prints the topics with the corresponding terms/tokens
    """
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
    """
    Function to quickly visualize our TSNE data

    Args:
        x: Coordinates from TSNE
        colors: Variables to determine colors
        num_topics: Number of topics

    Returns:
        Plots TSNE in a nice scatter plot
    """
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
        txts.append(txt)

    return f, ax, sc, txts
