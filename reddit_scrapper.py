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


def reddit_parser():
    reddit = set_up_reddit()
    headlines = set()

    topic = "politics"
    subreddit = reddit.subreddit(topic).top(limit=5)
    top_posts = dict()

    for submission in subreddit:
        top_posts[submission.title] = submission.comments[0].body
        headlines.add(submission.title)

    comments_result = open(f"comments_{topic}.txt", "w+")
    for comment_gotten in top_posts.values():
        comments_result.write(comment_gotten)
    comments_result.close()

    title_posts = pd.DataFrame(headlines)
    title_posts.to_csv('test_titles_hot.csv', header=False, encoding='utf-8', index=False)


def read_titles_count_vector():
    with open("test_titles_hot.csv", "r") as f:
        lines = f.readlines()

    vectorizer = CountVectorizer()

    frequency_words = vectorizer.fit_transform(lines)
    print(vectorizer.get_feature_names_out())
    print(frequency_words.toarray())

    word_weigh_vector = TfidfVectorizer()
    word_weigh = word_weigh_vector.fit_transform(lines)
    words_tiles = word_weigh_vector.get_feature_names_out()
    words_values = word_weigh_vector.idf_

    fig, ax = plt.subplots()
    ax.plot(words_tiles, words_values)
    plt.show()




# reddit_parser()
read_titles_count_vector()

