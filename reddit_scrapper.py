import praw
import config as config_setup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def set_up_reddit():
    reddit = praw.Reddit(client_id=config_setup.client_id,
                         client_secret=config_setup.client_secret,
                         user_agent=config_setup.user_agent,
                         username=config_setup.username)
    return reddit


def reddit_parser(topic: str) -> None:
    """
    :param topic: keyword to search through reddit subreddits
    """
    individual_subreddit(topic)
    search_all_subreddit(topic)


def individual_subreddit(topic: str):
    reddit = set_up_reddit()
    headlines = set()

    # Working with hot is better because we will not get new data if we use top
    # default time is all time, so the same titles are gotten over and over again
    # TODO: write exception in case subreddit doesnt exists
    subreddit = reddit.subreddit(topic).hot(limit=10)
    hot_posts = dict()

    # Get comments
    for submission in subreddit:
        # TODO: deal with bot comments
        # TODO: figure how many comments we want to analyze
        hot_posts[submission.title] = submission.comments[0].body
        headlines.add(submission.title)

    # TODO: what is the difference between getting words from topic's subreddit and from all subreddit search
    comments_result = open(f"comments_{topic}.txt", "w+")
    for comment_gotten in hot_posts.values():
        comments_result.write(comment_gotten)
    comments_result.close()

    with open(f"ind_titles_hot_{topic}.txt", "w", encoding="utf-8") as f:
        for result in headlines:
            f.write(result)


def read_titles_count_vector():
    with open("test_titles_hot.txt", "r") as f:
        lines = f.readlines()

    vectorizer = CountVectorizer()

    frequency_words = vectorizer.fit_transform(lines)
    print(vectorizer.get_feature_names_out())
    print(frequency_words.toarray())

    word_weigh_vector = TfidfVectorizer()
    word_weigh = word_weigh_vector.fit_transform(lines)
    words_tiles = word_weigh_vector.get_feature_names_out()
    words_values = word_weigh_vector.idf_

    print(words_tiles)
    print(words_values)

    #dt = pd.DataFrame(col=)
    fig, ax = plt.subplots()
    ax.plot(words_tiles, words_values)
    plt.show()


def search_all_subreddit(topic: str):
    reddit = set_up_reddit()
    # TODO: fix this search, it is taking top instead of hot
    subreddit = reddit.subreddit("all").search(topic, limit=10)

    with open(f"all_titles_hot_{topic}.txt", "w", encoding="utf-8") as f:
        for result in subreddit:
            f.write(result.title)


reddit_parser("cats")


