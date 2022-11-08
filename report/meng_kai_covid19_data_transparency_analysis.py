# -*- coding: utf-8 -*-
"""Meng_Kai_COVID19_Data_Transparency_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cmow78EKnM_73m7ElGOctI6--tMxnXue

# **Data Transparency Analysis-Covid-In Custody**

## 1. Data Pre-processing

---


In this part, data-transparency reporting to BSCC is aggregrated to county/facility level and then the averges are calculated.



1) Import original files

2) ***BSCC_preprocessing function:*** Extract ‘Reporting to BSCC’ part and calculate duration

3) ***groupby_location function:*** Aggregate data to COUNTY/FACILITY level and calculate average


---

###Step1: Import original files
"""

#import original data-transparency files
import pandas as pd
from geopy.exc import GeocoderTimedOut
import numpy as np
import warnings
from geopy.geocoders import Nominatim
from geopy.point import Point
import folium
warnings.filterwarnings('ignore')
from dateutil.parser import parse
covid=pd.read_csv("https://raw.githubusercontent.com/kangkai20000518/Covid_In-Custody_Project_Data_sourse/main/County%20Jails%20COVID%20Data%20Tracker%20-%20Population%20Tracker.csv",header=[2,3,4],encoding="ISO-8859-1",error_bad_lines=False)
covid.head()

"""### Step2: Extract ‘Reporting to BSCC’ part and calculate duration"""

def BSCC_preprocessing(df):
    
    """
    this function is called preprocessing it take a dataframe as input which is data tracker in this case and indentify which columns
    are belongs to Reporting to BSCC and it will also change multiindex to make sure there is only one column name for each column
    the final return type is also a dataframe
    """
    def preprocessing(df):
        covid_names = df.head(0)
        covid_names=list(df)
        first_row_index = [i[0] for i in covid_names]
        second_row_index = [i[1] for i in covid_names]
        wb_index=second_row_index.index('Reporting on website')
        temp=covid[first_row_index[0:wb_index]]#only extract county facility and time period
        temp.columns = temp.columns.droplevel(1).droplevel(1)
        bscc_index=second_row_index.index('Reporting to BSCC') 
        BSCC=covid[first_row_index[bscc_index:-2]]#only extract Reporting to BSCC
        BSCC.columns = BSCC.columns.droplevel().droplevel()
        BSCC=pd.concat([temp,BSCC], axis=1)
        for i in range(1,BSCC.shape[0]):
            for j in list(BSCC.columns):
                if pd.isna(BSCC.loc[i,j])==True:
                    BSCC.loc[i,j]=BSCC.loc[i-1,j]
            
        return BSCC
    
    df=preprocessing(df)#call preprocessing to get the output    
    """
    This function is called cal_time
    which can add three more columns named as Duration, Start_Day, End_Day, and calculate time period between Start_Day and End_Day
    and the function will return a dataframe
    """
#Separate Time-period into Start_Day and End_Day & counting the duration
    def cal_time(df):
        df.insert(loc=3,column='Duration', value=0)
        df.insert(loc=4,column='Start_Day', value=0)
        df.insert(loc=5,column='End_Day', value=0)
        for i in range(0,len(df)):
            position=df["Time Period"][i].rfind(" - ")
            start=df["Time Period"][i][0:position]
            end=df["Time Period"][i][position+3:]
            df.loc[i, 'Start_Day'] = start
            df.loc[i, 'End_Day'] = end
            df.loc[i, 'Duration'] = (parse(end)-parse(start)).days
        return df
    
    df=cal_time(df)#call cal_time to get the output
    

    return df

"""*The Duration, Start_Day and End_day are added into the file"""

BSCC=BSCC_preprocessing(covid)
BSCC.head()

"""### Step3: Aggregate data to COUNTY/FACILITY level and calculate average"""

def groupby_location(df,string):
    df1=df.copy()
    """
    # because there is a different between group by county and facility so which means there Time Period 
    and Duration will also get change so the function group_concat will get the correct time information 
    result for county and facility
    """
    def group_concat(df1):
        df1['Time Period'] = ' , '.join(set(df1['Time Period']))
        return df1.drop_duplicates()
    if string=="County":
        time_info=df1[[string,"Time Period"]].groupby([string],group_keys=False,sort=False).apply(group_concat)#call function get time info
    else:
        time_info=df1[["County","Facility","Time Period"]].groupby(["Facility"],group_keys=False,sort=False).apply(group_concat)
    cols=list(df1.columns)[6:]
    for i in range(len(cols)):#calcualte total days
        df1[cols[i]]=df1[cols[i]]*df1["Duration"]
    BSCC_by_location=df1.groupby([string]).sum()
    BSCC_by_location.reset_index(inplace=True)
    for i in range(len(cols)):#calcualte percentage
        BSCC_by_location[cols[i]]=round(BSCC_by_location[cols[i]]/BSCC_by_location["Duration"],2)
    BSCC_by_location=pd.merge(time_info,BSCC_by_location)
    return BSCC_by_location

"""*The data is aggregated at the COUNTRY level"""

County=groupby_location(BSCC,string="County")
County.head()

"""*The data is aggregated at the FACILITY level"""

Facility=groupby_location(BSCC,string="Facility")
Facility.head()

