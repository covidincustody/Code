#!/usr/bin/env python
# coding: utf-8


"""
install and import all the pachages we will use in this function
"""
#!pip install word2number
import schedule
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from csv import writer
import re
from pandas.core.frame import DataFrame
import operator
import os
import numpy as np
import pandas as pd 
from word2number import w2n




def save_to_csv(address):
    """
    input:address
    output:csv file
    
    discription:save_to_csv function take address as input which is the local address we want to save
    the function well find out weather the csv file exist or not if it exist then
    will print out a message said "File exist" other weather it will create a new 
    empty csv file with column names 
    """       
    if os.path.exists(address):
        with open(address,mode='r',encoding='utf-8') as ff:    
            print("File exist")
    else:
        Data_collection = pd.DataFrame(columns=['Date','Active Cases (Incarcerated population, Net increase)','Confirmed Cases (Incarcerated population, cumulative)','Deaths (Incarcerated population, Net increase)','Tests (Incarcerated population, Net increase)',
                                   'Tests (Incarcerated population, cumulative)','Population (Incarcerated population, Net increase)','Hospitalizations (Incarcerated population, Net increase)','Hospitalizations (Incarcerated population, cumulative)',
                                   'At least one dose (Incarcerated population, cumulative)','First dose (Incarcerated population, Net increase)','Second dose (Incarcerated population, Net increase)','Boosted (Incarcerated population, Net increase)',
                                   'Total dose provided (Incarcerated population, Net increase)'])
    Data_collection.to_csv(address,index=False)




def COVID_Data_Collection(url):
    """
    input:url
    output:perday
    
    discription:COVID_Data_Collection fucntion take url as input which is the sacramento sheriff covide data offical website 
    by using the for loop the function will match the key words in the website and extract the corresponding number 
    and remove all the punctuation symbol in the number like "," and return a array which contain all the information
    in a single row
    """
    response = requests.get(url)
    results_page = BeautifulSoup(response.content,'html.parser')
    A=results_page.find_all("li")
    date=results_page.find_all("p")
    for i in A:
        if 'Total Inmate Population' in i.get_text():
            Total_Inmate=i.get_text().split()[-1]
        if 'COVID-19 tests' in i.get_text():
            Total_test = re.findall(r"(.*?)[(]", i.get_text().split(':')[1])[0].strip()
            Total_test_net=str(i.get_text().split()[-1])[0:-1]
        if 'Total number of confirmed COVID-19 cases since ' in i.get_text():
            Total_confirmed_March=re.findall(r"(.*?)[(]", i.get_text().split(':')[1])[0].strip()
            Total_confirmed_March_net=str(i.get_text().split()[-1])[0:-1]
        if ' intake observation/quarantine period ' in i.get_text():
            Total_quarantine=re.findall(r"(.*?)[(]", i.get_text().split(':')[1])[0].strip()
            Total_quarantine_net=str(i.get_text().split()[-1])[0:-1]
        if 'intake observation/quarantine period since ' in i.get_text():
            intake_observation=re.findall(r"(.*?)[(]", i.get_text().split(':')[1])[0].strip()
            intake_observation_net=str(i.get_text().split()[-1])[0:-1]
        if 'deaths' in i.get_text():
            deaths=i.get_text().split()[-1]
        if 'new inmates' in i.get_text():
            new_inmates=i.get_text().split()[3]
        if '2nd doses' in i.get_text():
            second=i.get_text().split()[3]
        if 'booster doses' in i.get_text():
            booster=i.get_text().split()[3]
        if 'doses provided' in i.get_text():
            total_dose=i.get_text().split()[2]
    for j in date:
        if ' inmates received at least one COVID-19 vaccine dose.' in j.get_text():
            day=str(j.get_text().split()[2])[0:-1]
            least_one_dose=j.get_text().split()[3]
                          
    perday=np.array([day,Total_confirmed_March_net,Total_confirmed_March,deaths,Total_test_net,Total_test,Total_Inmate,Total_quarantine_net,Total_quarantine,least_one_dose,new_inmates,second,booster,total_dose])
    for i in range(len(perday)):
        if operator.contains (perday[i], ','):
            perday[i]=w2n.word_to_num(str(perday[i].replace(',','')))#becasue sometime the number is in English so we need to translate into number 
        elif i!=0:                                                   #the package w2n.word_to_num will help us to do that
            perday[i]=w2n.word_to_num(str(perday[i]))
    return perday


def output_csv(list_data):
    """
    input:list_data
    output:csv file
    
    discription:output_csv function take list_data as input which is a array object and the array contain all the covid information
    and add the list_data into our csv file which is already created by the first function. If the data is duplicate
    the function will remove all the duplicate to make sure the data are unique and correct. Finally, output a csv file 
    to the address whcih we assign at first
    """
    with open(address, 'a', newline='') as f_object:  
        # Pass the CSV  file object to the writer() function
        writer_object = writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(list_data)  
        # Close the file object
        f_object.close()
    frame=pd.read_csv(address)
    data = frame.drop_duplicates()
    data.to_csv(address,index=False)
    
   




