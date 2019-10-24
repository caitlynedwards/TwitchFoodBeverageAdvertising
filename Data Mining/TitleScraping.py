#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 08:03:51 2019
Last Updated: July 22nd

@author: cpollack

"""

#%% Importing Libraries

# other imports
import configparser
import time
import pandas as pd
import os

# selenium specific imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from MisspellingsList import words


#%% Initial Configuration 

# configuration parser initialization
config = configparser.ConfigParser()
config.read('../config.ini')
delay = 10 # waits for 10 seconds for the correct element to appeaar

#%% Read in File

stream_data = pd.DataFrame(columns=['Title', 'Streamer', 'Date', 'Hours Watched', 'Word'])

#%% Login

def login_streamhatchet():
    driver.get("https://app.streamhatchet.com/")
    driver.find_element_by_id("cookiesAccepted").click()

    username = driver.find_element_by_name("loginEmail")
    username.clear()
    username.send_keys(config['login_credentials']['email'])

    password = driver.find_element_by_name("loginPassword")
    password.clear()
    password.send_keys(config['login_credentials']['password'])

    driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    time.sleep(3) # sleep for 3 seconds to let the page load


#%% Stream Title Search
def stream_title_search(query, incomplete_queries_list, df):
    driver.get("https://app.streamhatchet.com/search/toolstatus")
    time.sleep(1)
    
    # Enters query into 'Stream title query'
    stream_title_query_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='status-query']")))
    stream_title_query_input.send_keys(query)

    # Makes twitch the only platform to search
    platform_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='search']")))
    platform_input.click()
    platform_input.send_keys(Keys.BACKSPACE)
    platform_input.send_keys(Keys.BACKSPACE)
    platform_input.send_keys(Keys.BACKSPACE)

    # Click to Expand Date Options
    driver.find_element_by_xpath("//div[@id='NewRangePicker']").click()
    
    # change the hours and minutes to 0:00 for date from and to 
    driver.find_element_by_xpath("//div[@class='calendar left']//select[@class='hourselect']//option[1]").click()
    driver.find_element_by_xpath("//div[@class='calendar left']//option[contains(text(),'00')]").click()
    driver.find_element_by_xpath("//div[@class='calendar right']//select[@class='hourselect']//option[1]").click()
    driver.find_element_by_xpath("//div[@class='calendar right']//option[contains(text(),'00')]").click()
    
    # Keep clicking on left_arrow
    while driver.find_element_by_xpath("//i[@id='icon-down-New']").is_displayed() == True:
        try:
            driver.find_element_by_xpath("//i[@class='fa fa-chevron-left glyphicon glyphicon-chevron-left']").click()
        except:
            break
                
     # Click on first day of the month:  
    day_one_element = driver.find_element_by_xpath("//div[@class='calendar left']//tr[1]//td[2]")
    try:
        day_one_element.click()
    except WebDriverException:
        print("First Day element is not clickable")   
    
    while driver.find_element_by_xpath("//i[@id='icon-down-New']").is_displayed() == True:
        try:
            driver.find_element_by_xpath("//i[@class='fa fa-chevron-right glyphicon glyphicon-chevron-right']").click()
        except:
           break
    
    driver.find_element_by_xpath("//div[@class='calendar right']//td[contains(text(), '27')]").click()

    # Runs the search
    driver.find_element_by_xpath("//button[@class='applyBtn btn btn-sm btn-success ui google plus button']").click()
    run_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='medium ui google plus submit button']")))
    run_button.click()
    
    # Scrape the Number of Titles
    num_titles = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-count']")))
    num_titles = num_titles.text
    
    #Scrolling to bottom of page to pull table data
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        #Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        #Wait to load page
        time.sleep(1)
        
        #Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Pulls table data
    df = driver.find_element_by_xpath("//table/tbody").text.split("\n")

    return(num_titles, df)

#%% Run Stream Title Search

df = []
incomplete_queries_list = []
driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver.exe")) #Open chrome driver so that it opens in another page

login_streamhatchet() #Log into streamhatchet

for word in words: #For each word
    print("Starting " + word) #Print so you know which line you're on
    num_titles, table_id = stream_title_search(word, incomplete_queries_list, df) #Run above script
    for i in range(len(table_id))[0::6]: #For table of results
        if len(table_id) == 1: #If no data
            stream_data = stream_data.append({'Word': word,
                                              'Title': "None", #Adds unique users, streamers, and total views to data set
                                              'Streamer': "None", 
                                              'Date': "None",
                                              'Hours Watched': 0}, ignore_index = True)
        else: #If at least one stream title
            stream_data = stream_data.append({'Word': word,
                                          'Title': table_id[i], #Adds unique users, streamers, and total views to data set
                                          'Streamer': table_id[i+1], 
                                          'Date': table_id[i+2],
                                          'Hours Watched': table_id[i+3]}, ignore_index = True)

#%% If Stream Title Search Breaks
driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver.exe"))

login_streamhatchet()

for word in words[300:]:
    print("Starting " + word)
    num_titles, table_id = stream_title_search(word, incomplete_queries_list, df)
    for i in range(len(table_id))[0::6]:
        if len(table_id) == 1:
            stream_data = stream_data.append({'Word': word,
                                              'Title': "None", #Adds unique users, streamers, and total views to data set
                                              'Streamer': "None", 
                                              'Date': "None",
                                              'Hours Watched': 0}, ignore_index = True)
        else:
            stream_data = stream_data.append({'Word': word,
                                          'Title': table_id[i], #Adds unique users, streamers, and total views to data set
                                          'Streamer': table_id[i+1], 
                                          'Date': table_id[i+2],
                                          'Hours Watched': table_id[i+3]}, ignore_index = True)

#%% Export Data File
stream_data.to_csv('/Users/cpollack/Documents/Dartmouth/Research/Twitch/Data/Jan18July27_StreamTitles.csv', index = None, header=True)
