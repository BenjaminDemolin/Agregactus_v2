
TABLE_WEBSITES_NAME = "websites"
TABLE_WEBSITES_COLUMNS = "website_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE,url TEXT NOT NULL UNIQUE"
TABLE_WEBSITES_INIT = [["france24","https://www.france24.com/fr/info-en-continu/"],
                       ["francetvinfo","https://www.francetvinfo.fr/"]]

TABLE_MAIN_CATEGORY_NAME = "main_category"
TABLE_MAIN_CATEGORY_COLUMNS = "main_category_id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE"

TABLE_NEWS_NAME = "news"
TABLE_NEWS_COLUMNS = " news_id SERIAL PRIMARY KEY, website_id INT REFERENCES websites (website_id), url TEXT NOT NULL UNIQUE, ia_tweet TEXT, question TEXT, main_category_id INT REFERENCES main_category (main_category_id), date BIGINT, email_sent BOOLEAN DEFAULT FALSE"
