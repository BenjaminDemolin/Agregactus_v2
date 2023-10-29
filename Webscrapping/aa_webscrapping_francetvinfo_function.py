import Common.aa_webscrapping_function as webscrapping_f
import Database.aa_local_database_function as localdb_f

"""
    File name: aa_webscrapping_francetvinfo_function.py
    Description: This file contains functions to extract data from francetvinfo website
"""

# https://www.francetvinfo.fr/

"""
    Description: 
        This function returns all articles links from francetvinfo website. Limit is 20 articles.
    Parameters:
        num_articles : int
    Return:
        articles_links: list
"""
def get_all_articles(num_articles=20):
    try:
        url = localdb_f.get_website_url_by_name("francetvinfo")
        return webscrapping_f.get_articles_links(url,"article")[:num_articles]
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
        titre = webscrapping_f.find_tag(url,".c-title")[0].text
        intro = webscrapping_f.find_tag(url,".c-chapo")[0].text
        corps = webscrapping_f.find_tag(url,".c-body")[0].text
        return titre + "\n" + intro + "\n" + corps
    except Exception as e:
        print(e)
        return e