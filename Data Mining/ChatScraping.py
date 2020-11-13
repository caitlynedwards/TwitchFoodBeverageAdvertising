#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 10:55:38 2020

@author: caitlynedwards
"""

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
import ipdb

# selenium specific imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from MisspellingsList import words


#%% Initial Configuration 

# configuration parser initialization
config = configparser.ConfigParser()
config.read('./config.ini')
delay = 30 # waits for 10 seconds for the correct element to appeaar

#%% Read in File

stream_data = pd.DataFrame(columns=['Message', 'Time', 'Channel', 'Game', 'Language', 'Viewers'])

#%% Login

def login_streamhatchet():
    driver.get("https://app.streamhatchet.com/")
    time.sleep(3) # sleep for 3 seconds to let the page load
    driver.find_element_by_id("hs-eu-confirmation-button").click()

    username = driver.find_element_by_name("loginEmail")
    username.clear()
    username.send_keys(config['login_credentials']['email'])

    password = driver.find_element_by_name("loginPassword")
    password.clear()
    password.send_keys(config['login_credentials']['password'])

    driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    time.sleep(3) # sleep for 3 seconds to let the page load

#%% 
def run_search(query, incomplete_queries_list):
    df = []
    driver.find_element_by_xpath("//button[@class='applyBtn btn btn-sm btn-success ui google plus button']").click()
    run_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='medium ui google plus submit button']")))
    run_button.click()
    time.sleep(5)

    # Scrape the Number of Titles
    driver.find_element_by_tag_name('body').send_keys(Keys.HOME)

    num_titles = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-count']")))
    num_titles = num_titles.text

    unique_channels = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='unique-channels']")))
    unique_channels = unique_channels.text

    unique_users = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='unique-users']")))
    unique_users = unique_users.text

    # #Scrolling to bottom of page to pull table data
    # last_height = driver.execute_script("return document.body.scrollHeight")

    # while True:
    #     #Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     #Wait to load page
    #     time.sleep(1)

    #     #Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

        # Pulls table data
   # if minute == 0:
            #df = driver.find_element_by_xpath("//table/tbody").text.split("\n")
    # df = driver.find_element_by_xpath("//div[@id='table_discovery']/tbody").text.split("\n")
            
    
    table_rows = driver.find_elements_by_xpath("//table[@id='table_discovery']/tbody/tr")
    #df = [i.text for i in table_rows]
    for i in table_rows:
        df.append(i.text.split("\n"))
        
        
    print("Analyzed")
           
    # else:
    #         #df = df.append(driver.find_element_by_xpath("//table/tbody").text.split("\n"))
    #         df = df.append(driver.find_element_by_xpath("//div[@id='table_discovery']/tbody").text.split("\n"))
            
    #         print("Analyzed")

    # driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
    # time.sleep(5)
    # driver.find_element_by_xpath("//div[@id='NewRangePicker']").click()
    # driver.set_page_load_timeout(60)

    return(num_titles, unique_channels, unique_users, df)


#%% Stream Title Search
def stream_title_search(query, incomplete_queries_list):
    df = []
    driver.get("https://app.streamhatchet.com/chatsearch")
    time.sleep(2)
    
    # Enters query into 'Stream title query'
    stream_title_query_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='chat-query']")))
    stream_title_query_input.send_keys(query)
    
    # Click to Check Statistics Box
    driver.find_element_by_xpath("//div[@class = 'checkbox']").click()

    # Click to Expand Date Options
    driver.find_element_by_xpath("//div[@id='NewRangePicker']").click()
    
    #ipdb.set_trace()
    # Select last 30 days
    driver.find_element_by_css_selector("div#new-picker > div.ranges > ul > li:nth-child(3)").click()
    
    # # Loop over time and pull data
    # hour = 0
    # minute = 0
    # #for day in range(22,32):
    # for day in range (22,23):
    #     driver.find_element_by_xpath("//div[@class='calendar left']//td[contains(text(), '{0}')]".format(day)).click()
    #     driver.find_element_by_xpath("//div[@class='calendar left']//td[contains(text(), '{0}')]".format(day)).click()
    #     while hour != 24:
    #         while minute != 59:
    #             driver.find_element_by_xpath("//div[@class='calendar left']//select[@class='hourselect']//option['{0}']".format(hour)).click()
    #             driver.find_element_by_xpath("//div[@class='calendar right']//select[@class='hourselect']//option['{0}']".format(hour)).click()
                                
    #             if len(str(minute)) != 2 and minute != 9: #Need to pad 00s if 0 through 9, but 10 does not need zero padding
    #                 driver.find_element_by_xpath("//div[@class='calendar left']//option[contains(text(),'{0}')]".format(str("0" + str(minute)))).click()
    #                 driver.find_element_by_xpath("//div[@class='calendar right']//option[contains(text(),'{0}')]".format(str("0" + str(minute + 1)))).click()
    #                 num_titles, unique_channels, unique_users, df = run_search(minute, df)

                
    #             elif len(str(minute)) != 2 and minute == 9: #Need to accommodate for 09 and 10
    #                 driver.find_element_by_xpath("//div[@class='calendar left']//option[contains(text(),'{0}')]".format(str("0" + str(minute)))).click()
    #                 driver.find_element_by_xpath("//div[@class='calendar right']//option[contains(text(),'{0}')]".format(str(minute + 1))).click()   
    #                 num_titles, unique_channels, unique_users, df = run_search(minute, df)

                
    #             else: #Both are double digits
    #                 driver.find_element_by_xpath("//div[@class='calendar left']//option[contains(text(),'{0}')]".format(minute)).click()
    #                 driver.find_element_by_xpath("//div[@class='calendar right']//option[contains(text(),'{0}')]".format(minute)).click()
    #                 num_titles, unique_channels, unique_users, df = run_search(minute, df)
               
    #             minute = minute + 1
           
    #         driver.find_element_by_xpath("//div[@class='calendar left']//option[contains(text(),'{0}')]".format(minute)).click()
            
    #         driver.find_element_by_xpath("//div[@class='calendar right']//select[@class='hourselect']//option[{0}]".format(hour+1)).click()
    #         driver.find_element_by_xpath("//div[@class='calendar right']//option[contains(text(),'{0}')]".format(minute)).click()
    #         run_search(minute)

            
    #         hour = hour + 1
    #         minute = 0
        
    #     hour = 0
    #     minute = 0
    return(num_titles,  unique_channels, unique_users, df)


#%% Test Case
#df = []

# driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver")) #Open chrome driver so that it opens in another page
# login_streamhatchet()
# num_titles, unique_channels, unique_users, table_id = stream_title_search("test", df) #Run above script





#%% Run Stream Title Search

incomplete_queries_list = []
driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver")) #Open chrome driver so that it opens in another page

login_streamhatchet() #Log into streamhatchet

for word in words: #For each word
    print("Starting " + word) #Print so you know which line you're on
    num_titles, table_id = stream_title_search(word, incomplete_queries_list) #Run above script
    if len(table_id) == 1: #If no data
            stream_data = stream_data.append({'Word': word,
                                              'Title': "None", #Adds unique users, streamers, and total views to data set
                                              'Streamer': "None", 
                                              'Date': "None",
                                              'Hours Watched': 0}, ignore_index = True)
    else: #If at least one stream title
        for i in range(len(table_id)): #For table of results
            stream_data = stream_data.append({'Word': word,
                                          'Title': table_id[i], #Adds unique users, streamers, and total views to data set
                                          'Streamer': table_id[i+1], 
                                          'Date': table_id[i+2],
                                          'Hours Watched': table_id[i+3]}, ignore_index = True)

#%% If Stream Title Search Breaks
# driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver.exe"))

# login_streamhatchet()

# for word in words[300:]:
#     print("Starting " + word)
#     num_titles, table_id = stream_title_search(word, incomplete_queries_list)
#     for i in range(len(table_id))[0::6]:
#         if len(table_id) == 1:
#             stream_data = stream_data.append({'Word': word,
#                                               'Title': "None", #Adds unique users, streamers, and total views to data set
#                                               'Streamer': "None", 
#                                               'Date': "None",
#                                               'Hours Watched': 0}, ignore_index = True)
#         else:
#             stream_data = stream_data.append({'Word': word,
#                                           'Title': table_id[i], #Adds unique users, streamers, and total views to data set
#                                           'Streamer': table_id[i+1], 
#                                           'Date': table_id[i+2],
#                                           'Hours Watched': table_id[i+3]}, ignore_index = True)

#%% Export Data File
stream_data.to_csv('/Users/caitlynedwards/Desktop/python/StreamTitles2.csv', index = None, header=True)
