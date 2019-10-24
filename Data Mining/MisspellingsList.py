#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last Updated: 07.22.19
Creates list of misspellings to be searched. 
"""


# This assumes everything is in lowercase. We should make sure this is the case
# before running through this.
# %% Import Libraries and Packages
import pandas as pd
import difflib
import matplotlib.pyplot as plt

from difflib import SequenceMatcher
from pyjarowinkler import distance

# %% Read in data files
words = pd.read_csv("BrandListandStats - Modified Search Term.csv", header = None) #Import brand list compiled by Travis
words = words.dropna() #Drop any NAs

words = words.values.tolist()
words = list(map(''.join, words))

# %% Some common misspellings based on the one that I found 
misspellings = []
k = ["k", "c", "cc", "ch", "ck"]
g = ["g", "gg", "gh"]
j = ["j", "g", "dg", "de", "di", "dj"]
n = ["n", "nn", "gn", "kn", "pn"]
f = ["f", "ff", "gh", "ough", "ph"]
a = ["a", "ai", "e", "ea", "eo", "ie", "ue", "ee"]
ew = ["ew", "o", "oe", "oo", "ou", "u", "ui", "wo"]
c = ["c", "s"]
ch = ["ch", "sh"]
z = ["z", "s"]
t = ["t", "d"]
vowels = ["a", "e", "i", "o", "u", "y"]
letters = [k, g, j, n, f, a, ew, c, ch, z, t]

#vowels are the most common spelling errors I see (so spelling Reese’s with 
#some variation of “ric-“ or something like that) and also watch out for 
#ch-/sh-, x, qu, z/s (this one is more common than you’d think because words 
#like pigs are pronounced with a z), t/d 


# %% Create list of misspellings
for word in words: #For each word in the list
    if "-" in word:
        words.append(word.replace("-", " "))
    if "'" in word:
        words.append(word.replace("'", "’")) # Makes sure to redo everything without apostraphe
        words.append(word.replace("'", "")) # Makes sure to redo everything without apostraphe
    if "’" in word:
        words.append(word.replace("’", "'"))
        words.append(word.replace("’", "")) # Makes sure to redo everything without apostraphe
    if " " in word: #If there are multiple words
        words.append(word.replace(" ", "")) #Make sure to make it only one word 
    if "&" in word:
        words.append(word.replace("&", "and"))
    if "z" in word:
        words.append(word.replace("z", "s"))
    for lists in letters: #For each list in the letters masterlist
        for letter in lists: #For each letter in the list
            if letter in word: #If the letter is in the word
                for replace in lists: #For each letter in the list
                    misspellings.append(word.replace(letter, replace)) #Switch it out for all possible combinations
    for vowel in vowels: #For each vowel
        if vowel in word: #If the vowel is in the word
            misspellings.append(word.replace(vowel, "")) #Replace all vowels
            for index in range(0, len(word)): #For each letter in the word
                if word[index] in vowel: #If the letter at a particular index is a vowel
                    misspellings.append(word[:index] + "" + word[index + 1:]) #Remove it. 

misspellings = pd.DataFrame(misspellings) #Drop duplicated words

# %% Export basic word file
words_dataframe = pd.DataFrame(words)
words_dataframe =words_dataframe.drop_duplicates()

# %% Calculate various word distances 
misspellings_list = misspellings.values.tolist()
misspellings_list = list(map(''.join, misspellings_list))
misspellings["Closest Word, 1-DL"] = ""
misspellings["Closest Distance, 1-DL"] = ""
misspellings["Closest Word, JW"] = ""
misspellings["Closest Distance, JW"] = ""

similar_words = []
counter = 0

# Return a measure of the sequences' similarity as a float in the range [0, 1]. 
#Where T is the total number of elements in both sequences, and  M is the number of 
#matches, this is 2.0*M / T.

for spelling in misspellings_list:
    sequence = difflib.get_close_matches(spelling, words)
    seq_old = 0
    seq_old_jw = 0
    if len(sequence) > 0:
        for seq in sequence:
            if SequenceMatcher(None, spelling, seq).ratio() > seq_old: #If the closeness is higher based on D-L
                misspellings.iat[counter, 1] = seq # Closest Word
                misspellings.iat[counter, 2] = SequenceMatcher(None, spelling, seq).ratio() #Closest Distance 1 - Damerau Levenshtein 
                seq_old = SequenceMatcher(None, spelling, seq).ratio()
            if distance.get_jaro_distance(seq, spelling, winkler = True) > seq_old_jw:
                misspellings.iat[counter, 3] = seq
                misspellings.iat[counter, 4] = distance.get_jaro_distance(seq, spelling, winkler = True)
                seq_old_jw = distance.get_jaro_distance(seq, spelling, winkler = True)
    counter = counter + 1
                
misspellings['Closest Distance, 1-DL'] = pd.to_numeric(misspellings['Closest Distance, 1-DL'],errors='coerce')
misspellings['Closest Distance, JW'] = pd.to_numeric(misspellings['Closest Distance, JW'], errors = 'coerce')
plt.hist(misspellings.iloc[:,2])   
plt.hist(misspellings.iloc[:,4])          

misspellings = misspellings.dropna()
misspellings = misspellings.drop_duplicates()

