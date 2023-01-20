import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import openpyxl
import operator
import os
from csv import writer

def san_franciso():
    url='https://www.sfsheriff.com/covid-19-jail-community-programs-sfso-staff-data' #data update automatically; just run the code every day
    response = requests.get(url)
    results_page = BeautifulSoup(response.content,'lxml')
    A=results_page.find_all('div',class_='stat-stat')
    df=pd.DataFrame([[A[3].get_text().replace('\n',''),A[2].get_text().replace('\n',''),'',A[1].get_text().replace('\n',''),A[7].get_text().replace('\n',''),A[4].get_text().replace('\n',''),A[10].get_text().replace('\n',''),'','',A[0].get_text().replace('\n','')]],columns=['Active Cases (Incarcerated population, current)','Confirmed Cases (Incarcerated population, cumulative)','Deaths (Incarcerated population, cumulative)','Tests (Incarcerated population, cumulative)','Released Cases (Incarcerated population, cumulative)','Resolved Cases in Custody (Incarcerated population, current)','Population (Incarcerated population, current)','Quarantined Cases (Incarcerated population, current)','Isolated Cases (Incarcerated population, current)','Bookings (Incarcerated population, cumulative)'])
    df
    #df.to_excel('Data_collection_SF.xlsx')

    import os
    import pandas as pd
    address=r'C:\Users\gemini\Desktop\Data_collection_SF.csv'###please change your local address right here
    if os.path.exists(address):
        with open(address,mode='r',encoding='utf-8') as ff:    
            print("File exist")
    else:
        Data_collection = pd.DataFrame(columns=['Active Cases (Incarcerated population, current)','Confirmed Cases (Incarcerated population, cumulative)','Deaths (Incarcerated population, cumulative)','Tests (Incarcerated population, cumulative)','Resolved Cases (Incarcerated population, cumulative)','Population (Incarcerated population, current)','Quarantined Cases (Incarcerated population, current)','Isolated Cases (Incarcerated population, current)','Bookings (Incarcerated population,cumulative)'])
        Data_collection.to_csv(address,index=False)
