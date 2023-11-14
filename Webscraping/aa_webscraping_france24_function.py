import Common.aa_webscraping_function as webscraping_f
import Database.aa_local_database_function as localdb_f

"""
    File name: aa_webscraping_france24_function.py
    Description: This file contains functions to extract data from france24 website
"""

# https://www.france24.com/fr/info-en-continu/

"""
    Description: 
        This function returns all articles links from france24 website. Limit is 20 articles.
    Parameters:
        num_articles: int
    Return:
        articles_links: list
"""
def get_all_articles(num_articles=20):
    try:
        url = localdb_f.get_website_url_by_name("france24")
        return webscraping_f.get_articles_links(url,".news__content")[:num_articles]
    except Exception as e:
        print(e)
        return e

"""
    Description:
        This function returns the text of an article from a given url
    Parameters:
        url: string
    Return:
        text: string
"""
def get_article_text(url):
    try:
        article = webscraping_f.get_text_from_tag(url,".t-content__title") + "\n"
        article += webscraping_f.get_text_from_tag(url,".t-content__chapo") + "\n"
        article += webscraping_f.get_text_from_tag(url,".t-content__title") + "\n"
        for tag in webscraping_f.find_tag(url,".o-self-promo"):
            article = article.replace(tag.text,"")
        return article
    except Exception as e:
        print(e)
        return e
    