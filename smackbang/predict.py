import numpy as np
import pandas as pd

def process_matches(df,city_one,city_two):
    '''This function preprocesses matches_df to be fed into the fare prediction model.
    Function takes in a dataframe, and the corresponding city_one and city_two, and returns

    need to split the matches_df into two seperate dataframes for each origin'''
    airports_df = pd.read_csv('../data/airport_codes.csv')

    #create the df for the city_one
    df1 = df.iloc[:,2:12:2]

    # convert local dearture to datetime
    df1[f'local_departure_{city_one}'] = pd.to_datetime(df1[f'local_departure_{city_one}'])

    # convert local arrival to datetime
    df1[f'local_arrival_{city_one}'] = pd.to_datetime(df1[f'local_arrival_{city_one}'])

    # create and format Date_of_Journey column based on local_departure
    df1['Date_of_Journey'] = df1[f'local_departure_{city_one}'].dt.date[0].strftime("%d/%m/%Y")

    # create and format Dep_Time column based on local_departure
    df1["Dep_Time"] = df1[f"local_departure_{city_one}"].apply(lambda x: x.strftime("%H:%M"))

    # create and format Arrival_time column based on local_arrival
    df1["Arrival_Time"] = df1[f"local_arrival_{city_one}"].apply(lambda x: x.strftime("%H:%M"))

    # create and format Duration
    df1['Duration'] = df1[f"duration_{city_one}"].apply(lambda x: f"{int(x)}h {(round(x*60)%60)}m")

    # Convert Total_Stops_city_one to strings
    df1[f'total_stops_{city_one}'] = df1[f'total_stops_{city_one}'].apply(str)

    # create Source Column based on city_one
    df1['Source'] = city_one

    # create placeholder column for Additional_Info. This column will be dropped during preproc pipeline
    df1['Additional_Info'] = "No info"

    # create placeholder column for Airline. This column will be dropped during preproc pipeline
    df1["Airline"] = "Multiple Carriers"

    #creating empty lat,long columns type float64
    df1['origin_one_latitude'] = np.nan
    df1['origin_one_longitude'] = np.nan

    # grabbing lat,lon from airports df
    for city in list(df1.index):
        if city in list(airports_df['city']):
            df1.loc[city,'origin_one_latitude']=list(airports_df[airports_df['city']==city]['lat'])[0]
            df1.loc[city,'origin_one_longitude']=list(airports_df[airports_df['city']==city]['lon'])[0]

    #creating empty lat,long columns type float64
    df1['origin_one_latitude'] = np.nan
    df1['origin_one_longitude'] = np.nan

    # grabbing lat,lon from airports df
    for city in list(df1.index):
        if city in list(airports_df['city']):
            df1.loc[city,'origin_one_latitude']=list(airports_df[airports_df['city']==city]['lat'])[0]
            df1.loc[city,'origin_one_longitude']=list(airports_df[airports_df['city']==city]['lon'])[0]

    df1['origin_two_latitude'] = np.nan
    df1['origin_two_longitude'] = np.nan

    df1['origin_two_latitude'] = list(airports_df[airports_df['city']==city_one]['lat'])[0]
    df1['origin_two_longitude'] = list(airports_df[airports_df['city']==city_one]['lon'])[0]

    # creating a new columns from the index which will be used for the Destination column
    df1 = df1.reset_index()

    # rename index column to Destination
    df1.rename(columns={'index':'Destination',f'total_stops_{city_one}':'Total_Stops'},inplace=True)

    # create placeholder column for Route. This column will be dropped during preproc pipeline
    df1['Route'] = df1["Source"] + "-" + df1["Destination"]

    df1_formatted = df1[['Airline','Date_of_Journey','Source','Destination',
                         'Route','Dep_Time','Arrival_Time','Duration','Total_Stops',
                         'Additional_Info','origin_one_latitude','origin_one_longitude',
                        'origin_two_latitude','origin_two_longitude']]

    df2 = df.iloc[:,3:12:2]

    # convert local dearture to datetime
    df2[f'local_departure_{city_two}'] = pd.to_datetime(df2[f'local_departure_{city_two}'])

    # convert local arrival to datetime
    df2[f'local_arrival_{city_two}'] = pd.to_datetime(df2[f'local_arrival_{city_two}'])

    # create and format Date_of_Journey column based on local_departure
    df2['Date_of_Journey'] = df2[f'local_departure_{city_two}'].dt.date[0].strftime("%d/%m/%Y")

    # create and format Dep_Time column based on local_departure
    df2["Dep_Time"] = df2[f"local_departure_{city_two}"].apply(lambda x: x.strftime("%H:%M"))

    # create and format Arrival_time column based on local_arrival
    df2["Arrival_Time"] = df2[f"local_arrival_{city_two}"].apply(lambda x: x.strftime("%H:%M"))

    # create and format Duration
    df2['Duration'] = df2[f"duration_{city_two}"].apply(lambda x: f"{int(x)}h {(round(x*60)%60)}m")

    # Convert Total_Stops_city_one to strings
    df2[f'total_stops_{city_two}'] = df2[f'total_stops_{city_two}'].apply(str)

    # create Source Column based on city_one
    df2['Source'] = city_two

    # create placeholder column for Additional_Info. This column will be dropped during preproc pipeline
    df2['Additional_Info'] = "No info"

    # create placeholder column for Airline. This column will be dropped during preproc pipeline
    df2["Airline"] = "Multiple Carriers"

    #creating empty lat,long columns type float64
    df2['origin_one_latitude'] = np.nan
    df2['origin_one_longitude'] = np.nan

    # grabbing lat,lon from airports df
    for city in list(df2.index):
        if city in list(airports_df['city']):
            df2.loc[city,'origin_one_latitude']=list(airports_df[airports_df['city']==city]['lat'])[0]
            df2.loc[city,'origin_one_longitude']=list(airports_df[airports_df['city']==city]['lon'])[0]

    #creating empty lat,long columns type float64
    df2['origin_one_latitude'] = np.nan
    df2['origin_one_longitude'] = np.nan

    # grabbing lat,lon from airports df
    for city in list(df2.index):
        if city in list(airports_df['city']):
            df2.loc[city,'origin_one_latitude']=list(airports_df[airports_df['city']==city]['lat'])[0]
            df2.loc[city,'origin_one_longitude']=list(airports_df[airports_df['city']==city]['lon'])[0]

    df2['origin_two_latitude'] = np.nan
    df2['origin_two_longitude'] = np.nan

    df2['origin_two_latitude'] = list(airports_df[airports_df['city']==city_one]['lat'])[0]
    df2['origin_two_longitude'] = list(airports_df[airports_df['city']==city_one]['lon'])[0]

    # creating a new columns from the index which will be used for the Destination column
    df2 = df2.reset_index()

    # rename index column to Destination
    df2.rename(columns={'index':'Destination',f'total_stops_{city_two}':'Total_Stops'},inplace=True)

    # create placeholder column for Route. This column will be dropped during preproc pipeline
    df2['Route'] = df2["Source"] + "-" + df2["Destination"]

    df2_formatted = df2[['Airline','Date_of_Journey','Source','Destination',
                        'Route','Dep_Time','Arrival_Time','Duration','Total_Stops',
                        'Additional_Info','origin_one_latitude','origin_one_longitude',
                        'origin_two_latitude','origin_two_longitude']]

    return df1_formatted, df2_formatted
