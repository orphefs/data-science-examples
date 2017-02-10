#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This function uses pytrends package to scrape some data from Google Trends, at high resolution and for possibly long periods of time, by retrieving data in segments. 

Use example:
    
get_google_trends_timeseries('username@gmail.com', 'password', '1Jan2015','12Jan2016', 1, ['game of thrones', 'medieval'], 'US', "/home/orphefs/Downloads/")

@author: Orfeas Kypris (orphefs)
"""

def get_google_trends_timeseries(google_username, google_password, start_date, stop_date, no_segments, keyword_list, location, path):
    
    from pytrends.request import TrendReq
    import pandas as pd
    
    
    def date_range(start, stop, interv):
        from datetime import datetime
        start = datetime.strptime(start,"%d%b%Y")
        stop = datetime.strptime(stop,"%d%b%Y")
        diff = (stop  - start ) / interv
        for i in range(interv):
            yield (start + diff * i).strftime("%Y-%m-%d")
        yield stop.strftime("%Y-%m-%d")
        
    def create_date_pairs(dates_list):
        date_pairs = [dates_list[i]+" "+dates_list[i+1] for i in range(len(dates_list)-1)]
        return date_pairs
    
    # make sure no. of no_segments is an integer
    no_segments = int(no_segments)
    # create list of dates
    dates_list = list(date_range(start_date,stop_date,no_segments))
    # create list of date pairs for input to pytrends
    date_pairs = create_date_pairs(dates_list)
     
    # Use pytrends to get data from Google trends for each time interval
    #google_username = "happymunkster@gmail.com"
    #google_password = "*****"
    #keyword_list = ['gift boyfriend','gift girlfriend','gift dog']
    
    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrends = TrendReq(google_username, google_password, hl='en-US', tz=360, custom_useragent=None)
    
    # Download the data!
    gtdata_df = []
    for i in range(no_segments):
        pytrends.build_payload(keyword_list, cat=0, timeframe=date_pairs[i], geo=location, gprop='')
        gtdata_df.append(pytrends.interest_over_time())
    
    # Concatenate the pandas dataframes into one dataframe
    gtdata_df = pd.concat(gtdata_df)
    # Save into csv file (doesn't preserve datetime format for index)
    
    gtdata_df.to_csv(path_or_buf= path + keyword_list[0].replace(" ","_") + '.csv')
