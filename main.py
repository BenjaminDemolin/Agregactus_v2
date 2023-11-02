from dotenv import dotenv_values
import datetime as dt
import Database.aa_local_database_function as localdb_f
import Webscrapping.aa_webscrapping_news_function as webscrapping_f
import Common.aa_mail_function as mail_f
import Common.aa_twitter_function as twitter_f
import Common.aa_openai_function as openai_f

secret = dotenv_values(".env")

def verify_database():
    if(localdb_f.table_websites_exists() == False):
        localdb_f.create_websites_table()
    if(localdb_f.table_main_category_exists() == False):
        localdb_f.create_main_category_table()
    if(localdb_f.table_news_exists() == False):
        localdb_f.create_news_table()
    if(localdb_f.table_configuration_exists() == False):
        localdb_f.create_configuration_table()
    if(len(localdb_f.get_all_websites()) == 0):
        localdb_f.init_websites_table()
    if(len(localdb_f.get_all_configuration()) == 0):
        localdb_f.init_configuration_table()
    

def format_tweet(tweet, source):
    return tweet + "\n(source : " + source + ")"

def send_email():
    try:
        data = localdb_f.get_article_to_send_by_email()
        for article in data:
            website_id = article[0]
            name = localdb_f.get_website_name_by_id(website_id)
            url = article[1]
            tweet = format_tweet(article[2], name)
            question = article[3]
            body = "url : \n" + url + "\n\n\n" + "tweet : \n" + tweet + "\n\n\n" + "question : \n" + question
            mail_sent = mail_f.send_email(secret["SENDER_EMAIL"], secret["SENDER_PASSWORD"], secret["RECEIVER_EMAIL"], url, body)
            if(mail_sent):
                localdb_f.update_email_sent_news_table(url)
    except Exception as e:
        print(e)
        return False

def tweet():
    tweet_every_x_minutes = int(localdb_f.get_configuration_value_by_name("tweet_every_x_minutes"))
    last_tweet_date = int(localdb_f.get_configuration_value_by_name("last_tweet_date"))
    current_timestamp = int(dt.datetime.now().timestamp())
    
    if(current_timestamp - last_tweet_date > tweet_every_x_minutes * 60):
        tweet_list = localdb_f.get_tweet_since_date(last_tweet_date)
        if(len(tweet_list) == 0):
            print("no tweet to send")
            return False
        # if only one tweet, no need to compare
        if(len(tweet_list) == 1):
            best_tweet_info = tweet_list[0]
        else:
            best_tweet_info = openai_f.get_best_tweet(tweet_list)

        if(best_tweet_info == False):
            print("Rate limit reached")
            return False
        else:
            website_id = best_tweet_info[0]
            name = localdb_f.get_website_name_by_id(website_id)
            url = best_tweet_info[1]
            tweet = best_tweet_info[2] + "\n(source : " + name + ")"
            twitter_obj = twitter_f.Twitter(secret["TWITTER_EMAIL"], secret["TWITTER_USERNAME"], secret["TWITTER_PASSWORD"], secret["FIREFOX_PROFILE"])
            twitter_obj.auto_tweet(tweet)
            localdb_f.update_configuration_value_by_name("last_tweet_date", current_timestamp)
            localdb_f.update_tweet_sent_news_table(url)
            return True

def main():
    # check if database are good
    print("----VERIFY DATABASE----")
    verify_database()

    # get article list, parameter is the number of articles to get by website
    print("----GET ARTICLES----")
    dict_articles = webscrapping_f.get_all_articles(1)

    #  add articles url to database
    print("----ADD ARTICLES TO DATABASE----")
    webscrapping_f.add_articles_to_database(dict_articles)

    # if chatgpt limit is not reached, summarize all articles and add in database
    print("----SUMMARIZE ALL ARTICLES----")
    webscrapping_f.summarize_all_articles()
    
    print("--TWEET--")
    if(tweet()):
        print("tweeted")
    else:
        print("not tweeted")



if __name__ == "__main__":
    main()