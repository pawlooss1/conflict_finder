import pandas as pd
import datetime
import numpy as mp
import xlrd


def load_sheet(file_name, sheet_name):
    return pd.read_excel(file_name, sheet_name)



def filter_everything(df, lok, sala, tyg, dzien, sem, godz):
    if not isinstance(tyg, str):
        df = df[(df['sala'] == sala) &
                (df['dzien'] == dzien) &
                (df['lok'] == lok) &
                (df['sem'] == sem) &
                (df['godz'] == godz)]
    else:
        df = df[(df['sala'] == sala) &
                (df['dzien'] == dzien) &
                (df['tyg'] == tyg) &
                (df['lok'] == lok) &
                (df['sem'] == sem) &
                (df['godz'] == godz)]
    return df


def find_conflict(df):
    new = pd.DataFrame(columns=df.columns.tolist())
    for every_godz in df['godz'].unique():
        print('godz')
        for every_sem in df['sem'].unique():
            print('sem')
            for every_lok in df['lok'].unique():
                print("lok")
                for every_sala in df['sala'].unique():
                    print("sala")
                    for every_tyg in df['tyg'].unique():
                        print("tyg")
                        for every_dzien in df['dzien'].unique():
                            print("dzien")
                            df = filter_everything(df, every_lok, every_sala, every_tyg, every_dzien, every_sem, every_godz)
                            if df.shape[0] > 1:
                                new = pd.concat([df, new])
    return new


def finder(file_name, file_sheet1, file_sheet2):
    
    df = load_sheet(file_name, file_sheet1)
    df2 = load_sheet(file_name, file_sheet2)
    new_df = fits(df, df2)
    return find_conflict(new_df)

def fits(df2, df):

    df2.rename(columns={'cel': 'przedmiot','od': 'godz','do': 'koniec'}, inplace=True)
    
    return (concat(df, df2))
    