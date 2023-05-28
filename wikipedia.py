import requests
import re
from bs4 import BeautifulSoup

def wikipediaArticleContent(url):
    response = requests.get(url)
    tree = BeautifulSoup(response.content, 'html.parser')
    article = tree.find('div', {'class' : 'mw-body-content mw-content-ltr'}).get_text()

    endOfArticle = article.find("References\n")
    if endOfArticle != -1:
        article = article[:endOfArticle]
    article = re.sub(r"\[\d+\]",'',article)
    return article

print(wikipediaArticleContent('https://en.wikipedia.org/wiki/Python_(programming_language)'))