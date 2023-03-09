"""
install and import all the pachages we will use in this function
"""
#!pip install word2number
import schedule
import time
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from csv import writer
import requests
import re
from pandas.core.frame import DataFrame
import operator
import os
import numpy as np
import pandas as pd 
from word2number import w2n




def create_csv_with_columns(address,cols=['Date','Active Cases (Incarcerated population, Net increase)','Confirmed Cases (Incarcerated population, cumulative)','Deaths (Incarcerated population, Net increase)','Tests (Incarcerated population, Net increase)',
                                   'Tests (Incarcerated population, cumulative)','Population (Incarcerated population, Net increase)','Hospitalizations (Incarcerated population, Net increase)','Hospitalizations (Incarcerated population, cumulative)',
                                   'At least one dose (Incarcerated population, cumulative)','First dose (Incarcerated population, Net increase)','Second dose (Incarcerated population, Net increase)','Boosted (Incarcerated population, Net increase)',
                                   'Total dose provided (Incarcerated population, Net increase)']):

    """
    Function Name: 
    create_csv_with_columns

    Description:
    This function creates a CSV file with specified columns. If the CSV file already exists, the function checks if the existing columns match the specified columns. 
    If any columns are missing, the function adds them to the existing file. If the file does not exist, a new CSV file is created with the specified columns.


    Parameters:
    address - (str) the file path and name of the CSV file to be created or updated.
    cols - (list) a list of strings representing the column names for the CSV file.

    Returns:
    None
    """  
    Data_collection = pd.DataFrame(columns=cols)
    if os.path.exists(address):
        Data_collection = pd.read_csv(address)
        existing_cols = list(Data_collection.columns)
        if existing_cols != cols:
            missing_cols = list(set(cols) - set(existing_cols))
            for col in missing_cols:
                Data_collection[col] = ''
    else:
        Data_collection = pd.DataFrame(columns=cols)
    Data_collection.to_csv(address, index=False)




