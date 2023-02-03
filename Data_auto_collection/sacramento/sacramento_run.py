from sacramento_utils import *
"""
url is the address of the offcial sacramento sheriff covid data website
address is the local address that will save the csv output
"""
url='https://www.sacsheriff.com/pages/covid19.php'
address=r'C:\Users\kangk\Desktop\Data_collection_Sacramento.csv'
save_to_csv(address)#call save_to_csv to create or open csv file
list_data=COVID_Data_Collection(url)# call COVID_Data_Collection to extract data
output_csv(list_data)# call output_csv to output final csv file 
