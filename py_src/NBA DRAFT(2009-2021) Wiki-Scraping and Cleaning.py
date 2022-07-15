# Importing Libraries
import os
import requests
import time
import datetime
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""Maybe make it into a job that extracts and sends a completion email every year."""
# import smtplib 


# Creating a list of draft years.
current_year = datetime.date.today().year
draft_years = [year for year in range(2009, (current_year))]
columns = ['Round', 'Pick', 'Player', 'Position', 'Nationality', 'Team', 'School/club team']
print(columns)

# Function to create new columns:
def create_new_columns(df):
    
    def create_traded_to_a_different_team(x):
        if re.findall("from", x) or re.findall("traded", x) or re.findall("via", x):
            y = "Yes"
        else:
            y = "No"  
        return y

    def create_status(x):
        if re.findall("Fr.", x):
            y = "College Freshman"
        elif re.findall("So.", x):
            y = "College Sophmore"
        elif re.findall("Jr.", x):
            y = "College Junior"
        elif re.findall("Sr.", x):
            y = "College Senior"
        elif re.findall("G League", x):
            y ="NBA G League Player"
        else:
            y = "Playing Internationally" 
        return y

    df['Traded to a different team'] = df[columns[5]].apply(create_traded_to_a_different_team)
    df['Status'] = df[columns[6]].apply(create_status)
    
    return df

# Function to clean the data:
# Function to clean the data.

def clean_data(df):
    
    def clean_player(x):
        x = x.rstrip('*~#+').split('[')[0]
        return x

    def clean_nationality(x):
        x = x.split('[')[0].split('\xa0')[0]
        return x

    def clean_team(x):
        x = x.split('[')[0].split('(')[0].rstrip(' ')
        return x

    def clean_school_club_team(x):
        x = x.split('[')[0]
        if len(re.findall("Fr.", x))!=0 or len(re.findall("So.", x))!=0 or len(re.findall("Jr.", x))!=0 or len(re.findall("Sr.", x))!=0 or len(re.findall("G League", x))!=0:
            x = x.split('(')[0].rstrip(' ')
        return x
    

    df[columns[2]] = df[columns[2]].apply(clean_player)
    df[columns[4]] = df[columns[4]].apply(clean_nationality)
    df[columns[5]] = df[columns[5]].apply(clean_team)
    df[columns[6]] = df[columns[6]].apply(clean_school_club_team)
    
    df.fillna(-1, inplace=True)
    df[columns[0]] = df[columns[0]].astype(int)
    df[columns[1]] = df[columns[1]].astype(int)
    
    return df


# Connect to WIKI Page, load data into pandas dataframe and save as .csv file.
for draft_year in draft_years:
    URL = 'https://en.wikipedia.org/wiki/'+str(draft_year)+'_NBA_draft'

    # headers = {}

    wiki_page = requests.get(URL, timeout=5, verify=True)
    df = pd.read_html(wiki_page.text)
    df = df[3]
    df.columns = columns
    create_new_columns(df)
    clean_data(df)
    df.to_csv('../csv/nba_draft_'+'{}'.format(draft_year)+'.csv', index=False)
    print('NBA Draft '+'{}'.format(draft_year)+' data Successfully loaded and transformed...')

print('Extraction and Transformation Complete!')


