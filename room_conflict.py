from tools import *


def filter_everything(df, sala, dzien, godz):
    return df[(df['sala'] == sala) &
              (df['dzien'] == dzien) &
              (df['godz'] == godz)]


def filter_week(df, week):
    # Jeśli tydzień A lub B to ogranicza, a jeżeli AB to wypisuje wszystkie tygodnie
    if (week == 'A') | (week == 'B'):
        df = df[(df['tyg'] == week)]
    return df


def find_conflict(df):
    new = pd.DataFrame(columns=df.columns.tolist())
    hours = df['godz'].unique()
    classrooms = df['sala'].unique()
    days = df['dzien'].unique()

    for hour in hours:
        for classroom in classrooms:
            for day in days:
                tmp_df = filter_everything(df, classroom, day, hour)

                for week in tmp_df['tyg'].unique():
                    tmp2_df = filter_week(tmp_df, week)
                    if tmp2_df.shape[0] > 1:
                        new = pd.concat([tmp2_df, new])

    return new.drop_duplicates(keep="first")


def finder(file_name, file_sheet1, file_sheet2=None, stationary=True):
    df = load_sheet(file_name, file_sheet1)
    df = clean_df(df)

    if stationary:
        df2 = load_sheet(file_name, file_sheet2)
        df2 = clean_df(df2)
        result = add(df, df2)
    else:
        result = df
    return find_conflict(result)


def is_conflict(class1, class2):
    if class1['sala'] == class2['sala'] and class1['godz'] == class2['godz'] and ((class1['tyg'] in class2['tyg']) or (class2['tyg'] in class1['tyg'])):
        return True
    return False


def print_conflicts(df):
    for index1, class1 in df.iterrows():
        for index2, class2 in df.iterrows():
            if is_conflict(class1, class2) and index1 < index2:
                print_conflict(index1, class1, index2, class2)


def find_room_conflict(file_name, sheet_name, stationary=True):
    if stationary:
        sheet_name2 = sheet_name[:-1] + 'inne'
        print('*******************'
              'Sprawdzam konflikty sal dla arkusza {} i {}...'
              '*******************'.format(sheet_name, sheet_name2))
        conflicts = finder(file_name, sheet_name, sheet_name2, stationary=True)
    else:
        print('*******************'
              'Sprawdzam konflikty sal dla arkusza {}...'
              '*******************'.format(sheet_name))
        conflicts = finder(file_name, sheet_name, stationary=False)
    print_conflicts(conflicts)
    print()


def add(df2, df):
    return pd.concat([df, df2], sort=False)

