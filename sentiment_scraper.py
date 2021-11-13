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
from twilio.rest import Client
import smtplib
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.headless = False

# THIS VERSION USES A SINGLE DRIVER - CONSIDER MODIFICATIONS TO USE MULTIPLE

# Removes Removing Navigator.Webdriver Flag, and changes resolution, user-Agent, and other details
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("window-size=1280,800")
chrome_options.add_argument("—disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
driver = webdriver.Chrome(executable_path="C:/Users/david/PycharmProjects/WebsiteBot/chromedriver.exe",
                          options=chrome_options)
# driver = webdriver.manage().Timeouts().ImplicitWait

ticker_array = ["AAPL", "TSLA", "HUT"]

# Initialization - getting first n headlines
driver.get("https://finviz.com/")
first_n = 10
timeout = 5
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

# Refresh page and get most recent headline
prev_headline = [''] * len(ticker_array)
wait_time = .5
while True:
    for i in range(len(ticker_array)):
        element = driver.find_element_by_xpath("//*[@id='search']/div/form/input")
        element.send_keys(ticker_array[i])
        element.send_keys(Keys.RETURN)

        # Wait for page to load before proceeding
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'tab-link-news'))
        WebDriverWait(driver, timeout).until(element_present)

        curr_headline = driver.find_element_by_class_name("tab-link-news")
        if curr_headline.text != prev_headline[i]:
            print(str(curr_headline.text))
            prev_headline[i] = curr_headline.text

driver.close()
driver.quit()
