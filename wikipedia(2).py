import requests
import re
import wikipediaapi
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

def wikipediaArticleContentAPI(name):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    article = wiki_wiki.page(name)
    if article.exists():
        return article.text
    else:
        return 0

print(wikipediaArticleContentAPI('Python_(programming_language)'))