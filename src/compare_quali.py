import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

#get data of quali session from 2026 season.
def get_quali_session(year, round):
    schedule = fastf1.get_event_schedule(year)
    event = schedule.get_event_by_round(round)
    session = event.get_qualifying()
    session.load(
        laps=True,
        telemetry=True,
        weather=False,
        messages=False
        )
    return session, event

#pick the FL from each team during quali. Only completed lap is picked.
def get_fastest_lap(session, team):
    return session.laps.pick_teams(team).pick_accurate().pick_fastest()

#get telemetory and add distance information

def get_telemetry(lap):
    return lap.get_car_data().add_distance()





#------make delta-------
def compute_delta(telemetry1, telemetry2, step=5):
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
                          s1.index, 
                          s1.values)
    th2 = telemetry2.set_index("Distance")["Throttle"]
    th2_interp = np.interp(dis,
                           th1.index,
                           th1.values
                           )
    delta = t2_interp - t1_interp
    max_speed_delta = s2_interp.max() - s1_interp.max()
    return dis, delta, max_speed_delta


def plot_comparison(event, session, lap1, lap2, tele1, tele2, dis, delta, year):
    # get team color
    team1_color = fastf1.plotting.get_team_color(lap1["Team"], session)
    team2_color = fastf1.plotting.get_team_color(lap2["Team"], session)

    # load circuit info
    circuit_info = session.get_circuit_info()

    # background color setting
    plt.style.use("dark_background")

    # figure
    fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(
        5, 1, sharex="all", tight_layout=True, figsize=(15, 15)
    )

    # speed min/max
    tele1_min = tele1["Speed"].min()
    tele2_min = tele2["Speed"].min()
    tele1_max = tele1["Speed"].max()
    tele2_max = tele2["Speed"].max()
    v_min = min(tele1_min, tele2_min)
    v_max = max(tele1_max, tele2_max)

    # corner vertical lines
    ax1.vlines(
        x=circuit_info.corners["Distance"],
        ymin=v_min - 40,
        ymax=v_max + 20,
        color="gray",
        linestyle="--"
    )
    ax2.vlines(
        x=circuit_info.corners["Distance"],
        ymin=-5,
        ymax=105,
        color="gray",
        linestyle="--"
    )
    ax3.vlines(
        x=circuit_info.corners["Distance"],
        ymin=-0.05,
        ymax=1.05,
        color="gray",
        linestyle="--"
    )
    ax4.vlines(
        x=circuit_info.corners["Distance"],
        ymin=0.5,
        ymax=8.5,
        color="gray",
        linestyle="--"
    )

    # telemetry plots
    ax1.plot(
        tele1["Distance"], tele1["Speed"],
        label=lap1["Driver"], color=team1_color
    )
    ax1.plot(
        tele2["Distance"], tele2["Speed"],
        label=lap2["Driver"], color=team2_color
    )

    ax2.plot(
        tele1["Distance"], tele1["Throttle"],
        label=lap1["Driver"], color=team1_color
    )
    ax2.plot(
        tele2["Distance"], tele2["Throttle"],
        label=lap2["Driver"], color=team2_color
    )

    ax3.plot(
        tele1["Distance"], tele1["Brake"],
        label=lap1["Driver"], color=team1_color
    )
    ax3.plot(
        tele2["Distance"], tele2["Brake"],
        label=lap2["Driver"], color=team2_color
    )

    ax4.plot(
        tele1["Distance"], tele1["nGear"],
        label=lap1["Driver"], color=team1_color
    )
    ax4.plot(
        tele2["Distance"], tele2["nGear"],
        label=lap2["Driver"], color=team2_color
    )

    # labels and title
    ax4.set_xlabel("Distance [m]")
    ax1.set_ylabel("Speed [kph]")
    ax2.set_ylabel("Throttle [%]")
    ax3.set_ylabel("Brake")
    ax4.set_ylabel("nGear")

    fig.suptitle(
        f"{event['EventName']} {year} Qualifying\n"
        f"{lap2['Team']} vs {lap1['Team']} Fastest Lap Comparison",
        y=0.99
    )

    # y limits
    ax1.set_ylim(v_min - 40, v_max + 20)
    ax2.set_ylim(-5, 105)
    ax3.set_ylim(-0.05, 1.05)
    ax4.set_ylim(0.5, 8.5)

    # ticks
    ax3.set_yticks(range(0, 2))
    ax4.set_yticks(range(1, 9, 2))
    ax4.set_yticks(range(1, 9), minor=True)
    ax4.grid(which="major", alpha=0.3)
    ax4.grid(which="minor", alpha=0.2)

    # delta line
    ax0.plot(dis, delta, color="#FF4500", linewidth=1.5)

    # zero line
    ax0.axhline(0, color="grey", linestyle="--", linewidth=1)

    # delta fill
    ax0.fill_between(
        dis, delta, 0,
        where=(delta >= 0),
        color=team1_color,
        alpha=0.35,
        interpolate=True
    )
    ax0.fill_between(
        dis, delta, 0,
        where=(delta < 0),
        color=team2_color,
        alpha=0.35,
        interpolate=True
    )

    ax0.set_ylabel("Delta [s]")
    ax0.set_ylim(delta.min() - 0.05, delta.max() + 0.05)

    ax0.vlines(
        x=circuit_info.corners["Distance"],
        ymin=delta.min() - 0.05,
        ymax=delta.max() + 0.05,
        color="gray",
        linestyle="--"
    )

    # corner numbers
    for _, corner in circuit_info.corners.iterrows():
        txt = f"T{corner['Number']}{corner['Letter']}"
        ax0.text(
            corner["Distance"],
            delta.max() + 0.2,
            txt,
            va="center_baseline",
            ha="center",
            size="medium",
            color="lightgrey",
            rotation=45
        )

    # legend
    delta_legend = [
        Line2D([0], [0], color=team1_color, lw=6, alpha=0.7,
               label=f"{lap1['Driver']}"),
        Line2D([0], [0], color=team2_color, lw=6, alpha=0.7,
               label=f"{lap2['Driver']}"),
    ]
    ax0.legend(handles=delta_legend, loc="lower left")

    plt.savefig(f"{event['EventName']} {year} {lap1['Driver']} vs {lap2['Driver']}.png", dpi=300)

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

    dis, delta = compute_delta(tele1, tele2)

    plot_comparison(event, session, lap1, lap2, tele1, tele2, dis, delta, year)


if __name__ == "__main__":
    main()