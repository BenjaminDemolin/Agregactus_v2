from requests_html import HTMLSession
from bs4 import BeautifulSoup
import cloudscraper

"""
    File name: aa_webscrapping_function.py
    Description: This file contains functions to scrap data
"""


"""
    Description:
        Get all articles links from a given url
    Parameters:
        url: string
        selector: string
        cloudflare: boolean. If true, use cloudscraper to bypass cloudflare protection
    Return:
        links: list
"""
def get_articles_links(url, selector, cloudflare=False):
    try:
        links = []
        if(cloudflare):
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.find_all(selector)
                for article in articles:
                    a_elements = article.find_all('a')
                    if(len(a_elements) != 0):
                        link = a_elements[0].get('href')
                        links.append(url + "/" + link)
        else:
            session = HTMLSession()
            page = session.get(url)
            articles = page.html.find(selector)
            for article in articles:
                new = article.find('a')
                link = new[0].absolute_links
                links.append(link)
        return links
    except Exception as e:
        print(e)
        return e

"""
    Description:
        Get text from a given url and a given selector (tag)
    Parameters:
        url: string
        selector: string
        cloudflare: boolean. If true, use cloudscraper to bypass cloudflare protection
        cloudflare_class: boolean. If true, use class_ instead of tag
    Return:
        text: string
"""
def find_tag(url, selector, cloudflare=False, cloudflare_class=False):
    try:
        text = ""
        if(cloudflare):
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                if cloudflare_class:
                    text = soup.find(class_=selector)
                else:
                    text = soup.find(selector)
        else:
            session = HTMLSession()
            page = session.get(url)
            text = page.html.find(selector)
        return text
    except Exception as e:
        print(e)
        return e

"""
    Description:
        Get text from a given text and a given selector (tag)
    Parameters:
        text: string
        selector: string
        cloudflare: boolean. If true, use cloudscraper to bypass cloudflare protection
        cloudflare_class: boolean. If true, use class_ instead of tag
    Return:
        text: string
"""
def find_tag_text(text, selector, cloudflare=False, cloudflare_class=False):
    try:
        if cloudflare:
            if cloudflare_class:
                extract_text = text.find_all(class_=selector)
            else:
                extract_text = text.find_all(selector)
        else:
            extract_text = text.find(selector)
        return extract_text
    except Exception as e:
        print(e)
        return e

"""
    Description:
        Get text from a given text and a given selector (tag)
    Parameters:
        text: string
        selector: string
        cloudflare: boolean. If true, use cloudscraper to bypass cloudflare protection
        cloudflare_class: boolean. If true, use class_ instead of tag
    Return:
        text: string
"""
def get_text_from_tag(url, selector, cloudflare=False, cloudflare_class=False):
    try:
        text = find_tag(url, selector, cloudflare=False, cloudflare_class=False)
        if(len(text) == 0):
            return ""
        else:
            return text[0].text
    except Exception as e:
        print(e)
        return e