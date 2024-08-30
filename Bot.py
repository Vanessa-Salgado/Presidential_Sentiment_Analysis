from selenium import webdriver
import os
import time
import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class InstagramBot:
    def __init__(self, username, password, amount, hashtag):
        self.username = username
        self.password = password
        self.amount = amount
        self.hastag = hashtag

        #self.driver = webdriver.Chrome('/Users/alanferia/Desktop/Presidential_Sentiment_Analysis/InstagramScrapper/chromedriver') #be sure to download chrome driver for mac prior to running this
        ##added

        options = webdriver.ChromeOptions()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        chrome_driver_binary = "/Users/alanferia/Desktop/Presidential_Sentiment_Analysis/InstagramScrapper/chromedriver" #change to your directory will update later so it doesnt need to be hard coded
        self.driver = webdriver.Chrome(chrome_driver_binary, options=options)

        ##Added
        time.sleep(1)
        self.login()

        self.by = By
        self.ec = EC 

        self.webDriverWait = WebDriverWait

        self.explore_hastags()


    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        
        self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.Name, 'username')))
        self.webDriverWait(self.driver, 20).until(self.ec.presence_of_element_located((self.by.Name, 'password')))
        self.webDriverWait(self.driver, 20).until(self.ec.element_to_be_clickable((self.by.XPATH, '//*[contains(text(),"Log In")]')))

        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[contains(text(),"Log In")]').click()

    #def explore_hastags(self):
        #self.driver.get('https://www.instagram.com/explore/tags/' + self.hastag) #navigating to hastag topic

    #def scrape_post(self): 
        #self.driver.find_element_by_class_name("v1Nh3").click()
        #i = 1
        #while i <= self.element:
            #time.sleep()
            #self.driver.find_element_by_class_name("v1Nh3").click()
            #self.driver.find_element_by_class_name("coreSpriteRightPaginationArrow").click()
            #i += 1

        #self.driver.get('https://www.instagram.com')


ig = InstagramBot("crf.alan_", "xewxyg-0cipho-qosbYc!", 2, "cats") #to be changed, dont want to put personal info on internet



    

