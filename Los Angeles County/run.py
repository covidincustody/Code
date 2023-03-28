from utils import *

"""The code imports all functions from the module Los Angeles_utils using the syntax "from utils import *". 
This means that all functions defined in  Los Angeles_utils can be used directly in the code without the need to specify the module name.

The code then defines a URL from which to extract COVID-19 data and specifies the columns to be extracted from the data.

The function create_csv_with_columns is then called with the arguments 'address' and 'cols'. This function creates a new CSV file at the 
specified address (if it doesn't already exist) and adds the column headers specified in 'cols' to the CSV file.

The function text_extract is then called with the arguments 'url' This function extracts the COVID-19 data from the 
specified URL.

The function COVID_Data_Collection is then called with the arguments 'text'. This function extracts the COVID-19 data from the 
text and returns the data as a list.

The function output_csv is then called with the argument 'list_data'. This function appends the data in 'list_data' to the CSV file 
specified by 'address', removes any duplicate rows in the CSV file, and saves the updated CSV file.

In summary, the code imports functions from sacramento_utils, creates a new CSV file with column headers, extracts COVID-19 data 
from a specified URL, appends the data to the CSV file, removes any duplicate rows, and saves the updated CSV file.
"""

address=r'C:\Users\kangk\Desktop\Data_collection_LA.csv'
url='https://lasd.org/covid19updates/
cols=['date','confirmed','death','jail_pop','daily_bookings','jail_population','current_positive','confirmed_positive','atient_deaths','patient_recovered']
save_to_csv(address,cols) # Call to create or open csv file
text=text_extract(url)
list_data=COVID_Data_Collection(text)
output_csv(list_data) # Call to write output to final csv file 
