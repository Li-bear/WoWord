import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import requests
import all_scrapper


def get_type_word(word_to_search):
    r = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word_to_search}')
    if r.status_code == 200:
        info_api_dict = r.json()
        for info in info_api_dict[0]['meanings']:
            # dict_keys(['partOfSpeech', 'definitions', 'synonyms', 'antonyms'])
            return info['partOfSpeech']


def get_n_top_words(filename, n_words, keyword):
    df = pd.DataFrame()
    with open(filename, "r", encoding='utf8') as f:
        lines = f.readlines()

    common_words = []
    with open("common_words.txt", 'r', encoding='utf-8') as f:
        common_words = f.readlines()

    common_words = [common_words[index].replace('\n', '') for index in range(len(common_words))]

    #  TF-IDF is an acronym for “Term Frequency — Inverse Document Frequency”
    word_weigh_vector = TfidfVectorizer()
    words_TF = word_weigh_vector.fit_transform(lines)
    words_tiles = word_weigh_vector.get_feature_names_out()

    df['words'] = words_tiles
    df['TF'] = word_weigh_vector.idf_

    # clean dataframe from common words
    df = df[~df['words'].isin(common_words)]

    # clean keyword topic
    # index_keyword = df.index[df['words'] == keyword].tolist()[0]
    # df.drop(index_keyword, inplace=True)

    # sort by importance
    df = df.sort_values(['TF'])

    result_df = df.head(n_words).copy()

    for word in result_df['words']:
        result_df.loc[result_df['words'] == word, 'type'] = get_type_word(word)
    return result_df


def top_words_gui_getter(topic: str, n: int, source: int):
    if source == 0:
        all_scrapper.wikipedia_parser(topic)
        return get_n_top_words(f"wikipedia_{topic}.txt", n, "")
    elif source == 1:
        all_scrapper.search_all_subreddit(topic)
        return get_n_top_words(f"reddit_{topic}.txt", n, "")
    elif source == 2:
        all_scrapper.youtube_parser(topic)
        return get_n_top_words(f"youtube_{topic}.txt", n, "")


def pie_chart_individual_source(source_df: pd.DataFrame, source_from: str) -> plt.figure:
    """
    :param source_df: dataframe containing the most n popular words from a specific source
    :param source_from: string used for title indicating where the data is parsed
    :return: figure to use in gui.py
    """
    labels = source_df['words']
    TF_value = source_df['TF']

    fig, ax = plt.subplots()
    plt.title(f"TF-IDF from {source_from}")
    ax.pie(TF_value, labels=labels, autopct='%1.1f%%')
    return fig


def bar_chart_all_sources(all_df: pd.DataFrame) -> plt.figure:
    """
    :param all_df: concatenate datafrmaes from all sources chosen
    :return: bar char with type of word frequency
    """
    series_words = all_df['type'].value_counts()

    # creating the dataset
    fig = plt.figure(figsize=(5, 5))

    # creating the bar plot
    plt.bar(series_words.index, series_words.values, color='green',
            width=0.4)

    plt.xlabel("Word type")
    plt.ylabel("Frequency")
    plt.title("Frequency of word types")
    return fig
