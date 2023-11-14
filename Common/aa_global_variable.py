from dotenv import dotenv_values

secret = dotenv_values(".env")

"""
    This file contains all the global variables used in the project
"""

"""
    Website table. Contains the list of websites to scrap
"""
TABLE_WEBSITES_NAME = "websites"
TABLE_WEBSITES_COLUMNS = "website_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE,url TEXT NOT NULL UNIQUE"
TABLE_WEBSITES_INIT = [["france24","https://www.france24.com/fr/info-en-continu/"],
                       ["francetvinfo","https://www.francetvinfo.fr/"]]

"""
    News table. Contains the list of news scrapped
"""
TABLE_NEWS_NAME = "news"
TABLE_NEWS_COLUMNS = " news_id SERIAL PRIMARY KEY, website_id INT REFERENCES websites (website_id), url TEXT NOT NULL UNIQUE, ia_tweet TEXT, date BIGINT, tweet_sent BOOLEAN DEFAULT FALSE"

"""
    Configuration table. Contains the configuration of the bot
"""
TABLE_CONFIGURATION_NAME = "configuration"
TABLE_CONFIGURATION_COLUMNS = "configuration_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE, value TEXT NOT NULL"
TABLE_CONFIGURATION_INIT = [["tweet_every_x_minutes",secret["TIME_BETWEEN_TWEETS_IN_MINUTES"]],
                     ["last_tweet_date","0"]]