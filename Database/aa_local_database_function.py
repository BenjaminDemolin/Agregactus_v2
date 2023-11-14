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

def create_configuration_table():
    try:
        connector.create_table(TABLE_CONFIGURATION_NAME,TABLE_CONFIGURATION_COLUMNS)
        return True
    except Exception as e:
        print(e)
        return False

def create_tables():
    try:
        create_websites_table()
        create_news_table()
        create_configuration_table()
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

def reset_configuration_table():
    try:
        connector.reset_table(TABLE_CONFIGURATION_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def reset_tables():
    try:
        reset_configuration_table()
        reset_news_table()
        reset_websites_table()
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

def delete_configuration_table():
    try:
        connector.delete_table(TABLE_CONFIGURATION_NAME)
        return True
    except Exception as e:
        print(e)
        return False

def delete_tables():
    try:
        delete_configuration_table()
        delete_news_table()
        delete_websites_table()
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

def insert_row_configuration_table(name,value):
    try:
        return connector.insert_row(TABLE_CONFIGURATION_NAME,"name,value","'%s','%s'" % (name,value))
    except Exception as e:
        print(e)
        return False

def get_all_websites():
    try:
        return connector.select_rows(TABLE_WEBSITES_NAME)
    except Exception as e:
        print(e)
        return False

def get_all_configuration():
    try:
        return connector.select_rows(TABLE_CONFIGURATION_NAME)
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

def get_configuration_value_by_name(name):
    try:
        return connector.select_rows(TABLE_CONFIGURATION_NAME,"value","name = '%s'" % (name))[0][0]
    except Exception as e:
        print(e)
        return False
    
def insert_row_news_table(website_name,url,ia_tweet=None,date=None):
    try:
        website_id = get_website_id_by_name(website_name)[0][0]
        if ia_tweet is None:
            ia_tweet = "NULL"
        if date is None:
            date = "NULL"
        return connector.insert_row(TABLE_NEWS_NAME,"website_id,url,ia_tweet,date","%s,'%s','%s',%s" % (website_id,url,ia_tweet,date))
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

def update_configuration_value_by_name(name,value):
    try:
        return connector.update_row(TABLE_CONFIGURATION_NAME,"value = '%s'" % (value),"name = '%s'" % (name))
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
    
def table_configuration_exists():
    try:
        return connector.check_table_exists(TABLE_CONFIGURATION_NAME)
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

def init_configuration_table():
    try:
        for configuration in TABLE_CONFIGURATION_INIT:
            insert_row_configuration_table(configuration[0],configuration[1])
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

def update_tweet_sent_news_table(url):
    try:
        return connector.update_row(TABLE_NEWS_NAME,"tweet_sent = TRUE","url = '%s'" % (url))
    except Exception as e:
        print(e)
        return False

def get_tweet_since_date(date_timestamp):
    try:
        return connector.select_rows(TABLE_NEWS_NAME,columns='website_id,url,ia_tweet',condition="ia_tweet != 'NULL' AND date > %s" % (date_timestamp))
    except Exception as e:
        print(e)
        return False