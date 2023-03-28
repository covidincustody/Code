"""
install and import all the pachages we will use in this function
Also install sofeware from https://github.com/UB-Mannheim/tesseract/wiki    
and when install this software please do not change the path!
"""
import pandas as pd
import re
import numpy as np
import requests
from bs4 import BeautifulSoup
import operator
from PIL import Image
from pytesseract import pytesseract
from csv import writer


def save_to_csv(address):

    """
    Function Name: 
    save_to_csv

    Description:
    This function creates a CSV file with specified columns. If the CSV file already exists, the function checks if the existing columns match the specified columns. 
    If any columns are missing, the function adds them to the existing file. If the file does not exist, a new CSV file is created with the specified columns.


    Parameters:
    address - (str) the file path and name of the CSV file to be created or updated.

    Returns:
    None
    """  
    if os.path.exists(address) and list(pd.read_csv(address).columns) == cols:
        with open(address,mode='r',encoding='utf-8') as ff:    
            print("File exist")
    elif os.path.exists(address) and list(pd.read_csv(address).columns) !=cols:
        raise ValueError('You are changing the columns go want to gather compare to previse, please change your local save address to save new data file')
    else:
        Data_collection = pd.DataFrame(columns=cols)
        Data_collection.to_csv(address,index=False)


def text_extract(url):
    """
    Function Name: 
    text_extract

    Description:
    The purpose of this Python code provided and how to use it to extract text from an image. The code uses the BeautifulSoup and 
    requests modules to scrape an image from a webpage, then uses the pytesseract library to extract text from the image.

    Parameters:
    address - (str) the file path and name of the CSV file to be created or updated.
    cols - (list) a list of strings representing the column names for the CSV file.

    Returns:
    text - (str) text from the image
    """  
    ### download file
    res = requests.get(url)
    results_page = BeautifulSoup(res.text,'lxml')
    A=results_page.find_all('div', class_="grve-media")
    img_url=A[0].find('img').get('src')
    img_con = requests.get(img_url)
    f = open('covid_la.jpg','wb')
    f.write(img_con.content)
    f.close()
    #Define path to tessaract.exe
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #Define path to image
    path_to_image = 'covid_la.jpg'
    #Point tessaract_cmd to tessaract.exe
    pytesseract.tesseract_cmd = path_to_tesseract
    #Open image with PIL
    img = Image.open(path_to_image)
    #Extract text from image
    text = pytesseract.image_to_string(img)
    return text


def COVID_Data_Collection(text):
    """
    Function Name: 
    COVID_Data_Collection

    Description:
    The COVID_Data_Collection function is a Python function that is designed to extract specific information related to COVID-19 from a given input string. 
    The function uses regular expression patterns to extract the date of the report, total confirmed cases, total number of patient deaths, total jail
    population, total number of people in isolation, total daily bookings, current number of positive cases in custody, total number of confirmed positive 
    cases, total number of patient deaths due to COVID-19, and total number of patients recovered from COVID-19. The extracted information is then stored 
    in an array called perday.


    Parameters:
    text - (str) text from the image
    
    Returns:
    perday (numpy.array): A numpy array of the values extracted from the webpage for each column.
    """  
    # define regular expression patterns to extract information
    date_pattern = r"Custody Division COVID-19 Fact Sheet (\d{2}/\d{2}/\d{4})"
    confirmed_pattern = r"Current Isc Positives\n.*?\nTotal Confirmed (\d+)"
    death_pattern = r"Total number of patient deaths (\d+)"
    jail_pop_pattern = r"Jail Population \(Custody Division Total ADP\) (\d+)"


    isolation_pattern = r"Isolation Total (\d+)"
    booking_pattern = r"Total Daily Bookings (\d+)"
    jail_population_pattern = r"Jail Population \(Custody Division Total ADP\) (\d+)"
    current_positive_pattern = r"Current Isc Positives\n.*?Current (\d+)\n"
    daily_bookings_pattern = r"Total Daily Bookings (\d+)"
    confirmed_positive_pattern = r"Total Confirmed (\d+)"
    patient_deaths_pattern = r"Total number of patient deaths (\d+)"
    patient_recovered_pattern = r"Total positive COVID-19 Recovered (\d+)"

    # extract the information from the string

    date = re.search(date_pattern, text).group(1)
    confirmed = re.search(confirmed_pattern, text, re.DOTALL).group(1)
    death = re.search(death_pattern, text).group(1)
    jail_pop = re.search(jail_pop_pattern, text).group(1)

    isolation_total = re.search(isolation_pattern, text).group(1)
    daily_bookings = re.search(daily_bookings_pattern, text).group(1)
    jail_population = re.search(jail_population_pattern, text).group(1)
    current_positive = re.search(current_positive_pattern, text, re.DOTALL).group(1)
    confirmed_positive = re.search(confirmed_positive_pattern, text, re.DOTALL).group(1)
    patient_deaths = re.search(patient_deaths_pattern, text).group(1)
    patient_recovered = re.search(patient_recovered_pattern, text).group(1)
    
    perday=np.array([date,confirmed,death,jail_pop,daily_bookings,jail_population,current_positive,confirmed_positive,patient_deaths,patient_recovered])
    for i in range(len(perday)):
        if operator.contains (perday[i], ','):
            perday[i]=perday[i].replace(',','')
    return perday



def output_csv(list_data):
    
    """
    Function Name: 
    output_csv
    
    Description:
    The output_csv function writes the data provided in the list_data parameter to a CSV file. The CSV file is created if it doesn't exist, and if it exists, 
    the data is appended to the end of the file. The function then removes any duplicate rows from the CSV file to ensure data integrity.
    
    Parameters:
    list_data: a list of data to be written to a CSV file
    
    Returns:
    This function does not return any value..
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
