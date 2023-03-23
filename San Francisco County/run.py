
from utils import *

address=r'C:\Users\gemini\Desktop\Data_collection_SF.csv' # Address to write the output or scraped data
url='https://www.sfsheriff.com/covid-19-jail-community-programs-sfso-staff-data' # url of the website with COVID-19 data

if os.path.exists(address):
    with open(address,mode='r',encoding='utf-8') as ff:    
        print("File exist")
else:
    san_franciso_auto(url).to_csv(address,index=False)

