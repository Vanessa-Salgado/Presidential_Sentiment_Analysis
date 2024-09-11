"""
Purpose: Rewriting tweets-scrapper.py with the correct Class structure.
"""

from selenium import webdriver
import os
import time
import datetime
import csv

import pandas as pd
import argparse

#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class tweets_scraper:


    
    # -- Constructor ---
    def __init__(self, subject, isHashtag):
        
        # now a list of subjects
        self.subject = subject
        self.isHashtag = isHashtag
        
        self.user_tags = []
        self.time_stamps = []
        self.tweets = []
        self.replies = []
        self.retweets = []
        self.likes = []
        
        # set up driver connection
        option = webdriver.ChromeOptions()
        
        option.add_experimental_option("detach", True)
        option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(options = option )

        self.by = By
        self.ec = EC
        self.webDriverWait = WebDriverWait
        
        assert "Twitter" in self.driver.title
        
        

    # --- Set-Up Login ---   
    def login(self) :
        self.driver.get('https://x.com/i/flow/login')
       
        # Wait for the page to load and locate the username input fields
        self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.XPATH, "//input[@name='text']")))
        
        # Send keys to the input fields
        self.driver.find_element(self.by.XPATH,  "//input[@name='text']").send_keys(username)
        
        # Locate the next button and click 
        self.webDriverWait(self.driver, 10).until(self.ec.element_to_be_clickable((self.by.XPATH, "//span[contains(text(), 'Next')]")))
        self.driver.find_element(self.by.XPATH, "//span[contains(text(), 'Next')]").click()
        time.sleep(5)
        
        # Wait for the page to laod and locate the password input fields
        self.webDriverWait(self.driver, 10).until(self.ec.presence_of_element_located((self.by.XPATH, "//input[@name='password']")))
        #self.webDriverWait(self.driver, 10).until(self.ec.presence_of_element_located((self.by.NAME, 'password')))
        self.driver.find_element(self.by.NAME, 'password').send_keys(password)
        
        # Locate login button 
        #sleep(2)
        self.webDriverWait(self.driver, 5).until(self.ec.element_to_be_clickable((self.by.XPATH, "//span[contains(text(), 'Log in')]")))
        self.driver.find_element(self.by.XPATH, "//span[contains(text(), 'Log in')]").click()
        
    # --- Search for a designated user or hashtag and fetch ---   
    def search_subject(self, self.isHashtag,):
        # wait and find search box 
        #self.webDriverWait(self.driver,20).until(self.ec.presence_of_element_located((self.by.XPATH,"//input[@data-testid='SearchBox_Search_Input']")))
        
        # TO DO: look up the hastag  
        # if we search a hastag type, search it in the search box 
        if(self.isHashtag == True): 
            self.driver.find_element(self.by.CSS_SELECTOR, 'input[name="text"]').send_keys(self.subject)
            self.driver.find_element(self.by.CSS_SELECTOR, 'input[name="text"]').send_keys(Keys.RETURN)
        
        # else if subject is a user, go directly to the subjects profile
        else:
            self.driver.get('https://x.com/' + self.subject)
    
    def collect_tweets(self):
        
        # find elements of the tweet
        articles = self.driver.find_element(self.by.XPATH, "//article[@data-testid = 'tweet']")
        
        # Automate the Process 
        while(True):
            for articles in articles:
                # grabs retweets and tweet replies , need to find a way to distinguish
                # authors own tweets, retewets, replie type 
                user_tag = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'User-Name']").text
                self.user_tags.append(user_tag)

                # collect timestamp 
                timestamp = self.driver.find_element(self.by.XPATH, ".//time[@datetime]").get_attribute('datetime')
                # or 
                #timestampe = sefl.driver.find_element(self.by.TAG_NAME, "time").get_attribute('datetime')
                self.time_stamps.append(timestamp)

                # collect tweet text
                tweet_text = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'tweetText']").text
                self.tweets.append(tweet_text)

                # collect replies_count
                replies_count = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'reply']").text
                self.replies.apppend(replies_count)

                # collect retweet_count
                retweet_count = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'retweet']").text
                self.retweets.append(retweet_count)

                # collect like_count
                like_count = self.driver.find_element(self.by.XPATH, ".//div[@data-testid = 'like']").text
                self.likes.append(like_count)


            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # wait 
            articles = self.driver.find_elements(self.by.XPATH, "//article[@data-testid = 'tweet']")
            tweets_update = list(set(tweets))
            if len(tweets_update) > 5 :
                break
    
    # TO DO: function that distinguies tweet, repost, reply type      
    # def label_text_type(self):
            
    # create csv of tweets colleted          
    def export_to_csv(self):
        
        # create dataframe
        tweets_dataframe = pd.DataFrame(zip(user_tags, time_stamps, tweets, replies, retweets, likes ),
                     columns = ['user_name', 'timestamp', 'tweet_text', 'replies_count', 'retweet_count', 'like_count'])
        
        # export as csv
        # eventual path for data folder
        # os.makedirs('Users/vanessa/Documents/dev_projects/github_projects/Presidential_Sentiment_Analysis/', exist_ok=True) 
        
        # export as csv
        tweets_dataframe.to_csv('Users/vanessa/Documents/dev_projects/sentiment_data_folder/tweets_data.csv', index=False) 
        
 #  to pass an array of subjects directly from the terminal 
if __name__ == "__main__":
     # Set up argument parsing
    parser = argparse.ArgumentParser(description="Tweet Scraper")
    parser.add_argument("subjects", nargs='+', type=str, help="The subjects or hashtags to scrape tweets for (space-separated)")
    parser.add_argument("--hashtag", action="store_true", help="Indicate if the subjects are hashtags")

    args = parser.parse_args()

    # Instantiate Tweet_scraper with the command-line arguments
    scraper = tweets_scraper(args.subjects, args.hashtag)
    scraper.start_scraping()


'''
TO DO: 
Want to feed in  password, username, array of hastags | array of user @  to interatively go through and find the tweets
Ideally we do not want to manually change the function arguments 

OUTPUT: 
excel sheet
1. user tweets csv
2. hastag tweets csv
'''
# To Use Scraper, 
# Create a scraper object and build the the csv of data collected
# i.e.

# scraper object for a list of hastags
hashtags_tweets= tweets_scraper(subject=['#election', '#debate'], isHashtag = True)

# scraper object for a list of a users' @
users_tweets = tweets_scraper(subject=['realDonaldTrump', 'KamalaHarris'], isHashtag = False)


# directly into the terminal 
# 



