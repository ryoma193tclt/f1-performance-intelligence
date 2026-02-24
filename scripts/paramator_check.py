import fastf1
from fastf1.exceptions import DataNotLoadedError
import pandas as pd
fastf1.Cache.enable_cache("data/cache")

schedule = fastf1.get_event_schedule(2026)

#print(schedule)
#print(schedule[schedule["RoundNumber"] == 0].columns)

round0 = schedule[schedule["RoundNumber"] == 0]
mask = round0["OfficialEventName"].str.contains("PRE-SEASON TESTING 2 2026", case = False, na = False )
#for column in round0.columns:
if mask.sum() == 1:  
    print(round0.loc[mask, "OfficialEventName"])
else :
    print("there are more than two events with the same name, check the schedule")

event = fastf1.get_testing_event(2026, 2)
test_2_session1 = event.get_session(1)
try:
    test_2_session1 = test_2_session1.laps
except DataNotLoadedError:
    test_2_session1.load(laps = True)
    test_2_session1_normal = test_2_session1.laps
    print(test_2_session1_normal)
    cleanlaps = test_2_session1.laps[(test_2_session1.laps["IsAccurate"] == True) & (test_2_session1.laps["Deleted"] == False)]
    each_fastest = cleanlaps.groupby("Driver")["LapTime"].idxmin()
    print(cleanlaps.loc[each_fastest, ["Driver", "LapTime", "Team", "Stint", "Compound", "TyreLife"]])

#print(test_2_session1.columns)
#print(event["Session1"])
