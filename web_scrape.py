#!/usr/bin/env python
# coding: utf-8

# In[151]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


# In[150]:


#scrape html data using BeautifulSoup
def scrape_data(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text,
                        'lxml')

    #saves 'taux d'interet' table as a dictionary
    table = soup.find_all('div', {'class': 'taux_interet clear'})
    
    data = []
    
    #loops through table for value and title
    for value in table:
        item = {}
        
        #creates a dictionary with title as the key and % as the value
        item[value.find('span', {'class': 'type'}).text] = value.find('span', {'class': 'valeur'}).text.strip('\xa0%')
        
        data.append(item)
    
    return data


# In[152]:


#converts list of dictionaries to csv
def export_data(data):
    
    percent = []
    desc = []
    
    #loops through the list of dics and appends the value and description to their own respective lists
    
    for value in data:
        desc.append(list(value.keys()))
        percent.append(list(value.values()))
        
    #gets rid of list inside list
    desc = [elem[0] for elem in desc]
    
    df = pd.DataFrame(percent)
    
    #turns desc into a series
    df_index = pd.Series(desc)
    
    #set desc as the index
    df.set_index(df_index, inplace =True)
    
    #Names dataframe
    df = df.rename(columns={ df.columns[0]: "Taux d'intérêt" })
    
    print(df)
    
    return df


# In[149]:


if __name__ == '__main__':
    data = scrape_data('https://www.beac.int/')
    export_data(data)

