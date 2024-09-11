"""
Purpose: tweets scraper to scrape tweets of a specific user or hashtag
"""

from selenium import webdriver
import time


import pandas as pd

#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class tweets_scraper:
    
    
    # Constructor
    def __init__(self, username, password, subject, isHashtag):
        
        self.username = username
        self.password = password
        self.subject = subject
        self.isHashtag = isHashtag
        
        self.user_tags = []
        self.time_stamps = []
        self.tweets = []
        self.replies = []
        self.retweets = []
        self.likes = []
         

        option = webdriver.ChromeOptions()
        
        option.add_experimental_option("detach", True)
        # option.add_argument("--headless=new") # testing purposes
        option.add_argument("--incognito") # avoiding tracking 
        option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(options = option )

        self.by = By
        self.ec = EC
        self.webDriverWait = WebDriverWait

        # time.sleep(1)
        
        self.login()
        
        # time.sleep(1)
        self.search_subject()
        
        time.sleep(10)
        self.collect_tweets()
        

    # --- Set-Up Login ---  WORKING
    def login(self):
        self.driver.get('https://x.com')
        print("twitter page opened ")
        self.driver.fullscreen_window()
        
        # wait for the page to load and locate the sign in button
        try:
            self.webDriverWait(self.driver, 20).until(self.ec.visibility_of_element_located((self.by.XPATH, "//span[contains(text(),'Sign in')][1]"))).click()
            print("sign in button located")
        except: 
            print("Exception occurred")
            
        
        # Wait for the page to load and locate the username input fields
        self.webDriverWait(self.driver, 10).until(self.ec.visibility_of_element_located((self.by.XPATH, "//div[@class='css-175oi2r r-18u37iz r-1pi2tsx r-1wtj0ep r-u8s1d r-13qz1uu']")))
        print("username field visible")
        
        # Send keys to the input fields
        self.driver.find_element(self.by.XPATH,  "//input[@name='text']").send_keys(self.username)
        print("username inputted")
        
        # Locate the next button and click 
        self.webDriverWait(self.driver, 10).until(self.ec.element_to_be_clickable((self.by.XPATH, "//span[contains(text(), 'Next')]")))
        print("Next button found")
        self.driver.find_element(self.by.XPATH, "//span[contains(text(), 'Next')]").click()
        print("Next button clicked")
        
        # Wait for the page to laod and locate the password input fields
        #self.by.XPATH, "//input[@name='password']")))
        self.webDriverWait(self.driver, 10).until(self.ec.visibility_of_element_located((self.by.NAME, 'password')))
        print("password field visible ")
        self.driver.find_element(self.by.NAME, 'password').send_keys(self.password)
        print("password inputted")
        
        # Locate login button 
        self.webDriverWait(self.driver, 20).until(self.ec.visibility_of_element_located((self.by.XPATH, "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1fkl15p r-1loqt21 r-o7ynqc r-6416eg r-jc7xae r-1ny4l3l']"))).click()
        
    # --- Search for a user or hashtag and fetch ---   
    def search_subject(self):
        # wait and find search box 
        self.webDriverWait(self.driver,20).until(self.ec.presence_of_element_located((self.by.XPATH,"//input[@data-testid='SearchBox_Search_Input']")))
        
        # if we search a hastag type, search it in the search box 
        if(self.isHashtag == True): 
            # search hashtag
            self.driver.find_element(self.by.CSS_SELECTOR, 'input[name="text"]').send_keys(self.subject)
            # press the enter key 
            self.driver.find_element(self.by.CSS_SELECTOR, 'input[name="text"]').send_keys(Keys.RETURN)
            return 
        # else if it a user, go directly to the subjects profile
        else:
            self.driver.get('https://x.com/' + self.subject)
        
        #look up the hastag  
    
    # def collect_hashtag_tweets(self):
    #     print("inside collect_hashtag_tweets()")
        
    
    # --- Collect tweets from users profile ---
    def collect_tweets(self):
        
        # find elements of the tweet
        # (//article[@role='article'])[3]
        #(//article[@role='article'])[1]
        articles = self.driver.find_elements(self.by.XPATH, "//article[@data-testid = 'tweet']")
        
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
                tweets.append(tweet_text)

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
            articles = self.driver.find_element(self.by.XPATH, "//article[@data-testid = 'tweet']")
            tweets_update = list(set(tweets))
            # break at August 2 
            if len(tweets_update) > 5 :
                return user_tags, time_stamps
    
    
    
    
    # TO DO: function that distinguies tweet, repost, reply tweet,         
    # def label_text_type(self):
            
    # --- Generates a csv file ---      
    def export_to_csv(self):
        # create dataframe
        tweets_dataframe = pd.DataFrame({
            'user_name': self.user_tags,
            'timestamp': self.time_stamps,
            'tweet_text': self.tweets,
            'replies_count': self.replies,
            'retweet_count': self.retweets,
            'like_count': self.likes
        })
        
        # export as csv
        # os.makedirs('Users/vanessa/Documents/dev_projects/github_projects/Presidential_Sentiment_Analysis/', exist_ok=True) 
        
        tweets_dataframe.to_csv('Users/vanessa/Documents/dev_projects/sentiment_data_folder/tweets_data.csv', index=False)  

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
tweets_scraper( username="", password="", subject="realDonaldTrump", isHashtag = False)


# Notes: 
# XPATH for tweets that were replied to : //div[@data-testid='tweetText' and ancestor::div[@role='link']]
# XPATH 