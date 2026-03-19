import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from compare_quali import get_quali_session, get_fastest_lap, get_telemetry



def build_llm_input(telemetry1, telemetry2, step=5):
    base_dis = min(telemetry1["Distance"].max(),
               telemetry2["Distance"].max())
    dis = np.arange(0, base_dis, step)

    t1 = telemetry1.set_index("Distance")["Time"]
    t1 = t1.dt.total_seconds()
    t1_interp = np.interp(dis,
                          t1.index,
                          t1.values)
    s1 = telemetry1.set_index("Distance")["Speed"]
    s1_interp = np.interp(dis, 
                          s1.index, 
                          s1.values)
    th1 = telemetry1.set_index("Distance")["Throttle"]
    th1_interp = np.interp(dis,
                           th1.index,
                           th1.values
                           )
    
    t2 = telemetry2.set_index("Distance")["Time"]
    t2 = t2.dt.total_seconds()
    t2_interp = np.interp(dis,
                          t2.index,
                          t2.values)
    s2 = telemetry2.set_index("Distance")["Speed"]
    s2_interp = np.interp(dis, 
                          s2.index, 
                          s2.values)
    th2 = telemetry2.set_index("Distance")["Throttle"]
    th2_interp = np.interp(dis,
                           th1.index,
                           th1.values
                           )
    delta = t2_interp - t1_interp
    max_speed_delta = s2_interp.max() - s1_interp.max()
    print(max_speed_delta)
    return dis, delta, max_speed_delta

def main():
    year = 2026
    round_number = 2
    team1 = "Aston Martin"
    team2 = "Mercedes"

    session, event = get_quali_session(year, round_number)

    lap1 = get_fastest_lap(session, team1)
    lap2 = get_fastest_lap(session, team2)

    tele1 = get_telemetry(lap1)
    tele2 = get_telemetry(lap2)

    build_llm_input(tele1, tele2)


if __name__ == "__main__":
    main()