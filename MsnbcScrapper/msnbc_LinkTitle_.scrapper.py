import selenium
from selenium import webdriver
import os
import time
import datetime
import csv
from random import randint
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class msnbcBot:
    def __init__(self, topic):
        self.topic = topic

        # Lists to store scraped data
        self.articleLink = []
        self.title = []
        self.authors = []
        self.originaldates = []
        self.editedDates = []
        self.articleContent = []

        # Set up Chrome driver
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")  # Run in headless mode (no pop up browser)
        option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.driver = webdriver.Chrome(option)

        # For Selenium interaction
        self.by = By
        self.ec = EC

        # Random sleep to simulate human behavior
        sleep(randint(5, 10))

        # Navigate to MSNBC page and collect article links
        self.navigateMsnbc()

        sleep(randint(5, 10))

        # Save the links and titles to CSV
        self.articleLinkToCsv()

    def navigateMsnbc(self):
        # Access MSNBC archive for the specified month
        self.driver.get('https://www.msnbc.com/archive/articles/2024/august')

        # Find and extract all links from the main content section
        main_element = self.driver.find_element(self.by.XPATH, "//main[@class='MonthPage']")
        links = main_element.find_elements(self.by.XPATH, 'a')

        # Loop through each link and collect URL and text (article title)
        for link in links:
            self.articleLink.append(link.get_attribute('href'))
            self.title.append(link.text)

    def articleLinkToCsv(self):
        # Save article titles and links to a CSV file
        filename = f"results_august_articles.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Title', 'Link'])
            # Write rows
            for i in range(len(self.articleLink)):
                writer.writerow([self.title[i], self.articleLink[i]])

        print(f"Data saved to {filename}")

# Test run with topic 'July'
test = msnbcBot('July')
