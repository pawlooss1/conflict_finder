import pandas as pd
import datetime
import numpy as mp
import xlrd
import tools as *



def filter(df, lok, sala, dzien, godz):
    
    
    return df[(df['sala'] == sala) &
            (df['dzien'] == dzien) &
            (df['lok'] == lok) &
            (df['godz'] == godz)]


def filter_week(df, week):
    #Jeśli tydzień A lub B to ogranicza, a jeżeli AB to wypisuje wszystkie tygodnie
    if (week == 'A') | (week == 'B'):
        df = df[(df['tyg'] == week)]
    return df


def find_conflict(df):
    new = pd.DataFrame(columns=df.columns.tolist())
    hours = df['godz'].unique()
    lacations = df['lok'].unique()
    classrooms = df['sala'].unique()
    days = df['dzien'].unique()
    
    for hour in hours:
        for location in lacations:
            for classroom in classrooms:
                for day in days:
                    tmp_df = filter(df, location, classroom, day, hour)
                    
                    for week in tmp_df['tyg'].unique():
                        tmp2_df = filter_week(tmp_df, week)
                        if tmp2_df.shape[0] > 1:
                            new = pd.concat([tmp2_df, new])
                     
    
    return new.drop_duplicates(keep="first")
   


def finder(file_name, file_sheet1, file_sheet2, stationary = True):
    
    df = load_sheet(file_name, file_sheet1)
    df = clean_df(df)
    
    if stationary == True:
        df2 = load_sheet(file_name, file_sheet2)
        df2 = clean_df(df2)
        result = add(df, df2)
        
    result = df
    return find_conflict(result)

def add(df2, df):
    
    #w sumie chyba tego nie trzeba bo concat samo wie co gdzie dopasować
    #df2.rename(columns={'cel': 'przedmiot','od': 'godz','do': 'koniec'}, inplace=True)
    
    return (concat(df, df2))
    
