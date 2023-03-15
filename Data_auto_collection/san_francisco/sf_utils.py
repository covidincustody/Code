import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import openpyxl
import operator
import os
from csv import writer


def obtain_value(name,j):
    """
    Function: Obtain matched value in the name list
    In: name is a list and j is a string
    Out: a list containing the matched value
    """
    result = []
    count = 0
    for i in name:
        if j in i:
            a = name.index(i)
            result.append(value[a])
        else:
            count+=1

    if count == len(name):
        result.append('Null')
    return result



def san_franciso_auto(url):
    """
    Function: san_franciso_auto collection
    In: url for the san_franciso website
    Out: dataframe matched with the dataset containing from Active Cases (Incarcerated population, current) to Bookings (Incarcerated population, cumulative)
    """
    response = requests.get(url)
    results_page = BeautifulSoup(response.content,'lxml')
    A=results_page.find_all('div',class_='stat-stat')
    B=results_page.find_all('div',class_='stat-header')
    name = []
    value = []
    result_final = []
    for i in range(len(B)):
        name.append(B[i].get_text().strip().replace('\n',''))
        value.append(A[i].get_text().strip())
        
    result_final.extend(obtain_value(name,'active'))
    result_final.extend(obtain_value(name,'recorded positive'))
    result_final.extend(obtain_value(name,'death'))
    result_final.extend(obtain_value(name,'test'))
    result_final.extend(obtain_value(name,'released'))
    result_final.extend(obtain_value(name,'recovered cases'))
    result_final.extend(obtain_value(name,'population'))
    result_final.extend(obtain_value(name,'quarantined'))
    result_final.extend(obtain_value(name,'isolated'))
    result_final.extend(obtain_value(name,'bookings'))
    
    df=pd.DataFrame([result_final],
                columns=['Active Cases (Incarcerated population, current)',
                         'Confirmed Cases (Incarcerated population, cumulative)',
                         'Deaths (Incarcerated population, cumulative)',
                         'Tests (Incarcerated population, cumulative)',
                         'Released Cases (Incarcerated population, cumulative)',
                         'Resolved Cases in Custody (Incarcerated population, current)',
                         'Population (Incarcerated population, current)',
                         'Quarantined Cases (Incarcerated population, current)',
                         'Isolated Cases (Incarcerated population, current)',
                         'Bookings (Incarcerated population, cumulative)'])
    return df

