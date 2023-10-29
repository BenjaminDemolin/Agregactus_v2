import Common.aa_webscrapping_function as webscrapping_f

from dotenv import dotenv_values

secret = dotenv_values(".env")

# URL = "https://fr.investing.com/news/latest-news"

# #print(webscrapping_f.get_articles_links(URL,"article",True))

# URL = "https://www.france24.com/fr/info-en-continu/"

# print(webscrapping_f.get_articles_links(URL,".news__content"))

# URL = "https://www.france24.com/fr/info-en-continu/20230906-wall-street-termine-en-baisse-prises-de-b%C3%A9n%C3%A9fices-sur-un-march%C3%A9-sans-entrain"

# print(webscrapping_f.find_tag(URL,"article")[0].text)

# URL = "https://fr.investing.com/news/economy/crash-boursier-et-recession-au-printemps-selon-david-rosenberg-2205503"

# text = webscrapping_f.find_tag(URL,"WYSIWYG articlePage",True,True)

# array = webscrapping_f.find_tag_text(text,"p",True)

# for a in array:
#     print(a.text)

import Webscrapping.aa_webscrapping_francetvinfo_function as francetvinfo_f

#print(francetvinfo_f.get_article_text("https://www.francetvinfo.fr/faits-divers/police/ce-que-l-on-sait-de-la-collision-mortelle-entre-un-adolescent-en-deux-roues-et-une-voiture-de-police-dans-les-yvelines_6048275.html"))
#print(francetvinfo_f.get_all_articles())

import Webscrapping.aa_webscrapping_france24_function as france24_f

#print(france24_f.get_all_articles())
#print(str(france24_f.get_all_articles()[0]).strip("{").strip("}").strip("'"))
article = france24_f.get_article_text(str(france24_f.get_all_articles()[0]).strip("{").strip("}").strip("'")).strip(" ")
print(article)

import Database.aa_global_database_function as globaldb_f

#globaldb_f.Postgres_db("xxx","xxx","xxx","xxx",1000)

import Database.aa_local_database_function as localdb_f


#print(localdb_f.reset_tables())
#print(localdb_f.delete_tables())
#print(localdb_f.create_tables())
#localdb_f.insert_row_websites_table("france24","https://www.france24.com/fr/info-en-continu/")
#print(localdb_f.get_website_id("france24"))
#localdb_f.insert_row_websites_table("francetvinfo","https://www.francetvinfo.fr/")

#print(localdb_f.insert_row_news_table("France24","https://www.france24.com/fr/info-en-continu/20230906-wall-street-termine-en-baisse-prises-de-b%C3%A9n%C3%A9fices-sur-un-march%C3%A9-sans-entrain"))
#print(localdb_f.update_row_news_table("https://www.france24.com/fr/info-en-continu/20230906-wall-street-termine-en-baisse-prises-de-b%C3%A9n%C3%A9fices-sur-un-march%C3%A9-sans-entrain",content="tgztgz",ia_tweet="qfvdfv"))

import Webscrapping.aa_webscrapping_news_function as news_f

#articles = aawebscrf.get_all_articles()

#print(articles)
#print(localdb_f.row_exists_news_table("https://www.france24.com/fr/info-en-continu/20230906-wtreet-termine-en-baisse-prises-de-b%C3%A9n%C3%A9fices-sur-un-march%C3%A9-sans-entrain"))
#articles = news_f.get_all_articles()
#print(articles)
#print(str(articles['france24'][0]).strip("{").strip("}").strip("'"))
#print(france24_f.get_article_text(str(articles['france24'][0]).strip("{").strip("}").strip("'")))
#news_f.add_articles_to_database(articles)

#text = france24_f.get_article_text(str(articles['france24'][0]).strip("{").strip("}").strip("'"))

import Common.aa_openai_function as openai_f
#print(openai_f.resume_article_chatgpt(text))
#print(openai_f.article_category_chatgpt(text))

import Common.aa_mail_function as mail_f

#mail_f.send_email(secret["SENDER_EMAIL"],secret["SENDER_PASSWORD"],secret["RECEIVER_EMAIL"],"test","test")


print("------")
print("------")
print("------")




# Example usage
text_to_summarize = article
summary = webscrapping_f.summarize_text(text_to_summarize)
print(summary)
