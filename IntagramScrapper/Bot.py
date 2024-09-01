from selenium import webdriver
import os
import time
import datetime
import csv

#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramBot:
    def __init__(self, username, password, amount, userAccount):
        self.username = username
        self.password = password
        self.amount = amount
        self.userAccount = userAccount

        ##added

        option = webdriver.ChromeOptions()
        option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(option)

        self.by = By
        self.ec = EC
        self.webDriverWait = WebDriverWait

        time.sleep(1)
        self.login()

        time.sleep(5)
        self.explore_user()
        
        time.sleep(5)
        self.post_collector()

        time.sleep(5)
        self.link_url=[]
        self.Authorcomments = []
        self.collect_comment_by_author()

        time.sleep(5)
        self.viewer_comments = []
        self.collect_viewer_comments()

        time.sleep(5)

        self.comment_dates = []
        self.comment_date_collector()

        time.sleep(5)
        self.save_data_to_csv()






    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        
        # Wait for the page to load and locate the username and password input fields
        self.webDriverWait(self.driver, 10).until(self.ec.presence_of_element_located((self.by.NAME, 'username')))
        self.webDriverWait(self.driver, 10).until(self.ec.presence_of_element_located((self.by.NAME, 'password')))
        
        # Send keys to the input fields
        self.driver.find_element(self.by.NAME, 'username').send_keys(self.username)
        self.driver.find_element(self.by.NAME, 'password').send_keys(self.password)
        
        # Wait for the Log In button to be clickable and click it
        self.webDriverWait(self.driver, 10).until(self.ec.element_to_be_clickable((self.by.XPATH, '//button[@type="submit"]')))
        self.driver.find_element(self.by.XPATH, '//button[@type="submit"]').click()

        #time.sleep(30)
    def explore_user(self):
        self.driver.get('https://www.instagram.com/'+ self.userAccount)

    def post_collector(self):
        self.driver.find_element(self.by.CLASS_NAME, '_aagu').click()
        time.sleep(10)

    #comments = []
    def collect_comment_by_author(self):
        #comments = []
    # Ensure the page is scrolled to the bottom to load all comments
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Give time for comments to load

        try:
            specific_comment_element = self.driver.find_element(self.by.XPATH, '//div[2]/div[1]/h1[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]')
            comment_text = specific_comment_element.text

            if comment_text:  # Check if the comment text is not empty
                self.comments.append(comment_text)
                print(f"Author comment: {comment_text}")
        except Exception as e:
            print(f"Error collecting specific comment: {e}")

        link_element = self.driver.current_url  # This fetches the first link found on the page

# Get the URL from the href attribute
        self.link_url.append(link_element)

        print(self.link_url)  
        #print(self.comments)


    def collect_viewer_comments(self):
        #viewer_comments = []

        # Ensure the page is scrolled to the bottom to load all comments
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Give time for comments to load

        try:
            # Locate all comment elements by tag and class names
            comment_elements = self.driver.find_elements(self.by.XPATH, '//div[2]/div[1]/span[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"]')

            # Collect the first 5 comments
            for i, comment_element in enumerate(comment_elements[:15]):
                comment_text = comment_element.text
                if comment_text:  # Check if the comment text is not empty
                    self.viewer_comments.append(comment_text)
                    #print(f"Collected viewer comment {i + 1}: {comment_text}")

        
        except Exception as e:
            print(f"Error collecting comments: {e}")
        #print(self.viewer_comments)

    def comment_date_collector(self):
        #self.comment_dates = []

        # Ensure the page is scrolled to the bottom to load all comments
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Give time for comments to load

        try:
            # Locate all comment elements by tag and class names
            
            comment_dates_elements = self.driver.find_elements(self.by.XPATH, '//time[@class="_a9ze _a9zf"]')
            
        #print(comment_date)

            # Collect the first 5 comments
            for i, comment_date in enumerate(comment_dates_elements[1:16]):
                comment_date = comment_date.get_attribute('datetime')
                if comment_date:  # Check if the comment text is not empty
                    self.comment_dates.append(comment_date)
                    #print(f"Collected comment date {i+1}: {comment_date}")
                    

        
        except Exception as e:
            print(f"Error collecting comments: {e}")

        #print(self.comment_dates)


        # For tommorow, align date and comment - task done within each of the functions, i started one function frmo 0-15 and the other from 1-16

        # date is ahead by one. - done - above

        #example: collected viewer comment 1 --> collected comment date 2 - done above. 

    '''def save_data_to_csv(self):
        # Check if lists are of equal length
        if len(self.viewer_comments) != len(self.comment_dates):
            print("Error: Mismatched data lengths between comments and dates.")
            return

        # Save data to a CSV file
        with open('comments.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Comment_by_viewer", "Date_comment_posted"])
            # Write the data
            for comment, date in zip(self.viewer_comments, self.comment_dates):
                writer.writerow([comment, date])

    def author_save_data_to_csv(self):
        # Check if lists are of equal length
        if len(self.viewer_comments) != len(self.comment_dates):
            print("Error: Mismatched data lengths between comments and dates.")
            return

        # Save data to a CSV file
        with open('comments.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Comment_by_viewer", "Date_comment_posted"])
            # Write the data
            for comment, date in zip(self.viewer_comments, self.comment_dates):
                writer.writerow([comment, date])'''

# Example usage
ig = InstagramBot("crf.alan_", "sufwuw-4xazhU-wehxob", 2, "kamalaharris")