"""# 2. Data Visualization

---


In this part, the data-transparency of facilities is shown on map and that of counties is shown on scattergram.


**-FACILITY**

1) Calculate the mean of 9 columns

2) ***do_geocode function:*** obtain the latitude and longitude of locations

3) Map-illustration with 6 colors

【Conclusion】: 5 facilities in poor data-transparency


**-COUNTY**

1) Calculate the mean of 9 columns and classified with 6 colors

2) Scattergram

【Conclusion】: 9 counties in poor data-transparency (5 red & 4 darkred)


---

FACILITY PART:

### Step1: Calculate the mean of columns
"""

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.point import Point
import folium

geo=Nominatim(user_agent='my-test-app')
df=Facility
df=df.drop('Duration',axis=1)
df=df.drop('County',axis=1)
df1=df.drop('Facility',axis=1)
df1=df1.drop('Time Period',axis=1)
df1=df1.astype(float)
fac=df['Facility'].tolist()

df['mean']=np.mean(df1,axis=1)#obtain the mean of the 9 columns for each facility

df

"""### Step2: Obtain the latitude and longitude of locations"""

#Use geopy to obtain the latitude and longitude of locations
def do_geocode(address, attempt=1, max_attempts=10):
    try:
        return geo.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return do_geocode(address, attempt=attempt+1)
        raise

lat=[]
lon=[]
geolocator = Nominatim()
for i in fac:
    Geo=do_geocode(i)
    if Geo is None:
        lat.append(np.nan)
        lon.append(np.nan)
        continue
    if geolocator.reverse(Point(Geo.latitude, Geo.longitude)).raw.get("address").get("state")=="California":
        lat.append(Geo.latitude)
        lon.append(Geo.longitude)
    else:
        lat.append(np.nan)
        lon.append(np.nan)

df['lat']=lat
df['lon']=lon
BSCC_map=df.dropna()

"""### Step3: Map-illustration with 6 colors"""

BSCC_map.head()

# 0-0.2；0.2-0.4；0.4-0.5；0.5-0.6；0.6-0.8 ;>0.8
m=[]
for i in BSCC_map['mean']:
    if 0<=i<0.2:
        m.append('darkred')
    elif 0.2<=i<0.4:
        m.append('red')
    elif 0.4<=i<0.5:
        m.append('lightred')
    elif 0.5<=i<0.6:
        m.append('lightgreen')
    elif 0.6<=i<0.8:
        m.append('green')
    elif 0.8<=i:
        m.append('darkgreen')
# green means good data-transparency; red means poor data-transparency

BSCC_map['grade']=m
BSCC_map=BSCC_map.dropna()

fac=BSCC_map['Facility'].tolist()
tim=BSCC_map['Time Period'].tolist()
mea=BSCC_map['mean'].tolist()
lat=BSCC_map['lat'].tolist()
lon=BSCC_map['lon'].tolist()
c=BSCC_map['grade'].tolist()
m = folium.Map(location=[37.351002,-121.905769], zoom_start=10)
for i in range(len(lat)):
    folium.Marker([lat[i],lon[i]], popup='【'+str(round(mea[i],2))+'】'+fac[i]+'   '+tim[i],icon=folium.Icon(color=c[i])).add_to(m)
m

"""COUNTY PART

### Step1: Calculate the mean of 9 columns and classified with 6 colors
"""

from plotly import express as px
County_analysis=County.drop(["Time Period","Duration"],axis=1)
County_analysis['mean']=np.mean(County_analysis,axis=1)
m=[]
for i in County_analysis['mean']:
    if 0<=i<0.2:
        m.append('darkred')
    elif 0.2<=i<0.4:
        m.append('red')
    elif 0.4<=i<0.5:
        m.append('lightred')
    elif 0.5<=i<0.6:
        m.append('lightgreen')
    elif 0.6<=i<0.8:
        m.append('green')
    elif 0.8<=i:
        m.append('darkgreen')
County_analysis['grade']=m

County_analysis.head()

"""### Step2: Scattergram"""

fig = px.scatter(data_frame = County_analysis, # data that needs to be plotted
                 x = "County", # column name for x-axis
                 y = "mean", # column name for y-axis
                 color = "grade", # column name for color coding
                 width = 1000,
                 height = 500)

# reduce whitespace
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# show the plot
fig.show()

"""## 3. Urban & Rural Analysis

---
In this part, the relationship between data-transparency and urban-level is calculated. 

**The results show that there is no correlation.**

1) Use official region codes to show urban-level

2) Calculate correlation

---

### Step1: Region codes for urban-level
"""

covid=pd.read_csv("https://raw.githubusercontent.com/kangkai20000518/Covid_In-Custody_Project_Data_sourse/main/Copy%20of%20NCHSURCodes2013.csv",error_bad_lines=False)
covid.head()
urban_code=covid##because in region code data set there is a space after county hence before we merge two data set we need to delate the space first
v=[]
for i in urban_code['County']:
  b=i.strip()
  v.append(b)
urban_code['County']=v
County_Urban= pd.merge(County_analysis,urban_code,on=['County'])

County_Urban.head()

"""### Step 2: Calculate correlation"""

corr=County_Urban[["Active cases","Cumulative confirmed cases",	"Resolved cases in custody","Deaths",	"Testing",	"Population",	"Vaccinations",	"Frequency",	"History available",	"2013 code"]]
for column in corr[["2013 code"]]:
    corr[column] = (corr[column] - corr[column].min()) / (corr[column].max() - corr[column].min())    
corr=corr.corr()
corr.fillna(value=0)

from google.colab import drive
drive.mount('drive')
County_Urban.to_csv('County_Urban.csv',index =False ,sep = ',')
!cp County_Urban.csv "drive/My Drive/"