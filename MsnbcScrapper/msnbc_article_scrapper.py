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
    def __init__(self, topic, start_row):
        self.topic = topic

        self.start_row = start_row

        self.i = 0

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

        sleep(randint(5, 10))

        self.intervalParsed()

        sleep(randint(5, 10))

        self.articleParse()

        sleep(randint(5, 10))

        self.save_to_csv()

    def intervalParsed(self):
        # Open the CSV file
        try:
            with open("results_august_articles.csv", mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Skip the header row
                next(reader)

                # Iterate through the rows, starting at the specified row and extracting the next 25 entries
                for i, row in enumerate(reader):
                    if i < self.start_row:  # Skip rows until we reach the start_row
                        continue
                    if i >= self.start_row + 25:  # Stop after 25 rows starting from start_row
                        break
                    self.title.append(row[0])  # Assuming title is in the first column
                    self.articleLink.append(row[1])  # Assuming article link is in the second column

                    self.i = i
        
        except FileNotFoundError:
            print("CSV file not found. Please check the file path.")

        except Exception as e:
            print(f"An error occurred: {e}")


    def articleParse(self):
        # Parse and extract additional data (author, dates, content) from each article link
        for link in self.articleLink:
            self.driver.get(link)
            sleep(randint(5, 10))

            try:
                orig_date = self.driver.find_element(self.by.XPATH, "//time[@class='relative z-1']").text
            except:
                orig_date = "Not Found"

            #print(orig_date)

            # Extract edited date if available

            edited_date = "Not Avaiable For MSNBC"

            #print(edited_date)

            # Extract article content
            try:
                text_as_list = self.driver.find_elements(self.by.XPATH, "//p[@class='']")
            except:
                text_as_list = "Not Found"

            try:
                text_as_list_ending = self.driver.find_elements(self.by.XPATH, "//p[@class='endmark']")
            except:
                text_as_list_ending = "Not Found"


            #print(text_as_list)

            combined_list = text_as_list + text_as_list_ending

            #print(combined_list)
            
            text_as_paragraph = ' '.join([element.text for element in combined_list])

            # Append the parsed data to the lists
            self.originaldates.append(orig_date)
            self.editedDates.append(edited_date)
            self.articleContent.append(text_as_paragraph)

    def save_to_csv(self):
        # Save the parsed article data to a CSV file
        filename = f"results_{self.topic}_{self.start_row}_to_{min(self.start_row + 25, self.i)}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Title', 'Edit_Date', 'Origal_Date', 'Link', 'Content'])
            # Write rows
            for i in range(len(self.articleLink)):
                writer.writerow([self.title[i], self.editedDates[i], self.originaldates[i], self.articleLink[i], self.articleContent[i]])

        print(f"Data saved to {filename}")

test = msnbcBot('August', 1)
