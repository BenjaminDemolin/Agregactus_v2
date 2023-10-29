from dotenv import dotenv_values
import Database.aa_global_database_function as globaldb_f
from Common.aa_global_variable import *

secret = dotenv_values("./.env")

host = secret["DB_HOST"]
dbname = secret["DB_NAME"]
user = secret["DB_USER"]
password = secret["DB_PASSWORD"]
port = secret["DB_PORT"]


"""
    File name: aa_local_database_function.py
    Description: This file contains functions to interact with agregactus database
"""

connector = globaldb_f.Postgres_db(host,dbname,user,password,port)

def create_websites_table():
    try:
        connector.create_table(TABLE_WEBSITES_NAME,TABLE_WEBSITES_COLUMNS)
        return True
    except Exception as e:
        print(e)
        return False

def create_news_table():
    try:
        connector.create_table(TABLE_NEWS_NAME,TABLE_NEWS_COLUMNS)
        return True
    except Exception as e:
        print(e)
        return False

def create_main_category_table():
    try:
        connector.create_table(TABLE_MAIN_CATEGORY_NAME,TABLE_MAIN_CATEGORY_COLUMNS)
        return True
    except Exception as e:
        print(e)
        return False

def create_tables():
    try:
        connector.create_table(TABLE_WEBSITES_NAME,TABLE_WEBSITES_COLUMNS)
        connector.create_table(TABLE_NEWS_NAME,TABLE_NEWS_COLUMNS)
        connector.create_table(TABLE_MAIN_CATEGORY_NAME,TABLE_MAIN_CATEGORY_COLUMNS)
        return True
    except Exception as e:
        print(e)
        return False

