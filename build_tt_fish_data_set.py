# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib
import os
import pandas as pd

from datetime import date, timedelta

# <codecell>

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def get_month(day):
    return months[day.month - 1]

def get_data(day, market):
    url = "http://www.namistt.com/DocumentLibrary/Market%20Reports/Daily/Daily%20" + \
        market + "%20" + str(day.day).zfill(2) + "%20" + get_month(day) + "%20" + str(day.year) + ".xls"
    print(url)
    response = urllib.request.urlopen(url)
    xlfile = pd.ExcelFile(response)
    df = xlfile.parse(xlfile.sheet_names[0], skiprows=range(0,10))
    df = df.dropna()
    df["Date"] = "%i%s%s" % (day.year,str(day.month).zfill(2),str(day.day).zfill(2))
    df["Market"] = market
    if len(df.columns) == 9: # fix some corruption of Column names
        df.columns = ['Commodity', 'Unit', 'Min', 'Max', 'Mode', 'Average', 'Volumes', 'Date', 'Market']
    return df

# <codecell>

base_path = "c:/data/"

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

def build_month(year,month,market):
    start_date = date(year,month,1)
    end_date = last_day_of_month(start_date)
    df = pd.DataFrame()
    d = start_date
    delta = datetime.timedelta(days=1)
    while d <= end_date and d <= date.today():
        try:
            ndf = get_data(d, market)
            df = pd.concat([df, ndf])
        except:
            print("Could not download data for %i %s %i" % (d.day, getMonth(d), d.year))
        d += delta
    file_path = base_path + market + "_" + str(year) + str(month).zfill(2) + ".csv"
    print(df)
    if len(df.columns) == 9:
        df = df[["Date","Market","Commodity","Unit","Min","Max","Mode","Average","Volumes"]]
    else:
        df = df[["Date","Market","Commodity","Unit","Min","Max","Mode","Volumes"]] # older data does not have Average
    df.to_csv(file_path, encoding="utf8", index=False)   
    return df



# <codecell>

#market = "POSWFM"
market = "OVWFM"
for month in range(12,0,-1):
    build_month(2012,month,market)

# <codecell>

df = pd.DataFrame()

for filename in os.listdir(basedir):
    if not filename.endswith("csv"):
        continue
    fd = pd.read_csv(basedir + filename)
    df = pd.concat([df,fd])
    
df.to_csv(basedir + "all/tt_fish_prices.csv", encoding="utf8", index=False)   

# <codecell>


