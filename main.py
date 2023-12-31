from dotenv import dotenv_values
import datetime as dt
import Database.aa_local_database_function as localdb_f
import Webscraping.aa_webscraping_news_function as webscraping_f
import Common.aa_twitter_function as twitter_f
import Common.aa_openai_function as openai_f
import time

secret = dotenv_values(".env")

"""
    File name: main.py
    Description: This file contains the main function
"""
       
"""
    Description:
        Verify if database are good
    Parameters:
        None
    Return:
        None
"""
def verify_database():
    if(localdb_f.table_websites_exists() == False):
        localdb_f.create_websites_table()
    if(localdb_f.table_news_exists() == False):
        localdb_f.create_news_table()
    if(localdb_f.table_configuration_exists() == False):
        localdb_f.create_configuration_table()
    if(len(localdb_f.get_all_websites()) == 0):
        localdb_f.init_websites_table()
    if(len(localdb_f.get_all_configuration()) == 0):
        localdb_f.init_configuration_table()
    
"""
    Description:
        Get best tweet and send it 
    Parameters:
        None
    Return:
        None
"""
def tweet():
    # init variables
    tweet_every_x_minutes = int(localdb_f.get_configuration_value_by_name("tweet_every_x_minutes"))
    last_tweet_date = int(localdb_f.get_configuration_value_by_name("last_tweet_date"))
    current_timestamp = int(dt.datetime.now().timestamp())
    best_tweet_info = False
    # if last tweet date is more than tweet_every_x_minutes, get best tweet and send it
    if(current_timestamp - last_tweet_date > tweet_every_x_minutes * 60):
        if(last_tweet_date > 0):
            last_tweet_date = last_tweet_date - tweet_every_x_minutes * 60 * 3
        tweet_list = localdb_f.get_tweet_since_date(last_tweet_date)
        # if no tweet to send, return false
        if(len(tweet_list) == 0):
            print("no tweet to send")
            return False
        # if only one tweet, no need to compare
        if(len(tweet_list) == 1 & len(tweet_list[0][2]) <= int(secret["TWITTER_MAX_TWEET_SIZE"])):
            best_tweet_info = tweet_list[0]
        else:
            best_tweet_info = openai_f.get_best_tweet(tweet_list, int(secret["TWITTER_MAX_TWEET_SIZE"]))
        # if best tweet is -1, it means that chatgpt limit is reached
        if(best_tweet_info == -1):
            print("Rate limit reached, try again later")
            return False
        # if best tweet is -2, it means that all tweet are too long
        elif(best_tweet_info == -2):
            print("no tweet to send (all tweet are too long)")
            localdb_f.update_configuration_value_by_name("last_tweet_date", current_timestamp)
            return False
        # if best tweet is -3, it means that chatgpt didn't return a valid tweet number
        elif(best_tweet_info == -3):
            print("ChatGPT didn't return a valid tweet number")
            localdb_f.update_configuration_value_by_name("last_tweet_date", current_timestamp)
            return False
        else:
            print("best tweet : " + str(best_tweet_info))
            website_id = best_tweet_info[0]
            name = localdb_f.get_website_name_by_id(website_id)
            url = best_tweet_info[1]
            #tweet = best_tweet_info[2] + "\n(source : " + name + ")"
            tweet = best_tweet_info[2]
            twitter_obj = twitter_f.Twitter(secret["TWITTER_EMAIL"], secret["TWITTER_USERNAME"], secret["TWITTER_PASSWORD"], secret["FIREFOX_SLEEP_TIME"],os=secret["OS"],profile=secret["FIREFOX_PROFILE"], firefox_binary_location=secret["FIREFOX_BINARY_LOCATION"])
            twitter_obj.auto_tweet(tweet)
            localdb_f.update_configuration_value_by_name("last_tweet_date", current_timestamp)
            localdb_f.update_tweet_sent_news_table(url)
            return True

"""
    Description:
        Main function
    Parameters:
        None
    Return:
        None
"""
def main():
    while True:
        # check if database are good
        print("----VERIFY DATABASE----")
        verify_database()
        # get article list, parameter is the number of articles to get by website
        print("----GET ARTICLES----")
        dict_articles = webscraping_f.get_all_articles(1)
        #  add articles url to database
        print("----ADD ARTICLES TO DATABASE----")
        webscraping_f.add_articles_to_database(dict_articles)
        # if chatgpt limit is not reached, summarize all articles and add in database
        print("----SUMMARIZE ALL ARTICLES----")
        if(webscraping_f.summarize_all_articles()):        
            print("--TWEET--")
            if(tweet()):
                print("tweeted")
            else:
                print("not tweeted")
            print("--WAIT 5 MINUTE | %s--" % (dt.datetime.now().strftime("%H:%M:%S")))
            time.sleep(60*5)
        else:
            print("--WAIT A MINUTE | %s--" % (dt.datetime.now().strftime("%H:%M:%S")))
            time.sleep(60)


if __name__ == "__main__":
    main()