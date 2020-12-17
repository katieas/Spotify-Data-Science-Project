import pandas as pd
import numpy as np

def split_endTime(df):
    # Delete the endTime column and create two new columns: Date, Time
    df[['Date', 'Time']] = df.endTime.str.split(expand=True)
    df = df.set_index('Date')
    df = df.drop('endTime', axis=1)
    return df

def convert_timezone(df):
    tmp = pd.DatetimeIndex(pd.to_datetime(df['endTime'])).tz_localize('UTC').tz_convert('US/Pacific')
    df['endTime'] = tmp.strftime("%Y-%m-%d %H:%M")
    return df

def add_day_of_week(df):
    day_of_week = pd.DatetimeIndex(pd.to_datetime(df.index)).day_name()
    df['Day of Week'] = day_of_week
    return df

def add_skip_col(df):
    skip = df['secPlayed'] < 60 # listened to less than 60 seconds
    df['Skipped'] = skip
    
    num_skipped = 0
    for val in df["secPlayed"]:
        if val < 60: 
            num_skipped += 1
    return df, num_skipped
    #for i in range(0, len(df), 1):
        #if df['secPlayed'][i] > df['']
        
def get_most_artists(df):
    ser = pd.Series(name="Artist Count", dtype=int)
    grouped_artist = df.groupby("artistName")

    for group_name, group_df in grouped_artist:
        ser[group_name] = len(group_df)

    ser = ser.sort_values(ascending=False) # Most played sorted at the top
    return ser

def get_most_tracks(df):
    ser = pd.Series(name="Track Count", dtype=int)
    grouped_track = df.groupby("trackName")
    
    for group_name, group_df in grouped_track:
        ser[group_name] = len(group_df)
    
    ser = ser.sort_values(ascending=False) # Most played sorted at the top
    return ser

def mean_day_of_week(df):
    ser = pd.Series(name="Average Time (hours)", dtype=float) 

    grouped_dow = df.groupby("Day of Week")
    for group_name, group_df in grouped_dow:
        dow = [] # will contain times for all days on that day of the week
        grouped_day = group_df.groupby("Date")
        for day, day_df in grouped_day:
            times = np.sum(day_df["secPlayed"]) # sum time played for one day
            dow.append(times)
        ser[group_name] = np.mean(dow) / 60 / 60 # seconds to hours
        
    ser.index = pd.Categorical(ser.index, categories=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    ser = ser.sort_index()
    return ser

def split_weekdays(df):
    dow = {"Sunday":"Weekend", "Saturday":"Weekend", "Monday":"Weekday", "Tuesday":"Weekday", "Wednesday":"Weekday", "Thursday":"Weekday", "Friday":"Weekday"}
    weekend = []
    weekday = []
    
    grouped_dow = df.groupby("Day of Week")
    for group_name, group_df in grouped_dow:
        if dow[group_name] == "Weekend":
            weekend.extend(group_df["secPlayed"].tolist())
        if dow[group_name] == "Weekday":
            weekday.extend(group_df["secPlayed"].tolist()) 
    return weekend, weekday

def date_total_time(df):
    idx = pd.date_range(df.index[0], df.index[-1])
    
    ser = pd.Series(name="Time Listened By Date (hours)", dtype=int)
    grouped_date = df.groupby("Date")
    for group_name, group_df in grouped_date:
        ser[group_name] = sum(group_df['secPlayed']) / 60 / 60
    
    ser.index = pd.DatetimeIndex(ser.index)
    ser = ser.reindex(idx, fill_value=0)
    return ser
