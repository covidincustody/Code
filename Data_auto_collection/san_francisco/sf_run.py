
from sf_utils import *

address=r'C:\Users\gemini\Desktop\Data_collection_SF.csv' ###please change your local address right here
url='https://www.sfsheriff.com/covid-19-jail-community-programs-sfso-staff-data' 

if os.path.exists(address):
    with open(address,mode='r',encoding='utf-8') as ff:    
        print("File exist")
else:
    san_franciso_auto(url).to_csv(address,index=False)

