from dotenv import dotenv_values
import Database.aa_local_database_function as localdb_f
import Webscrapping.aa_webscrapping_news_function as webscrapping_f
import Common.aa_mail_function as mail_f

secret = dotenv_values(".env")

def verify_database():
    if(localdb_f.table_websites_exists() == False):
        localdb_f.create_websites_table()
    if(localdb_f.table_main_category_exists() == False):
        localdb_f.create_main_category_table()
    if(localdb_f.table_news_exists() == False):
        localdb_f.create_news_table()
    if(len(localdb_f.get_all_websites()) == 0):
        localdb_f.init_websites_table()

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

    # summarize all questions of all tweets in database
    print("----SUMMARIZE ALL QUESTIONS----")
    limit_not_reached = webscrapping_f.summarize_all_questions()

    # if chatgpt limit is not reached, summarize all articles and add in database
    print("----SUMMARIZE ALL ARTICLES----")
    if(limit_not_reached):
        webscrapping_f.summarize_all_articles()
    else:
        print("limit reached")

    # send email
    print("----SEND EMAIL----")
    send_email()


if __name__ == "__main__":
    main()