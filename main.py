from time_conflict import find_time_conflicts
from room_conflict import find_room_conflict

find_time_conflicts('2019-20203.xlsx', 'zima-s')
find_time_conflicts('2019-20203.xlsx', 'lato-s')
find_time_conflicts('2019-20203.xlsx', 'zima-n', stationary=False)
find_time_conflicts('2019-20203.xlsx', 'lato-n', stationary=False)
find_room_conflict('2019-20203.xlsx', 'zima-s')
find_room_conflict('2019-20203.xlsx', 'lato-s')
find_room_conflict('2019-20203.xlsx', 'zima-n', stationary=False)
find_room_conflict('2019-20203.xlsx', 'lato-n', stationary=False)
