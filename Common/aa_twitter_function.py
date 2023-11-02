from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip

class Twitter:

    def __init__(self, email, username, password, options=''):
        self.email = email
        self.username = username
        self.password = password
        # Define browser options
        firefox_options = Options()
        firefox_options.profile = webdriver.FirefoxProfile(options)
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()
        # Define WebDriverWait
        self.wait = WebDriverWait(self.driver, 30)

    def open_twitter(self):
        print("---open_twitter---")
        # Open Twitter login page
        self.driver.get('https://www.twitter.com/login')
        time.sleep(5)

    def login_email(self):
        print("---login_email---")
        # Enter email
        email_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "text")))
        email_input.send_keys(self.email)
        # Click on the 'Suivant' button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Suivant')]"))).click()
        time.sleep(5)

    def login_username(self):
        print("---login_username---")
        # Enter username 
        username_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "text")))
        username_input.send_keys(self.username)
        
        # Click on the 'Suivant' button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'Suivant')]"))).click()
        time.sleep(5)
    
    def login_password(self):
        print("---login_password---")
        # Enter password
        password_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input.send_keys(self.password)

        # Click on the 'Se connecter' button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(.,'connecter')]"))).click()
        time.sleep(5)

    def tweet(self, tweet):
        print("---tweet---")

        # Click on the 'Quoi de neuf ?' button
        actions = ActionChains(self.driver)
        actions.send_keys('n')
        actions.perform()
        time.sleep(5)

        # Copy content to paste
        pyperclip.copy(tweet)

        # Paste content in the input field
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL)
        actions.perform()
        time.sleep(5)

        # Press Enter to send the tweet
        actions.key_down(Keys.CONTROL).send_keys(Keys.RETURN)
        actions.perform()
        time.sleep(5)

    def quit(self):
        print("---quit---")
        self.driver.quit()

    def auto_tweet(self, tweet):
        self.open_twitter()
        if("Connectez‑vous à&nbsp;X" in self.driver.page_source):
            self.login_email()
            if "Entrez votre adresse email ou votre nom d'utilisateur" in self.driver.page_source:
                self.login_username()
            self.login_password()
        self.tweet(tweet)
        self.quit()