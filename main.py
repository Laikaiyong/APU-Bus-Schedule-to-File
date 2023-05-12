import requests
import json
import pandas as pd
import numpy as np
from dateutil import parser


INCLUDED_BUSES = [
    "LRT - Bukit Jalil",
    "APU"
]

api_url = "https://api.apiit.edu.my/transix-v2/schedule/active"

response = requests.get(url=api_url)

bus_schedule = json.loads(response.text)["trips"]
# bus_schedule_df = pd.DataFrame.from_records(bus_schedule)
bus_schedule_df = pd.json_normalize(bus_schedule)

selected_schedules = bus_schedule_df[
    (
        (bus_schedule_df["trip_from.name"] == INCLUDED_BUSES[0])
        &
        (bus_schedule_df["trip_to.name"] == INCLUDED_BUSES[1])
    ) | (
        (bus_schedule_df["trip_from.name"] == INCLUDED_BUSES[1])
        &
        (bus_schedule_df["trip_to.name"] == INCLUDED_BUSES[0])    
    )
]

final_schedules = selected_schedules.copy()
final_schedules['datetime'] = final_schedules['time'].str[11:-9]


final_schedules = final_schedules.rename(
    columns = {
        "day": "Day",
        "datetime": "Time",
        "trip_from.name": "From",
        "trip_to.name": "To",
    }
)[
    [
        'Day',
        'Time',
        'From',
        'To'
    ]
].sort_values(
    by=[
        'From',
        'Day',
        'Time'
    ]
)

final_schedules.to_csv("busses.csv", index=False)