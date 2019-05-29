import pandas as pd
import datetime


def load_sheet(file_name, sheet_name):
    return pd.read_excel(file_name, sheet_name)


def shrink_df(df, columns_to_leave):
    # wyrzuca puste wiersze i zostawia tylko kolumny z listy columns_to_leave
    df = df.dropna(thresh=2)
    return df[columns_to_leave]


def add_90_minutes(start_time):
    # pierwsze argumenty ponizszego konstruktora sa obowiazkowe ale nieistotne dla nas, stad stale wartosci
    full_start = datetime.datetime(100, 1, 1, start_time.hour, start_time.minute)
    delta = datetime.timedelta(seconds=5400)  # przesuniecie o 90 minut
    full_end = full_start + delta
    return full_end.time()  # zwroc sam czas


def check_pair_conflict(lecture_start, lecture_end, class_to_check):
    # sprawdz pare ktora jest w tym samym dniu (+ ew. w odpowiednim tygodniu)
    class_start = class_to_check['godz']
    if not isinstance(class_start, datetime.time):
        return False
    if not isinstance(class_to_check['koniec'], datetime.time):
        class_end = add_90_minutes(class_start)
    else:
        class_end = class_to_check['koniec']
    if lecture_start <= class_end <= lecture_end or lecture_start <= class_start <= lecture_end:
        return True
    else:
        return False


def print_conflict(lecture_index, lecture, class_index, class_conf):
    statement = 'Wiersz {} ({}, {} {}) koliduje z\n' \
                'wierszem {} ({}, {} {})\n'.format(lecture_index + 2, lecture['przedmiot'], lecture['sala'],
                                                   lecture['godz'], class_index + 2, class_conf['przedmiot'],
                                                   class_conf['sala'], class_conf['godz'])
    print(statement)


def find_conflict_with_lecture(lecture_index, lecture, classes):
    day = lecture['dzien']
    lecture_start = lecture['godz']
    if not isinstance(day, str) or not isinstance(lecture_start, datetime.time):
        return
    if not isinstance(lecture['koniec'], datetime.time):
        lecture_end = add_90_minutes(lecture_start)
    else:
        lecture_end = lecture['koniec']
    if not isinstance(lecture['tyg'], str):  # bez podzialu a/b
        classes_to_check = classes[classes['dzien'] == day]
    else:  # z podzialem a/b
        classes_to_check = classes[(classes['dzien'] == day) & (classes['tyg'] == lecture['tyg'])]
    for class_index, row in classes_to_check.iterrows():
        if check_pair_conflict(lecture_start, lecture_end, row):
            print_conflict(lecture_index, lecture, class_index, row)


def find_time_conflicts_semesters(df):
    lectures = df[df['typ'] == 'W']
    classes = df[(df['typ'] == 'L') | (df['typ'] == 'C') | (df['typ'] == 'P')]
    for index, row in lectures.iterrows():
        find_conflict_with_lecture(index, row, classes)


def find_time_conflicts_class_types(df):
    semesters = df['sem'].unique()
    for semester in semesters:
        tmp_df = df[df['sem'] == semester]
        find_time_conflicts_semesters(tmp_df)


def find_time_conflicts(file_name, sheet_name):
    sheet = load_sheet(file_name, sheet_name)
    df = shrink_df(sheet, ['studia', 'sem', 'przedmiot', 'typ', 'sala', 'tyg', 'dzien', 'godz', 'koniec'])
    class_types = df['studia'].unique()
    for class_type in class_types:
        tmp_df = df[df['studia'] == class_type]
        find_time_conflicts_class_types(tmp_df)
    # return df
