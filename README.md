# Agregactus V2.0

## Overview

Agregactus is your go-to tool for effortlessly staying informed and sharing summarized news on social media. It not only scrapes news websites, summarizes articles, and generates tweets but also poses insightful questions alongside. All of this is neatly stored in a PostgreSQL database and sent via email.

## Features
* Web Scraping: Extracts the latest news from specified websites.
* Summarization: Condenses articles while retaining key information.
* ChatGPT Integration: Crafts engaging tweets and questions using ChatGPT.
* Database Storage: Utilizes PostgreSQL to store tweet and question data.
* Configurability: Easily configurable through a .env file for email, OpenAI key, and database information.
* Automated tweeting: Tweets are automatically generated and posted at specified intervals.

## Getting Started

### Prerequisites
Python 3.x
PostgreSQL (can use Docker image)
Dependencies listed in requirements.txt

### Installation
Clone the repository:

```bash
git clone https://github.com/BenjaminDemolin/Agregactus_v2.git
cd Agregactus_v2
pip install -r requirements.txt
```

#### For Ubuntu 

This link can help you to install Firefox on Ubuntu (default firefox installation is not always working):
https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04#:%7E:text=Installing%20Firefox%20via%20Apt%20(Not%20Snap)&text=You%20add%20the%20Mozilla%20Team,%2C%20bookmarks%2C%20and%20other%20data.
Default Firefox profile path : /home/username/.mozilla/firefox/xxxxxxxx.default-release
Default Firefox binary location : /usr/bin/firefox

xclip is also required for Linux:
```bash
sudo apt-get install xclip
```

### Env file configuration

Create a .env file in the root directory of the project and fill it with the following information:

```bash
DB_HOST|DB_NAME|DB_USER|DB_PASSWORD|DB_PORT = PostgreSQL database information.
OPENAI_API_KEY = OpenAI API key (https://platform.openai.com/api-keys).
TWITTER_EMAIL|TWITTER_USERNAME|TWITTER_PASSWORD = Twitter account information.
TWITTER_MAX_TWEET_SIZE = Maximum tweet size (280 characters for free accounts).
TIME_BETWEEN_TWEETS_IN_MINUTES = Time between tweets in minutes. Only used when create database.
OS = Operating system (Windows or Linux).
FIREFOX_PROFILE = Firefox profile path. Use to keep Twitter logged in.
FIREFOX_BINARY_LOCATION = Firefox binary location (only for Linux).
FIREFOX_SLEEP_TIME = Time to wait for Firefox to load in seconds between each action (when tweeting).
```

### Run Agregactus:

python main.py
