import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import os
import atexit
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from threading import Timer
import csv
import time
from selenium import webdriver
from sentimentizer import sentimentize
from twilio.rest import Client
import smtplib
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import os
from sentimentizer import sentimentize
import matplotlib.pyplot as plt
import numpy as np

chrome_options = Options()
chrome_options.headless = False

# THIS VERSION USES A SINGLE DRIVER - CONSIDER MODIFICATIONS TO USE MULTIPLE

# Removes Removing Navigator.Webdriver Flag, and changes resolution, user-Agent, and other details
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("window-size=1280,800")
chrome_options.add_argument("—disable-gpu")
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'),
                          options=chrome_options)
# driver = webdriver.manage().Timeouts().ImplicitWait

# ticker_array = ["AAPL", "TSLA", "HUT"]
ticker_array = ["TSLA"]
# Initialization - getting first n headlines
driver.get("https://finviz.com/")
first_n = 10
timeout = 5
pos_count = 0
neg_count = 0

for i in range(len(ticker_array)):
    element = driver.find_element_by_xpath("//*[@id='search']/div/form/input")
    element.send_keys(ticker_array[i])
    element.send_keys(Keys.RETURN)
    time.sleep(1)

    # Wait for page to load, before proceeding
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'tab-link-news'))
    WebDriverWait(driver, timeout).until(element_present)

    headlines = driver.find_elements_by_class_name("tab-link-news")


    # Gets n most recent headlines
    with open(ticker_array[i] + '.csv', 'w', ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Headline'])
        for j in range(first_n):
            writer.writerow([str(headlines[j].text)])
            print(str(headlines[j].text))
            sentiment_result = sentimentize(str(headlines[j].text))
            if(sentiment_result['label'] == "POSITIVE"):
                pos_count += 1
            elif(sentiment_result['label'] == "NEGATIVE"):
                neg_count += 1

sentiment_count = np.array([pos_count, neg_count])
labels = ["Positive", "Negative"]

plt.pie(sentiment_count, labels=labels)
plt.title("TSLA Stock Sentiment Right Now")
plt.show()
# Refresh page and get most recent headline
# prev_headline = [''] * len(ticker_array)
# wait_time = .5
# while True:
#     for i in range(len(ticker_array)):
#         element = driver.find_element_by_xpath("//*[@id='search']/div/form/input")
#         element.send_keys(ticker_array[i])
#         element.send_keys(Keys.RETURN)

#         # Wait for page to load before proceeding
#         element_present = EC.presence_of_element_located((By.CLASS_NAME, 'tab-link-news'))
#         WebDriverWait(driver, timeout).until(element_present)

#         curr_headline = driver.find_element_by_class_name("tab-link-news")
#         if curr_headline.text != prev_headline[i]:
#             print(str(curr_headline.text))
#             # Goes through the transformer and prints out sentiment plus confidence
#             sentiment_result = sentimentize(str(curr_headline.text))
#             print("Label:", sentiment_result['label'])
#             print("Confidence Score:", sentiment_result['score'])
#             print()
#             prev_headline[i] = curr_headline.text

# driver.close()
# driver.quit()
