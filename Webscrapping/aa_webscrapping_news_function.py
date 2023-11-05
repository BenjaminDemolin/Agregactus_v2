from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
import heapq
import nltk
from datetime import datetime, timezone
import Webscrapping.aa_webscrapping_france24_function as france24_f
import Webscrapping.aa_webscrapping_francetvinfo_function as francetvinfo_f
import Database.aa_local_database_function as localdb_f
import Common.aa_openai_function as openai_f

"""
    File name: aa_webscrapping_news_function.py
    Description: This file contains functions to extract data from news websites
"""

"""
    Description: 
        This function returns all articles links from all websites. 
    Parameters:
        num_articles : int
    Return:
        dict_articles: dict
"""
def get_all_articles(num_articles = 20):
    try:
        dict_articles = {}
        dict_articles["france24".lower()] = france24_f.get_all_articles(num_articles)
        dict_articles["francetvinfo".lower()] = francetvinfo_f.get_all_articles(num_articles)
        return dict_articles
    except Exception as e:
        print(e)
        return e

"""
    Description:
        This function adds articles url to the database
    Parameters:
        dict_articles: dict
    Return:
        None
"""
def add_articles_to_database(dict_articles):
    try:
        for website in dict_articles:
            for article in dict_articles[website]:
                article = next(iter(article))
                if not localdb_f.row_exists_news_table(article):
                    localdb_f.insert_row_news_table(website, article)
    except Exception as e:
        print(e)
        return e

"""
    Description:
        Summarize a given text
    Parameters:
        text: string
        num_sentences: integer
    Return:
        summary_sentences: string
"""
def summarize_text(text, num_sentences=5):
    nltk.download('punkt')
    nltk.download('stopwords')
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('french'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Calculate word frequencies
    word_freq = FreqDist(filtered_words)

    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word, freq in word_freq.items():
            if word in sentence.lower():
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = freq
                else:
                    sentence_scores[sentence] += freq

    # Get the summary sentences with the highest scores
    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

    return ' '.join(summary_sentences)

def drop_first_last_character(input_string):
    if input_string[0] == '"' and input_string[-1] == '"':
        modified_string = input_string[1:-1]
        return modified_string
    else:
        return input_string

def summarize_all_articles():
    try:
        links_articles = localdb_f.get_uncompleted_articles_links()
        print("links_articles : " + str(len(links_articles)))
        for link in links_articles:
            link = link[0]
            if("france24" in link):
                article = france24_f.get_article_text(link)
            if("francetvinfo" in link):
                article = francetvinfo_f.get_article_text(link)
            article = summarize_text(article)
            # replace ' by '' for sql otherwise it will not work
            tweet = openai_f.article_to_tweet_chatgpt(article)
            tweet = drop_first_last_character(tweet)
            current_utc_time = datetime.now(timezone.utc)
            date = int(current_utc_time.timestamp())
            print("- " + tweet)
            if("Rate limit reached" not in tweet):
                localdb_f.update_tweet_news_table(link,ia_tweet=tweet,date=date)
            else:
                print("Rate limit reached")
                return False
        return True
    except Exception as e:
        print(e)
        return e
    
def summarize_all_questions():
    try:
        articles = localdb_f.get_uncompleted_questions_links()
        print("articles : " + str(len(articles)))
        for article in articles:
            link = article[0]
            tweet = article[1]
            question = openai_f.article_question_chatgpt(tweet)
            print("- " +question)
            if("Rate limit reached" not in question):
                localdb_f.update_question_news_table(link,question=question)
            else:
                print("Rate limit reached")
                return False
        return True
    except Exception as e:
        print(e)
        return e
    