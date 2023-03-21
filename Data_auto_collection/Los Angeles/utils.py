# First install software from https://github.com/UB-Mannheim/tesseract/wiki    
# After installation, do not change the path
def la_auto_collection():
    get_ipython().system('pip install pytesseract')
    get_ipython().system('pip install pillow')
    get_ipython().system('pip install fitz ')
    get_ipython().system('pip install opencv-python')
    get_ipython().system('pip install PyMuPDF')
    import os
    import pandas as pd
    import re
    import numpy as np
    import requests
    from bs4 import BeautifulSoup
    import operator
    from PIL import Image
    from pytesseract import pytesseract
    from csv import writer
    address=r'C:\Users\kangk\Desktop\Data_collection_LA.csv' ###please change your local address right here
    if os.path.exists(address):
        with open(address,mode='r',encoding='utf-8') as ff:    
            print("File exist")
    else:
        Data_collection = pd.DataFrame(columns=["As of Date","Active Cases (Incarcerated population, current)","Deaths (Incarcerated population, cumulative)","Resolved Cases (Incarcerated population, cumulative)","Population (Incarcerated population, current)","Quarantined Cases (Incarcerated population, current)","Isolated Cases (Incarcerated population, current)","Bookings (Incarcerated population, 1-day diff)"])
        Data_collection.to_csv(address,index=False)

    ### download file
    res = requests.get('https://lasd.org/covid19updates/')
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

    date=re.findall("Custody Division COVID-19 Fact Sheet (\d{2}/\d{2}/\d{4})",text)[0]
    Current_Total_Confirmed=re.findall(r"Total Confirmed (\d*,?\d*)",text)[0]
    patient_deaths =re.findall(r"Total number of patient deaths (\d*,?\d*)",text)[0]
    patient_recover =re.findall(r"Total positive COVID-19 Recovered (\d*,?\d*)",text)[0]
    Jail_Population=re.findall(r"Jail Population[A-Za-z\s\(\)]*(\d*,?\d*)",text)[0]
    total_list=re.findall(r"Total[\s]*(\d*,?\d*)",text)
    while "" in total_list:
        total_list.remove("")
    for i in range(len(total_list)):
        if operator.contains (total_list[i], ','):
            total_list[i]=total_list[i].replace(',','')#becasue sometime the number is in English so we need to translate into number
        total_list[i]=int(total_list[i])
    Total=sorted(total_list)[-2]
    Curren_Isolation_Total=re.findall(r"Isolation Total (\d*,?\d*)",text)[0]
    Daily_Bookings=re.findall(r"Total Daily Bookings (\d*,?\d*)",text)[0]
    perday=np.array([date,Current_Total_Confirmed,patient_deaths,patient_recover,Jail_Population,Total,Curren_Isolation_Total,Daily_Bookings])## after solve above problem then we can put data together
    for i in range(len(perday)):
        if operator.contains (perday[i], ','):
            perday[i]=perday[i].replace(',','')
    # The data assigned to the list 
    list_data=perday
    # Pre-requisite - The CSV file should be manually closed before running this code.
    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object
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
