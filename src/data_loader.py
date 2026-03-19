import fastf1
from fastf1.exceptions import DataNotLoadedError

def get_testing_session(year, test_number, session_number):
    event = fastf1.get_testing_event(year, test_number)
    return event.get_session(session_number)

#def fastest_laps_by_driver():

#test = get_testing_session(2026, 2, 1)

def get_race_data(year, round):
    schedule = fastf1.get_event_schedule(year)
    event = schedule.get_event_by_round(round)
    race_session = event.get_race()
    return race_session.laps

print(get_race_data(2026, 1))