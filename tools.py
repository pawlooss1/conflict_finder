import pandas as pd
import datetime


def load_sheet(file_name, sheet_name):
    return pd.read_excel(file_name, sheet_name)


def clean_df(df):
    # wyrzuca puste wiersze, a kolumny dzien i tyg
    # uzupelnia wartosciami domyslnymi (zeby nie bylo NaN i z nich skorzystac)
    df = df.dropna(thresh=2)
    return df.fillna(value={'dzien': 'noday', 'tyg': 'AB'})


def find_non_stationary_days_index(column_names):
    for i in range(len(column_names)):
        if column_names[i] == 'uwagi':
            return i + 1


def check_week(lecture, classes):
    values = []
    for i, c in classes.iterrows():
        values.append(c['tyg'] in lecture['tyg'] or lecture['tyg'] in c['tyg'])
    return pd.Series(data=values, index=classes.index)


def fold_true(row):
    acc = False
    for name in row.index:
        acc = acc or row[name]
        return acc


def add_90_minutes(start_time):
    # pierwsze argumenty ponizszego konstruktora sa obowiazkowe ale nieistotne dla nas, stad stale wartosci
    full_start = datetime.datetime(100, 1, 1, start_time.hour, start_time.minute)
    delta = datetime.timedelta(seconds=5400)  # przesuniecie o 90 minut
    full_end = full_start + delta
    return full_end.time()  # zwroc sam czas


def print_conflict(class_1_index, class_1, class_2_index, class_2):
    statement = 'Wiersz {} ({}, {} {}:{:02d}) koliduje z\n' \
                'wierszem {} ({}, {} {}:{:02d})\n'.format(class_1_index + 2, class_1['przedmiot'], class_1['sala'],
                                                          class_1['godz'].hour, class_1['godz'].minute,
                                                          class_2_index + 2, class_2['przedmiot'], class_2['sala'],
                                                          class_2['godz'].hour, class_2['godz'].minute)
    print(statement)