def reset_websites_table():
    try:
        connector.reset_table(TABLE_WEBSITES_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def reset_news_table():  
    try:
        connector.reset_table(TABLE_NEWS_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def reset_main_category_table():
    try:
        connector.reset_table(TABLE_MAIN_CATEGORY_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def reset_tables():
    try:
        connector.reset_table(TABLE_WEBSITES_NAME)
        connector.reset_table(TABLE_NEWS_NAME)
        connector.reset_table(TABLE_MAIN_CATEGORY_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def delete_websites_table():
    try:
        connector.delete_table(TABLE_WEBSITES_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def delete_news_table():
    try:
        connector.delete_table(TABLE_NEWS_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def delete_main_category_table():
    try:
        connector.delete_table(TABLE_MAIN_CATEGORY_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def delete_tables():
    try:
        connector.delete_table(TABLE_WEBSITES_NAME)
        connector.delete_table(TABLE_NEWS_NAME)
        connector.delete_table(TABLE_MAIN_CATEGORY_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def insert_row_websites_table(name,url):
    try:
        return connector.insert_row(TABLE_WEBSITES_NAME,"name,url","'%s','%s'" % (name.lower(),url))
    except Exception as e:
        print(e)
        return False

def insert_row_main_category_table(name):
    try:
        return connector.insert_row(TABLE_MAIN_CATEGORY_NAME,"name","'%s'" % (name.lower()))
    except Exception as e:
        print(e)
        return False

def get_all_websites():
    try:
        return connector.select_rows(TABLE_WEBSITES_NAME)
    except Exception as e:
        print(e)
        return False

def get_website_url_by_name(name):
    try:
        return connector.select_rows(TABLE_WEBSITES_NAME,"url","name = '%s'" % (name.lower()))[0][0]
    except Exception as e:
        print(e)
        return False

def get_website_name_by_url(url):
    try:
        return connector.select_rows(TABLE_WEBSITES_NAME,"name","url = '%s'" % (url))[0][0]
    except Exception as e:
        print(e)
        return False
    
def get_website_name_by_id(website_id):
    try:
        return connector.select_rows(TABLE_WEBSITES_NAME,"name","website_id = %s" % (website_id))[0][0]
    except Exception as e:
        print(e)
        return False
    
def get_website_id_by_name(name):
    try:
        return connector.select_rows(TABLE_WEBSITES_NAME,"website_id","name = '%s'" % (name.lower()))
    except Exception as e:
        print(e)
        return False

def get_main_category_id(name):
    try:
        return connector.select_rows(TABLE_MAIN_CATEGORY_NAME,"main_category_id","name = '%s'" % (name.lower()))
    except Exception as e:
        print(e)
        return False

def insert_row_news_table(website_name,url,ia_tweet=None,question=None,main_category=None,date=None):
    try:
        website_id = get_website_id_by_name(website_name)[0][0]
        if ia_tweet is None:
            ia_tweet = "NULL"
        if question is None:
            question = "NULL"
        if main_category is None:
            main_category = "NULL"
        else:
            if(len(get_main_category_id(main_category)) == 0):
                main_category = "NULL"
            else:
                main_category = get_main_category_id(main_category)[0][0]
        if date is None:
            date = "NULL"
        return connector.insert_row(TABLE_NEWS_NAME,"website_id,url,ia_tweet,question,main_category_id,date","%s,'%s','%s','%s',%s,%s" % (website_id,url,ia_tweet,question,main_category,date))
    except Exception as e:
        print(e)
        return False
    
def update_row_website_table(name,url,new_name = None):
    try:
        website_id = get_website_id_by_name(name)[0][0]
        if(new_name is None):
            return connector.update_row(TABLE_WEBSITES_NAME,"url" ,"'%s'" % (url),"website_id = %s" % (website_id))
        else:
            return connector.update_row(TABLE_WEBSITES_NAME,"name,url" ,"'%s','%s'" % (new_name.lower(),url),"website_id = %s" % (website_id))
    except Exception as e:
        print(e)
        return False
    
def update_tweet_news_table(url,ia_tweet=None, date=None):
    try:
        if ia_tweet is None:
            ia_tweet = "NULL"
        if date is None:
            date = "NULL"
        return connector.update_row(TABLE_NEWS_NAME,"ia_tweet = '%s', date =%s" % (ia_tweet,date),"url = '%s'" % (url))
    except Exception as e:
        print(e)
        return False

def update_question_news_table(url,question=None):
    try:
        if question is None:
            question = "NULL"
        print("question")
        return connector.update_row(TABLE_NEWS_NAME,"question = '%s'" % (question),"url = '%s'" % (url))
    except Exception as e:
        print(e)
        return False

def row_exists_news_table(url):
    try:
        if(len(connector.select_rows(TABLE_NEWS_NAME,condition ="url = '%s'" % (url))) == 0):
            return False
        return connector.select_rows(TABLE_NEWS_NAME,condition ="url = '%s'" % (url))[0][0]
    except Exception as e:
        print(e)
        return False
    
def table_websites_exists():
    try:
        return connector.check_table_exists(TABLE_WEBSITES_NAME)
    except Exception as e:
        print(e)
        return False
    
def table_news_exists():
    try:
        return connector.check_table_exists(TABLE_NEWS_NAME)
    except Exception as e:
        print(e)
        return False
    
def table_main_category_exists():
    try:
        return connector.check_table_exists(TABLE_MAIN_CATEGORY_NAME)
    except Exception as e:
        print(e)
        return False
    
def init_websites_table():
    try:
        for website in TABLE_WEBSITES_INIT:
            insert_row_websites_table(website[0],website[1])
        return True
    except Exception as e:
        print(e)
        return False
    
def get_uncompleted_articles_links():
    try:
        return connector.select_rows(TABLE_NEWS_NAME,columns='url',condition="ia_tweet = 'NULL'")
    except Exception as e:
        print(e)
        return False
    
def get_uncompleted_questions_links():
    try:
        return connector.select_rows(TABLE_NEWS_NAME,columns='url,ia_tweet',condition="question = 'NULL' AND ia_tweet != 'NULL'")
    except Exception as e:
        print(e)
        return False
    
def get_article_to_send_by_email():
    try:
        return connector.select_rows(TABLE_NEWS_NAME,columns='website_id,url,ia_tweet,question',condition="email_sent = FALSE AND ia_tweet != 'NULL' AND question != 'NULL'")
    except Exception as e:
        print(e)
        return False
    
def update_email_sent_news_table(url):
    try:
        return connector.update_row(TABLE_NEWS_NAME,"email_sent = TRUE","url = '%s'" % (url))
    except Exception as e:
        print(e)
        return False
   