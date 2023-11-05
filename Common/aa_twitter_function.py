from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
import time
import pyperclip

class Twitter:

    def __init__(self, email, username, password, sleep_time,os ='linux', profile='',firefox_binary_location = '/usr/bin/firefox'):
        self.email = email
        self.username = username
        self.password = password
        self.os = os.lower
        self.sleep_time = int(sleep_time)
        # Define browser options
        firefox_options = Options()
        if(self.os == 'linux'):
            firefox_options.binary_location = firefox_binary_location
        firefox_options.profile = webdriver.FirefoxProfile(profile)
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()
        # Define WebDriverWait
        self.wait = WebDriverWait(self.driver, 30)
        time.sleep(self.sleep_time)

    def open_twitter(self):
        print("---open_twitter---")
        # Open Twitter login page
        self.driver.get('https://www.twitter.com/login')
        self.wait.until(EC.title_contains("X"))
        time.sleep(self.sleep_time)

    def login_email(self):
        print("---login_email---")
        # Enter email
        email_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "text")))
        email_input.send_keys(self.email)
        # Click on the 'Suivant' button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Suivant') or contains(.,'Next')]"))).click()
        time.sleep(self.sleep_time)

    def login_username(self):
        print("---login_username---")
        # Enter username 
        username_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "text")))
        username_input.send_keys(self.username)
        
        # Click on the 'Suivant' button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Suivant') or contains(.,'Next')]"))).click()
        time.sleep(self.sleep_time)
    
    def login_password(self):
        print("---login_password---")
        # Enter password
        password_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input.send_keys(self.password)

        # Click on the 'Se connecter' button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'connecter') or contains(.,'Log in')]"))).click()
        time.sleep(self.sleep_time)

    def tweet(self, tweet):
        print("---tweet---")

        # Click on the 'Quoi de neuf ?' button
        actions = ActionChains(self.driver)
        actions.send_keys('n')
        actions.perform()
        time.sleep(self.sleep_time)

        # Copy content to paste
        if(self.os == 'LINUX'):
            subprocess.run(['xclip', '-selection', 'clipboard'], input=tweet.encode('utf-8'))
        else:
            pyperclip.copy(tweet)

        
        # Paste content in the input field
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(self.sleep_time)

        # Press Enter to send the tweet
        actions.key_down(Keys.CONTROL).send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(self.sleep_time)

    def quit(self):
        print("---quit---")
        self.driver.quit()

    def auto_tweet(self, tweet):
        self.open_twitter()
        if("Connectez‑vous à&nbsp;X" in self.driver.page_source or "Sign in to X" in self.driver.page_source):
            self.login_email()
            if ("Entrez votre adresse email ou votre nom d'utilisateur" in self.driver.page_source or "Enter your email address or username" in self.driver.page_source):
                self.login_username()
            self.login_password()
        self.tweet(tweet)
        self.quit()