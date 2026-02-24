import fastf1
from fastf1.exceptions import DataNotLoadedError

def get_testing_session(year, test_number, session_number):
    event = fastf1.get_testing_event(year, test_number)
    return event.get_session(session_number)

#def fastest_laps_by_driver():

test = get_testing_session(2026, 2, 1)
