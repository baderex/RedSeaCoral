#!/usr/bin/env python
# coding: utf-8

# In[139]:


import pandas as pd
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
from geopy import distance
import anvil.server
from datetime import datetime, timedelta
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


# In[59]:





# In[68]:





# In[127]:


coast_cities = pd.read_excel ("C:/Users/User/Downloads/ports_dataset.xlsx")
coast_cities_corddf = coast_cities[['lat','lng','port_name','country']]
coast_cities_cord = list(coast_cities_corddf.itertuples(index=False, name=None))


# In[105]:





# In[106]:





# In[145]:


'{:%Y/%m/%d %H:%M:%S}'.format(datetime.today())


# In[23]:





# In[28]:


url = "https://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/10"

response = urlopen(url)


# In[29]:


data_json = json.loads(response.read())


# In[107]:


coast_cities.head()


# In[40]:


elements = []
for name in data_json:
    elements.append(name)


# In[119]:


len(coast_cities)
coast_cities_cord


# In[44]:


events=data_json['events']


# In[109]:


cord_list=[]
for i in range(len(events)):
    e=events[i]
    geo=e['geometries']
    for j in range(len(geo)):
        g=geo[j]
        coords=g['coordinates']
        cord_list.append([float(coords[1]),float(coords[0])])


# In[114]:


#compare cord list and cities coord
city_event=[]
for cordi in cord_list:
    cctemp = coast_cities_cord
    ccfltr = filter(lambda cclat: abs(cclat[0]-cordi[0]) <=1, cctemp)
    for cordj in ccfltr:
        if distance.distance(cordi, cordj).km < 50:
            city_event.append(cordj)
            print(cordj)


# In[65]:


cord_list


# In[ ]:


anvil.server.connect("MR7WAVZXCRNPROCTVQQY7NDR-3WDV3IQYJHB5BW2F")

@anvil.server.callable
def say_hello(name):
  print("Hello from the uplink, %s!" % name)



@anvil.server.callable
def getEvents(name):
    #get events
    url = "https://eonet.sci.gsfc.nasa.gov/api/v3/categories/severeStorms"
    response = urlopen(url)
    data_json = json.loads(response.read())
    events=data_json['events']
    cord_list=[]
    for i in range(len(events)):
        e=events[i]
        geo=e['geometry']
        for j in range(len(geo)):
            g=geo[j]
            coords=g['coordinates']
            cord_list.append([float(coords[1]),float(coords[0])])
    
                
    url = "https://eonet.sci.gsfc.nasa.gov/api/v3/categories/volcanoes"
    response = urlopen(url)
    data_json = json.loads(response.read())
    events=data_json['events']
    
    for i in range(len(events)):
        e=events[i]
        geo=e['geometry']
        for j in range(len(geo)):
            g=geo[j]
            coords=g['coordinates']
            if len(coords)==2:
                cord_list.append([float(coords[1]),float(coords[0])])
    #filter for coastal
    city_event=[]
    for cordi in cord_list:
        cctemp = coast_cities_cord
        ccfltr = filter(lambda cclat: abs(cclat[0]-cordi[0]) <=1, cctemp)
        for cordj in ccfltr:
            if distance.distance(cordi, [cordj[0],cordj[1]]).km < 50:
                city_event.append(cordj)

                
    #build table of coords
    print('Evnts: {:%Y/%m/%d %H:%M:%S}'.format(datetime.today()))
    return city_event



@anvil.server.callable
def getCoast_cities(name):
    print('Cities: {:%Y/%m/%d %H:%M:%S}'.format(datetime.today()))
    return coast_cities_cord






anvil.server.wait_forever()


# In[160]:


url = "https://eonet.sci.gsfc.nasa.gov/api/v3/categories/severeStorms"
response = urlopen(url)
data_json = json.loads(response.read())
events=data_json['events']
cord_list=[]
for i in range(len(events)):
    e=events[i]
    geo=e['geometry']
    for j in range(len(geo)):
        g=geo[j]
        coords=g['coordinates']
        print(i,'-.-',j)
        cord_list.append([float(coords[1]),float(coords[0])])


url = "https://eonet.sci.gsfc.nasa.gov/api/v3/categories/volcanoes"
response = urlopen(url)
data_json = json.loads(response.read())
events=data_json['events']
cord_list=[]

for i in range(len(events)):
    e=events[i]
    geo=e['geometry']
    print(e['id'])
    for j in range(len(geo)):
        g=geo[j]
        coords=g['coordinates']
        if len(coords)==2:
            cord_list.append([float(coords[1]),float(coords[0])])
#filter for coastal
city_event=[]
for cordi in cord_list:
    cctemp = coast_cities_cord
    ccfltr = filter(lambda cclat: abs(cclat[0]-cordi[0]) <=1, cctemp)
    for cordj in ccfltr:
        if distance.distance(cordi, [cordj[0],cordj[1]]).km < 50:
            city_event.append(cordj)

                


# In[150]:


len(cord_list)

