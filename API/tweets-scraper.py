"""
# --- Import dependencies ---
import selenium
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# driver = webdriver.Chrome(ChromeDriverManager().install())

PATH = "/Users/vanessa/Documents/dev_projects/github_projects/Presidential_Sentiment_Analysis/API/chromedriver"

# Create a Service object and pass it to the webdriver
#service = Service(PATH)
#driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(PATH)
driver.get("https://nytimes.com")

"""

from selenium import webdriver
import os
import time
import datetime
import csv

import pandas as pd

#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class tweets_scraper:
    
    
    # constructore
    def __init__(self, username, password, subject, isHashtag):
        
        self.username = username
        self.password = password
        self.subject = subject
        self.isHashtag = isHashtag
        
        

        option = webdriver.ChromeOptions()
        
        option.add_experimental_option("detach", True)
        option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(options = option )

        self.by = By
        self.ec = EC
        self.webDriverWait = WebDriverWait

        time.sleep(1)
        self.login()
        
        time.sleep(2)
        self.search_subject()
        
        time.sleep(10)
        self.collect_tweets()
        

    # --- Set-Up Login ---   
    def login(self):
        self.driver.get('https://x.com/i/flow/login')
       
        # Wait for the page to load and locate the username input fields
        self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.XPATH, "//input[@name='text']")))
        
        # Send keys to the input fields
        self.driver.find_element(self.by.XPATH,  "//input[@name='text']").send_keys(self.username)
        
        # Locate the next button and click 
        self.webDriverWait(self.driver, 10).until(self.ec.element_to_be_clickable((self.by.XPATH, "//span[contains(text(), 'Next')]")))
        self.driver.find_element(self.by.XPATH, "//span[contains(text(), 'Next')]").click()
        time.sleep(5)
        
        # Wait for the page to laod and locate the password input fields
        self.webDriverWait(self.driver, 10).until(self.ec.presence_of_element_located((self.by.XPATH, "//input[@name='password']")))
        #self.webDriverWait(self.driver, 10).until(self.ec.presence_of_element_located((self.by.NAME, 'password')))
        self.driver.find_element(self.by.NAME, 'password').send_keys(self.password)
        
        # Locate login button 
        #sleep(2)
        self.webDriverWait(self.driver, 5).until(self.ec.element_to_be_clickable((self.by.XPATH, "//span[contains(text(), 'Log in')]")))
        self.driver.find_element(self.by.XPATH, "//span[contains(text(), 'Log in')]").click()
        
    # --- Search for a designated user or hashtag and fetch ---   
    def search_subject(self):
        # wait and find search box 
        #self.webDriverWait(self.driver,20).until(self.ec.presence_of_element_located((self.by.XPATH,"//input[@data-testid='SearchBox_Search_Input']")))
        
        # if we search a hastag type, search it in the search box 
        if(self.isHashtag == True): 
            self.driver.find_element(self.by.CSS_SELECTOR, 'input[name="text"]').send_keys(self.subject)
            self.driver.find_element(self.by.CSS_SELECTOR, 'input[name="text"]').send_keys(Keys.RETURN)
        # else if it a user, go directly to the subjects profile
        else:
            self.driver.get('https://x.com/' + self.subject)
        
        #look up the hastag  
          
    
    def collect_tweets(self):
        
        user_tags = []
        time_stamps = []
        tweets = []
        replies =[]
        retweets = []
        likes = []  
        
        # find elements of the tweet
        articles = self.driver.finde_element(self.by.XPATH, "//article[@data-testid = 'tweet']")
        
        while(True):
            for articles in articles:
                # grabs retweets and tweet replies , need to find a way to distinguish
                # authors own tweets, retewets, replie type 
                user_tag = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'User-Name']").text
                user_tags.append(user_tag)

                # collect timestamp 
                timestamp = self.driver.find_element(self.by.XPATH, ".//time[@datetime]").get_attribute('datetime')
                # or 
                #timestampe = sefl.driver.find_element(self.by.TAG_NAME, "time").get_attribute('datetime')
                time_stamps.append(timestamp)

                # collect tweet text
                tweet_text = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'tweetText']").text
                tweets.append(tweet_text)

                # collect replies_count
                replies_count = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'reply']").text
                replies.apppend(replies_count)

                # collect retweet_count
                retweet_count = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'retweet']").text
                retweets.append(retweet_count)

                # collect like_count
                like_count = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'like']").text
                likes.append(like_count)


            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            articles = self.driver.finde_element(self.by.XPATH, "//article[@data-testid = 'tweet']")
            tweets_update = list(set(tweets))
            if len(tweets_update) > 5 :
                break
    
    # TO DO: function that distinguies tweet, repost, reply tweet,         
    # def label_text_type
            
    # create csv          
    def export_to_csv(self):
        
        # create dataframe
        tweets_dataframe = pd.DataFrame(zip(user_tags, timestamps, tweets, replies, retweets, likes ),
                     columns = ['user_name', 'timestamp', 'tweet_text', 'replies_count', 'retweet_count', 'like_count'])
        
        # export as csv
        # os.makedirs('Users/vanessa/Documents/dev_projects/github_projects/Presidential_Sentiment_Analysis/', exist_ok=True) 
        
        tweets_dataframe.to_csv('Users/vanessa/Documents/dev_projects/sentiment_data_folder/tweets_data.csv', index=False)  
          
        
    
# Automate the Process 

# Export to Excel

# items/list of things we want to push to excel


'''
Eventually
want to feed in  password, username, array of hastags to be interatively go trough and find the top tweets,
array of users to find the tweets of the user
Ideally we do not want to manually change the function arguments 

OUTPUT: 
excel sheet
1. user tweets
2. 
'''
tweets = tweets_scraper( username="vactivez", password='2570cflmmo', subject="realDonaldTrump", isHashtag = False)


# XPATH for tweets that were replied to : //div[@data-testid='tweetText' and ancestor::div[@role='link']]
# XPATH 



