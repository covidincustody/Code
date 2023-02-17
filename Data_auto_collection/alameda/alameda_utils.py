#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import openpyxl
import operator
import os
from csv import writer
import csv


def ajax_request(url): 
    """
    Function: Ajax request-return the latest url in the Daily Updates
    In: the given url with Ajax
    Out: the url showing the required numbers
    """
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res = res.text.replace('GDWidgets[0].update(', '').replace(')', '')
    res = eval(res)
    res_first=res[0]
    url = res_first["href"]
    return url


def COVID_Data_Collection(url):#Obtain the data on the web
    """
    Function: Obtain the data on the Alameda web 
    In: the url showing the required numbers
    Out: dataframe with all required data; if none on the web, then return 0
    """
    response = requests.get(url)
    results_page = BeautifulSoup(response.content,'lxml')
    A=results_page.find_all("strong")
    for i in A:
        if 'positive' in i.get_text():
            Active_cases=i.get_text().split()[0]
    for i in range(len(A)-4):
        if 'Aggregate Statistics:' in A[i].get_text():
            Confirmed_Cases=A[i+3].get_text()
            Tests_IPC=A[i+1].get_text().strip()
            Pending_tests=A[i+4].get_text().strip()
            Hospitalizations=A[i+8].get_text().strip()
            Cases_Released_while_Active=A[i+7].get_text().strip()
            Cases_Released_after_Resolved=A[i+6].get_text().strip()
            Resolved_Cases_Custody=A[i+5].get_text().strip()
            Deaths=A[i+10].get_text().strip()
            break
        
            
        else:
            Confirmed_Cases=0
            Tests_IPC=0
            Pending_tests=0
            Hospitalizations=0
            Cases_Released_while_Active=0
            Cases_Released_after_Resolved=0
            Resolved_Cases_Custody=0
            Deaths=0
            
    for i in range(len(A)-4):        
        if 'Population:' in A[i].get_text():
            Population_IPC=A[i+2].get_text()
            Red_Patients=A[i+3].get_text()
            break
        else:
            Population_IPC=0
            Red_Patients=0
            
    for i in range(len(A)-4):            
        if 'ORANGE' in A[i].get_text():
            Orange_Patients=A[i-1].get_text()
            break
        else:
            Orange_Patients=0
    for i in range(len(A)-4):           
        if 'Inmate Vaccinations:' in A[i].get_text():
            Fully_Vaccinated_cumulative=A[i+2].get_text()
            Fully_Vaccinated_current=A[i+4].get_text()
            Boosted=A[i+7].get_text()
            break
        else:
            Fully_Vaccinated_cumulative=0
            Fully_Vaccinated_current=0
            Boosted=0
            
    Date_string=A[1].get_text().split()
    Date_list=Date_string[3:]
    Date='{}/{}/{}'.format(Date_list[0],Date_list[1].strip(','),Date_list[2])
    
    perday=np.array([Date,Active_cases,Confirmed_Cases,Deaths,Tests_IPC,Pending_tests,Population_IPC,Hospitalizations,Red_Patients,Orange_Patients,'',Cases_Released_while_Active,
                     Cases_Released_after_Resolved,Resolved_Cases_Custody,Fully_Vaccinated_cumulative,Fully_Vaccinated_current,Boosted])
    for i in range(len(perday)):
        if operator.contains (perday[i], ','):
            perday[i]=perday[i].replace(',','')
    return perday


def alameda_auto_collection(filepath):
    """
    Function: Obtain the latest data for alameda using 'ajax_request' and 'COVID_Data_Collection'
    In: the file_path with '.csv' of your datafile for storing the data
    Out: csv file with all required data
    """
    url = 'https://content.govdelivery.com/accounts/ACSO/widgets/ACSO_WIDGET_2/0.json'#Ajax request url for Santa Rita jail
    url_dated=ajax_request(url)
    list_data=COVID_Data_Collection(url_dated)
    with open(filepath, 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_data)
        f_object.close()
    address=filepath# change the csv location name while using
    if os.path.exists(address):
        with open(address,mode='r',encoding='utf-8') as ff:    
            print("File exist")
    else:
        Data_collection = pd.DataFrame(columns=['Date','Active Cases (Incarcerated population, current)', 'Confirmed Cases (Incarcerated population, cumulative)', 'Deaths (Incarcerated population, cumulative)','Tests (Incarcerated population, cumulative)',
                                       'Pending Tests (Incarcerated population, current)','Population (Incarcerated population, current)','Hospitalizations (Incarcerated population, cumulative)',
                                      'Red Patients (Incarcerated population, current)','Orange Patients (Incarcerated population, current)','Resolved Cases (Incarcerated population, cumulative)','Cases Released while Active (Incarcerated population, cumulative)',
                                      'Cases Released after Resolved (Incarcerated population, cumulative)','Resolved Cases in Custody (Incarcerated population, current)',
                                      'Fully Vaccinated (Incarcerated population, cumulative)','Fully Vaccinated (Incarcerated population, current)','Boosted (Incarcerated population, current)'])
        Data_collection.to_csv(address,index=False)    
        


def single_column_obtain(filepath,column_name):
    """
    Function: Obtain the specific number of a single column
    In: the file_path with '.csv' of your datafile for storing the data & required column name
    Out: the required number  
    """
    
    with open(filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if column_name=='Date':
                return row[0]
            elif column_name=='Active Cases(Incarcerated population, current)':
                return row[1]
            elif column_name=='Confirmed Cases (Incarcerated population, cumulative)':
                return row[2]
            elif column_name=='Deaths (Incarcerated population, cumulative)':
                return row[3]
            elif column_name=='Tests (Incarcerated population, cumulative)':
                return row[4]
            elif column_name=='Pending Tests (Incarcerated population, current)':
                return row[5]
            elif column_name=='Population (Incarcerated population, current)':
                return row[6]
            elif column_name=='Hospitalizations (Incarcerated population, cumulative)':
                return row[7]
            elif column_name=='Red Patients (Incarcerated population, current)':
                return row[8]
            elif column_name=='Orange Patients (Incarcerated population, current)':
                return row[9]
            elif column_name=='Resolved Cases (Incarcerated population, cumulative)':
                return row[10]
            elif column_name=='Cases Released while Active (Incarcerated population, cumulative)':
                return row[11]
            elif column_name=='Cases Released after Resolved (Incarcerated population, cumulative)':
                return row[12]
            elif column_name=='Resolved Cases in Custody (Incarcerated population, current)':
                return row[13]
            elif column_name=='Fully Vaccinated (Incarcerated population, cumulative)':
                return row[14]
            elif column_name=='Fully Vaccinated (Incarcerated population, current)':
                return row[15]
            else:
                return row[16]
            

