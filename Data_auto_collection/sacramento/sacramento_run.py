from sacramento_utils import *
"""The code imports all functions from the module sacramento_utils using the syntax "from sacramento_utils import *". 
This means that all functions defined in sacramento_utils can be used directly in the code without the need to specify the module name.

The code then defines a URL from which to extract COVID-19 data and specifies the columns to be extracted from the data.

The function create_csv_with_columns is then called with the arguments 'address' and 'cols'. This function creates a new CSV file at the 
specified address (if it doesn't already exist) and adds the column headers specified in 'cols' to the CSV file.

The function COVID_Data_Collection is then called with the arguments 'url' and 'cols'. This function extracts the COVID-19 data from the 
specified URL, filters the data to only include the columns specified in 'cols', and returns the data as a list.

The function output_csv is then called with the argument 'list_data'. This function appends the data in 'list_data' to the CSV file 
specified by 'address', removes any duplicate rows in the CSV file, and saves the updated CSV file.

In summary, the code imports functions from sacramento_utils, creates a new CSV file with column headers, extracts COVID-19 data 
from a specified URL, appends the data to the CSV file, removes any duplicate rows, and saves the updated CSV file.
"""

url='https://www.sacsheriff.com/pages/covid19.php'
cols=['Active Cases (Incarcerated population, Net increase)','Date']
address=r'C:\Users\kangk\Desktop\Data_collection_Sacramento.csv'
save_to_csv(address,cols)#call save_to_csv to create or open csv file
list_data=COVID_Data_Collection(url,cols)# call COVID_Data_Collection to extract data
output_csv(list_data)# call output_csv to output final csv file 
