import praw
import config as config_setup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import wikipediaapi
from youtube_transcript_api import YouTubeTranscriptApi


def wikipedia_article_content_API(name):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    article = wiki_wiki.page(name)
    if article.exists():
        return article.text
    else:
        return 0

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
    #individual_subreddit(topic)
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
    titles = np.array([], dtype='string_')
    # Takes top posts
    subreddit = reddit.subreddit("all").search(topic, limit=100)
    for i in subreddit: # submission element
        titles = np.append(titles, i.title)
        # this allows access for first comments
        # i.comments[0:10]

    with open(f"reddit_{topic}.txt", "w", encoding="utf-8") as f:
        for text in titles:
            f.write(text)
            f.write('\n')


def wikipedia_parser(topic):
    # TODO: what happen when there are multiple article pages?
    article = wikipedia_article_content_API(topic)
    with open(f"wikipedia_{topic}.txt", "w", encoding="utf-8") as f:
        f.write(article)

def youtube_parser(topic):
    num_results = 10
    youtube_base_url = 'https://www.youtube.com'

    # Construct the search query URL
    query = '+'.join(topic.split())
    url = f'{youtube_base_url}/results?search_query={query}'

    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Search for the pattern "videoId":"\w+" in the HTML content of soup
    matches = re.findall(r'"videoId":"\w+"', str(soup))

    # Extract the video IDs from the video links
    video_ids = []
    for match in matches:
        video_id = re.search(r'"videoId":"(\w+)"', match)
        if video_id:
            video_ids.append(video_id.group(1))

    number_successes = 0
    index = 0
    transcript = ""
    while number_successes < num_results:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_ids[index])
            # Join the text of each transcript segment to form the full transcript
            transcript = '\n'.join([t['text'] for t in transcript_list])
            number_successes += 1
        except:
            pass
        index += 1

    with open(f"youtube_{topic}.txt", "w", encoding="utf-8") as f:
        f.write(transcript)


if __name__ == '__main__':
    print("WoWord")
    #topic_word = input("Topic to search: ")
    topic_word = 'mathematics'
    reddit_parser(topic_word)
    wikipedia_parser(topic_word)
    youtube_parser(topic_word)




