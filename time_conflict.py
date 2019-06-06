from tools import *


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


def find_conflict_with_lecture(lecture_index, lecture, classes, stationary):
    day = lecture['dzien']
    lecture_start = lecture['godz']
    if not isinstance(lecture_start, datetime.time):
        return
    if not isinstance(lecture['koniec'], datetime.time):
        lecture_end = add_90_minutes(lecture_start)
    else:
        lecture_end = lecture['koniec']
    if not stationary:
        first_day_index = find_non_stationary_days_index(classes.columns.values)
        days = classes.columns.values[first_day_index:]
        classes = classes[(lecture[days] == classes[days]).apply(fold_true, axis=1)]
    classes_to_check = classes[(classes['dzien'] == day) & check_week(lecture, classes)]
    for class_index, row in classes_to_check.iterrows():
        if check_pair_conflict(lecture_start, lecture_end, row):
            print_conflict(lecture_index, lecture, class_index, row)


def find_time_conflicts_semesters(df, stationary):
    lectures = df[df['typ'] == 'W']
    classes = df[(df['typ'] == 'L') | (df['typ'] == 'C') | (df['typ'] == 'P')]
    for index, lecture in lectures.iterrows():
        classes_and_lectures = pd.concat([classes, lectures.drop(lecture.name)])
        find_conflict_with_lecture(index, lecture, classes_and_lectures, stationary)


def find_time_conflicts_class_types(df, stationary):
    semesters = df['sem'].unique()
    for semester in semesters:
        tmp_df = df[df['sem'] == semester]
        find_time_conflicts_semesters(tmp_df, stationary)


def find_time_conflicts(file_name, sheet_name, stationary=True):
    print('*******************'
          'Sprawdzam konflikty terminów dla arkusza {}...'
          '*******************'.format(sheet_name))
    sheet = load_sheet(file_name, sheet_name)
    df = clean_df(sheet)
    class_types = df['studia'].unique()
    for class_type in class_types:
        tmp_df = df[df['studia'] == class_type]
        find_time_conflicts_class_types(tmp_df, stationary)
    print()
