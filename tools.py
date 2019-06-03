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


def print_conflict(lecture_index, lecture, class_index, class_conf):
    statement = 'Wiersz {} ({}, {} {}) koliduje z\n' \
                'wierszem {} ({}, {} {})\n'.format(lecture_index + 2, lecture['przedmiot'], lecture['sala'],
                                                   lecture['godz'], class_index + 2, class_conf['przedmiot'],
                                                   class_conf['sala'], class_conf['godz'])
    print(statement)
