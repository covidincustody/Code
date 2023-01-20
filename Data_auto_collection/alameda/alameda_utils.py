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


def get_data(url): #Ajax request: Return the latest url in the Daily Updates
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
        if 'Population:' in A[i].get_text():
            Population_IPC=A[i+2].get_text()
            Red_Patients=A[i+3].get_text()
        if 'ORANGE' in A[i].get_text():
            Orange_Patients=A[i-1].get_text()
        if 'Inmate Vaccinations:' in A[i].get_text():
            Fully_Vaccinated_cumulative=A[i+2].get_text()
            Fully_Vaccinated_current=A[i+4].get_text()
            Boosted=A[i+7].get_text()
    Date_string=A[1].get_text().split()
    Date_list=Date_string[4:]
    Date='{}/{}/{}'.format(Date_list[0],Date_list[1].strip(','),Date_list[2])
    
    perday=np.array([Date,Active_cases,Confirmed_Cases,Deaths,Tests_IPC,Pending_tests,Population_IPC,Hospitalizations,Red_Patients,Orange_Patients,'',Cases_Released_while_Active,
                     Cases_Released_after_Resolved,Resolved_Cases_Custody,Fully_Vaccinated_cumulative,Fully_Vaccinated_current,Boosted])
    for i in range(len(perday)):
        if operator.contains (perday[i], ','):
            perday[i]=perday[i].replace(',','')
    return perday


def alameda_auto_collection():
    url = 'https://content.govdelivery.com/accounts/ACSO/widgets/ACSO_WIDGET_2/0.json'#Ajax request url for Santa Rita jail
    url_dated=get_data(url)
    list_data=COVID_Data_Collection(url_dated)
    with open(r'C:\Users\gemini\Desktop\Data_collection_Santa-Rita.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_data)
        f_object.close()
    address=r'C:\Users\gemini\Desktop\Data_collection_Santa-Rita.csv'# change the csv location name while using
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
        

