import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

#get data of quali session from 2026 season.
schedule = fastf1.get_event_schedule(2026)
event = schedule.get_event_by_round(2)
quali_session = event.get_qualifying()
quali_session.load(
    laps=True,
    telemetry=True,
    weather=False,
    messages=False
    )

#pick the FL from each team during quali. Only completed lap is picked.
ferrari_fl = quali_session.laps.pick_teams("Ferrari").pick_accurate().pick_fastest()
merc_fl = quali_session.laps.pick_teams("Mercedes").pick_accurate().pick_fastest()

#get telemetory and add distance information
ferrari_telemetry = ferrari_fl.get_car_data().add_distance()
merc_telemetry = merc_fl.get_car_data().add_distance()

#get team color
ferrari_color = fastf1.plotting.get_team_color("Ferrari", quali_session)
merc_color = fastf1.plotting.get_team_color("Mercedes", quali_session)

#load circuit info to take information about the location of the corners 
circuit_info = quali_session.get_circuit_info()


#background color setting
plt.style.use("dark_background")

#make figure. 4 graphs are put virtically and x is shared.
fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(5, 1, sharex = "all", tight_layout = True, figsize = (15, 15))
#Draw vertical dotted lines at each corner
ferrari_min = ferrari_telemetry["Speed"].min()
merc_min = merc_telemetry["Speed"].min()
ferrari_max = ferrari_telemetry["Speed"].max()
merc_max = merc_telemetry["Speed"].max()
v_min = min(ferrari_min,  merc_min)
v_max = max(ferrari_max, merc_max)
ax1.vlines(x = circuit_info.corners["Distance"],
           ymin = v_min-40,
           ymax = v_max+20,
           color = "gray",
           linestyle = "--")
ax2.vlines(x = circuit_info.corners["Distance"],
           ymin = -5,
           ymax = 105,
           color = "gray",
           linestyle = "--")
ax3.vlines(x = circuit_info.corners["Distance"],
           ymin = -0.05,
           ymax = 1.05,
           color = "gray",
           linestyle = "--")
ax4.vlines(x = circuit_info.corners["Distance"],
           ymin = 0.5,
           ymax = 8.5,
           color = "gray",
           linestyle = "--")



#make Distance vs Speed, Throttle, Brake, gear graph
ax1.plot(ferrari_telemetry["Distance"],
         ferrari_telemetry["Speed"], 
         label = ferrari_fl["Driver"], 
         color = ferrari_color)
ax1.plot(merc_telemetry["Distance"], 
         merc_telemetry["Speed"], 
         label = merc_fl["Driver"], 
         color = merc_color)
ax2.plot(ferrari_telemetry["Distance"], 
         ferrari_telemetry["Throttle"], 
         label = ferrari_fl["Driver"], 
         color = ferrari_color)
ax2.plot(merc_telemetry["Distance"], 
         merc_telemetry["Throttle"], 
         label = merc_fl["Driver"], 
         color = merc_color)
ax3.plot(ferrari_telemetry["Distance"], 
         ferrari_telemetry["Brake"], 
         label = ferrari_fl["Driver"], 
         color = ferrari_color)
ax3.plot(merc_telemetry["Distance"], 
         merc_telemetry["Brake"], 
         label = merc_fl["Driver"], 
         color = merc_color)
ax4.plot(ferrari_telemetry["Distance"], 
         ferrari_telemetry["nGear"], 
         label = ferrari_fl["Driver"], 
         color = ferrari_color)
ax4.plot(merc_telemetry["Distance"], 
         merc_telemetry["nGear"], 
         label = merc_fl["Driver"], 
         color = merc_color)
ax4.set_xlabel("Distance [m]")
ax1.set_ylabel("Speed [kph]")
ax2.set_ylabel("Throttle [%]")
ax3.set_ylabel("Brake")
ax4.set_ylabel("nGear")
fig.suptitle(
    f"{event['EventName']} 2026 Qualifying\nMercedes vs Ferrari Fastest Lap Comparison",
    y=0.99
)
#ax0.set_title(f"{event['EventName']} 2026 Qualifying\nMercedes vs Ferrari Fastest Lap Comaparison"
#              ,y=1.1)
ax1.set_ylim(v_min-40, v_max+20)
ax2.set_ylim(-5, 105)
ax3.set_ylim(-0.05, 1.05)
ax4.set_ylim(0.5, 8.5)
ax3.set_yticks(range(0, 2))
ax4.set_yticks(range(1, 9, 2))
ax4.set_yticks(range(1, 9), minor = True)
ax4.grid(which = "major", alpha = 0.3)
ax4.grid(which = "minor", alpha = 0.2)


#------make delta-------
base_dis = min(ferrari_telemetry["Distance"].max(),
               merc_telemetry["Distance"].max())
dis = np.arange(0, base_dis, 5)
ferrari_time = ferrari_telemetry.set_index("Distance")["Time"]
ferrari_time = ferrari_time.dt.total_seconds()
ferrari_time_arranged = np.interp(dis,
                                 ferrari_time.index,
                                 ferrari_time.values)
merc_time = merc_telemetry.set_index("Distance")["Time"]
merc_time = merc_time.dt.total_seconds()
merc_time_arranged = np.interp(dis,
                              merc_time.index,
                              merc_time.values)

delta_time = merc_time_arranged - ferrari_time_arranged

#delta line
ax0.plot(dis, delta_time, color="#FF4500", linewidth=1.5)

#zero line
ax0.axhline(0, color="grey", linestyle = "--", linewidth = 1)

# color fill
ax0.fill_between(
    dis, delta_time, 0,
    where=(delta_time >= 0),
    color=ferrari_color,
    alpha=0.35,
    interpolate=True
)
ax0.fill_between(
    dis, delta_time, 0,
    where=(delta_time < 0),
    color=merc_color,
    alpha=0.35,
    interpolate=True
)

ax0.set_ylabel("Delta [s]")
ax0.set_ylim(delta_time.min()-0.05, delta_time.max()+0.05)

ax0.vlines(x = circuit_info.corners["Distance"],
           ymin = delta_time.min()-0.05, 
           ymax =delta_time.max()+0.05, 
           color = "gray", 
           linestyle = "--")

#corner number above the graph
for _, corner in circuit_info.corners.iterrows():
    txt = f"T{corner['Number']}{corner['Letter']}"
    ax0.text(corner['Distance'], 
             delta_time.max()+0.2, 
             txt, 
             va = 'center_baseline', 
             ha = 'center', 
             size = 'medium', 
             color = "lightgrey",
             rotation = 45)

# custom legend for delta meaning
delta_legend = [
    Line2D([0], [0], color=ferrari_color, lw=6, alpha=0.7,
           label=f"{ferrari_fl['Driver']}"),
    Line2D([0], [0], color=merc_color, lw=6, alpha=0.7,
           label=f"{merc_fl['Driver']}"),
]

ax0.legend(handles=delta_legend, loc="lower left")
plt.savefig("example.png", dpi=300)
plt.show()


