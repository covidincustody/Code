
from sf_utils import *

address=r'C:\Users\gemini\Desktop\Data_collection_SF.csv' ###please change your local address right here

if os.path.exists(address):
    with open(address,mode='r',encoding='utf-8') as ff:    
        print("File exist")
else:
    san_franciso_auto().to_csv(address,index=False)