def COVID_Data_Collection(url,cols=['Date','Active Cases (Incarcerated population, Net increase)','Confirmed Cases (Incarcerated population, cumulative)','Deaths (Incarcerated population, Net increase)','Tests (Incarcerated population, Net increase)',
                                   'Tests (Incarcerated population, cumulative)','Population (Incarcerated population, Net increase)','Hospitalizations (Incarcerated population, Net increase)','Hospitalizations (Incarcerated population, cumulative)',
                                   'At least one dose (Incarcerated population, cumulative)','First dose (Incarcerated population, Net increase)','Second dose (Incarcerated population, Net increase)','Boosted (Incarcerated population, Net increase)',
                                   'Total dose provided (Incarcerated population, Net increase)']):

    """
    Function Name: 
    COVID_Data_Collection

    Description:
    The function COVID_Data_Collection takes a url string and a list of column names as input and returns a numpy array containing the values extracted 
    from the webpage for each column. The function uses the requests and BeautifulSoup libraries to extract the webpage content and parse it. The function
    then searches for specific text in the webpage content for each column name, extracts the values, and stores them in the numpy array perday. The function 
    then returns this numpy array.
    Also, note that the default column names are set to the most recent column names found in the webpage at the time the function was last updated. 
    Therefore, the default column names may not match the column names currently found in the webpage. In this case, the user should provide a list 
    of the column names currently found in the webpage.

    Parameters:
    url (string): A string representing the url of the webpage to be scraped.
    cols (list): A list of column names to be extracted from the webpage.

    Returns:
    perday (numpy.ndarray): A numpy array of the values extracted from the webpage for each column.
    """
    response = requests.get(url)
    results_page = BeautifulSoup(response.content,'html.parser')
    A=results_page.find_all("li")
    date=results_page.find_all("p")
    perday = np.zeros(len(cols), dtype=object)
    for i in A:
        if 'Population (Incarcerated population, Net increase)' in cols and 'Total Inmate Population' in i.get_text():
            Total_Inmate=i.get_text().split()[-1]
            index = cols.index('Population (Incarcerated population, Net increase)')
            perday[index]=Total_Inmate
            
        if 'COVID-19 tests' in i.get_text():
            if 'Tests (Incarcerated population, cumulative)' in cols:
                Total_test = re.findall(r"(.*?)[(]", i.get_text().split(':')[1])[0].strip()
                index = cols.index('Tests (Incarcerated population, cumulative)')
                perday[index]=Total_test
            if 'Tests (Incarcerated population, Net increase)' in cols:
                Total_test_net=str(i.get_text().split()[-1])[0:-1]
                index = cols.index('Tests (Incarcerated population, Net increase)')
                perday[index]=Total_test_net
                
        if 'Total number of confirmed COVID-19 cases since ' in i.get_text() :
            if 'Confirmed Cases (Incarcerated population, cumulative)' in cols:
                Total_confirmed_March=re.findall(r"(.*?)[(]", i.get_text().split(':')[1])[0].strip()
                index = cols.index('Confirmed Cases (Incarcerated population, cumulative)')
                perday[index]=Total_confirmed_March
            if 'Active Cases (Incarcerated population, Net increase)' in cols:
                Total_confirmed_March_net=str(i.get_text().split()[-1])[0:-1]
                index = cols.index('Active Cases (Incarcerated population, Net increase)')
                perday[index]=Total_confirmed_March_net
                
        if 'intake observation/quarantine period since ' in i.get_text():
            if 'Hospitalizations (Incarcerated population, cumulative)' in cols:
                intake_observation=re.findall(r"(.*?)[(]", i.get_text().split(':')[1])[0].strip()
                index = cols.index('Hospitalizations (Incarcerated population, cumulative)')
                perday[index]=intake_observation            
            if 'Hospitalizations (Incarcerated population, Net increase)' in cols:
                intake_observation_net=str(i.get_text().split()[-1])[0:-1]
                index = cols.index('Hospitalizations (Incarcerated population, Net increase)')
                perday[index]=intake_observation_net            
        if 'Deaths (Incarcerated population, Net increase)'in cols and 'deaths' in i.get_text():
            deaths=i.get_text().split()[-1]
            index = cols.index('Deaths (Incarcerated population, Net increase)')
            perday[index]=deaths
            
        if 'First dose (Incarcerated population, Net increase)' in cols and 'new inmates' in i.get_text():
            new_inmates=i.get_text().split()[3]
            index = cols.index('First dose (Incarcerated population, Net increase)')
            perday[index]=new_inmates
            
        if 'Second dose (Incarcerated population, Net increase)' in cols and '2nd doses' in i.get_text():
            second=i.get_text().split()[3]
            index = cols.index('Second dose (Incarcerated population, Net increase)')
            perday[index]=second
            
        if 'Boosted (Incarcerated population, Net increase)' in cols and 'booster doses' in i.get_text():
            booster=i.get_text().split()[3]
            index = cols.index('Boosted (Incarcerated population, Net increase)')
            perday[index]=booster
            
        if  'Total dose provided (Incarcerated population, Net increase)'in cols and  'doses provided' in i.get_text():
            total_dose=i.get_text().split()[2]
            index = cols.index('Total dose provided (Incarcerated population, Net increase)')
            perday[index]=total_dose
            
    for j in date:
        if "Date" in cols and ' inmates received at least one COVID-19 vaccine dose.' in j.get_text():
            day=str(j.get_text().split()[2])[0:-1]
            index = cols.index('Date')
            perday[index]=day
            if 'At least one dose (Incarcerated population, cumulative)' in cols:
                least_one_dose=j.get_text().split()[3]
                index = cols.index('At least one dose (Incarcerated population, cumulative)')
                perday[index]=least_one_dose

    for i in range(len(perday)):
        if operator.contains(str(perday[i]), ','):
            perday[i] = w2n.word_to_num(str(perday[i].replace(',','')))
        elif isinstance(perday[i], int) or operator.contains(perday[i], '/'):
            continue
        else:
            perday[i]=int(perday[i])
    return perday


def output_csv(list_data):
    """   
    Function Name:
    output_csv

    Description:
    This function takes a list of data as input and writes it to a CSV file. It then reads the CSV file into a Pandas dataframe, 
    removes any duplicate rows, and overwrites the original CSV file with the updated data.
    Note that user will need to define the "address" variable within the function before calling it, 
    as this specifies the file path for the CSV file. Also note that the "address" variable should be a string containing the file
    path, including the file name and file extension.

    Input:
    list_data: A list of data to be written to a CSV file

    Output:
    perday (numpy.ndarray): A numpy array of the values extracted from the webpage for each column.

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
    
    
   




