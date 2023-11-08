import openai
from dotenv import dotenv_values

secret = dotenv_values("./.env")
openai.api_key = secret["OPENAI_API_KEY"]

"""
    File name: aa_openai_function.py
    Description: This file contains functions to use openai api
"""

"""
    Description:
        Request openai api
    Parameters:
        content: string
        role: string
        model: string
        temperature: float
        max_tokens: int
        top_p: float
        frequency_penalty: float
        presence_penalty: float
    Return:
        chatgpt_content: string
"""
def openai_request(content, role="system", model="gpt-3.5-turbo", temperature=0.5, max_tokens=200, top_p=1, frequency_penalty=0, presence_penalty=0):
    try:
        response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
            "role": role,
            "content": content 
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
        )
        chatgpt_content = ""
        if(len(response['choices']) > 0):
            chatgpt_content = str(response['choices'][0]['message']['content']).replace("'", "''")
        return chatgpt_content
    except Exception as e:
        print(e)
        return e

"""
    Description:
        Use chatgpt to generate a tweet from a given article
    Parameters:
        article: string
    Return:
        response: string
"""
def article_to_tweet_chatgpt(article):
    try:
        return openai_request(content="Fait un tweet court et percutent en français en restant neutre à partir de l'article suivant : \n" + article)
        # return openai_request(content="Fait un tweet percutent en français en restant neutre à partir de l'article suivant : \n" + article)
    except Exception as e:
        print(e)
        return e
    
"""
    Description:
        Use chatgpt to categorize a given article
    Parameters:
        article: string
    Return:
        response: string
"""
def article_category_chatgpt(article):
    try:
        return openai_request(article + "\n\nclassifie le tweet dans un de ces types: actualités nationales et internationales, économie, culture, science, sports, environnement , faits divers, santé, technologie, politique. Retourne juste le type en réponse")
    except Exception as e:
        print(e)
        return e
    
"""
    Description:
        Use chatgpt to generate a question from a given article
    Parameters:
        article: string
    Return:
        response: string
"""
def article_question_chatgpt(article):
    try:
        return openai_request("Pose une question ouverte sur le tweet suivant : \n\n" + article)
    except Exception as e:
        print(e)
        return e

def get_best_tweet(tweet_list, tweet_size=260):
    try:
        print("---ask openai for best tweet---")
        i = 1
        nb_tweet_valid = 0
        index_only_one_tweet = -1
        body = "Retourne juste le numéro du tweet le plus important parmi les suivants : \n\n"
        #body = "Retourne juste le numéro du tweet le plus important parmi les suivants en priviligient les conflits puis la polique puis les faits divers : \n\n"
        for tweet in tweet_list:
            openai_tweet = tweet[2]
            # if tweet is inferior to max size then add it to the body
            if(len(openai_tweet) < tweet_size):
                body += str(i) + " : " + openai_tweet + "\n\n"
                nb_tweet_valid += 1
                index_only_one_tweet = i-1
            i += 1
        # if no tweet is inferior to max size then return false
        if(nb_tweet_valid == 0):
            return -2
        if(nb_tweet_valid == 1):
            return tweet_list[index_only_one_tweet]
        # else ask openai for the best tweet
        tweet_number = openai_request(body,temperature=0,max_tokens=100)
        number = -3
        # if openai return a valid tweet number then return the tweet (not Rate limit reached)
        if(isinstance(tweet_number, str)):
            print("openai best tweet : " + tweet_number)
            for i in range(len(tweet_list), 0, -1):
                if(str(i) in tweet_number):
                    number = i
                    break
            if(number == -3):
                return -3
            else:
                return tweet_list[number - 1]
        else:
            return -1
    except Exception as e:
        print(e)
        return e