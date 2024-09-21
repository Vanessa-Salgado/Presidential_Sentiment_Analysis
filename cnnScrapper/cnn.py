import selenium
from selenium import webdriver
import os
import time
import datetime
import csv

#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CnnBot:
    def __init__(self, topic, numpages, date, month):

        self.topic = topic
        self.numpages = numpages
        self.date = date
        self.month = month

        self.articleLink = []
        self.title = []
        self.authors = []
        self.originaldates = []
        self.editedDates = []
        self.articleContent = []

        option = webdriver.ChromeOptions()
        option.add_argument("--headless")  # Run in headless mode (no pop up browser)
        option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(option)

        self.by = By
        self.ec = EC

        time.sleep(5)
        self.navigateCnn()

        time.sleep(5)
        self.articleParse()

        time.sleep(5)
        self.save_to_csv()

    def navigateCnn(self):

        self.driver.get('https://www.cnn.com')
        
        first_search_button = self.driver.find_element(self.by.XPATH, '//*[@id="headerSearchIcon"]')
        first_search_button.click()
        
        search_input = self.driver.find_element(self.by.XPATH, "//form/input[@class='search-bar__input']")
        search_input.send_keys(self.topic)

        search_btn = self.driver.find_element(self.by.XPATH, "//button[@class='search-bar__submit']")
        search_btn.click()

        time.sleep(5)
        
        stories_btn = self.driver.find_element(self.by.XPATH, '//li[2]/label[@for="collection_article"]')
        stories_btn.click()

        time.sleep(5)
       
        i = 0
        while i < self.numpages:
            i += 1
            temp_list = [element.get_attribute('href') for element in self.driver.find_elements(self.by.XPATH, "//div[@class='card container__item container__item--type-media-image container__item--type- container_list-images-with-description__item container_list-images-with-description__item--type-  ']//a[1]")]
            
            for item in temp_list:

                self.articleLink.append(item)
                #print(item)
                #
                # 
                # 
                # 
                # 
                # print(i)

            next_btn = self.driver.find_element(By.XPATH, "//div[contains(@class, 'pagination-arrow')][2]")  # Pagination next button
            next_btn.click()
            time.sleep(5)

        #print("done Finding links")

    def articleParse(self):
        for link in self.articleLink:
                self.driver.get(link)
                
                time.sleep(5) 
                try:
                    temp_author = self.driver.find_element(self.by.XPATH, "//meta[@name='author']").get_attribute("content")
                except selenium.common.exceptions.NoSuchElementException:
                    temp_author = "No Results Found"
                try:
                    temp_title = self.driver.find_element(self.by.XPATH, "//meta[@property='og:title']").get_attribute("content")
                except:
                    temp_title = "No Results Found"
                #orig_date = self.driver.find_element(self.by.XPATH, "//meta[19][@property='article:published_time']").get_attribute("content")  

                try:
                    orig_date = self.driver.find_element(self.by.XPATH, "//meta[19][@property='article:published_time']").get_attribute("content") 
                except selenium.common.exceptions.NoSuchElementException:
                    orig_date = "No Results Found"

                try:
                    edited_date = self.driver.find_element(self.by.XPATH, '//div[2][@class="timestamp vossi-timestamp-primary-core-light"]').text
                except selenium.common.exceptions.NoSuchElementException:
                    edited_date = "No Results Found"

                try:
                    text_as_list = self.driver.find_elements(self.by.XPATH, ".//p[@class='paragraph inline-placeholder vossi-paragraph-primary-core-light']")
                except:
                    text_as_list = "No Results Found"
                text_as_paragraph = ' '.join([element.text for element in text_as_list])

                self.title.append(temp_title)
                self.authors.append(temp_author)
                self.originaldates.append(orig_date)
                self.editedDates.append(edited_date)
                self.articleContent.append(text_as_paragraph)

    def save_to_csv(self):
        filename = f"results_{self.month}_{self.date}_{self.topic}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Title','Edit_Date', 'Origal_Date', 'Link', 'Content'])
            # Write rows
            for i in range(len(self.articleLink)):
                writer.writerow([self.title[i], self.editedDates[i], self.originaldates[i], self.articleLink[i], self.articleContent[i]])

        print(f"Data saved to {filename}")

    
       
test = CnnBot('trump', 4, 18, 'sept')
test = CnnBot('harris', 2, 18, 'sept')
test = CnnBot('election', 4, 18, 'sept')