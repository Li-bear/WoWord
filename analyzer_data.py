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
    #index_keyword = df.index[df['words'] == keyword].tolist()[0]
    #df.drop(index_keyword, inplace=True)

    # sort by importance
    df = df.sort_values(['TF'])

    result_df = df.head(n_words).copy()

    for word in result_df['words']:
        result_df.loc[result_df['words'] == word, 'type'] = get_type_word(word)
    return result_df

def top_words_gui_getter(topic: str, n: int, source: int):
    if source == 0:
        all_scrapper.wikipedia_parser(topic)
        return get_n_top_words(f"wikipedia_{topic}.txt",n,"")
    elif source == 1:
        all_scrapper.search_all_subreddit(topic)
        return get_n_top_words(f"reddit_{topic}.txt",n,"")
    elif source == 2:
        all_scrapper.youtube_parser(topic)
        return get_n_top_words(f"youtube_{topic}.txt",n,"")
    
print(top_words_gui_getter("Bee",5,0)['words'].values.tolist())