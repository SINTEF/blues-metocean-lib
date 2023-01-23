from datetime import datetime
import numpy as np

def subset(values, start_date: datetime, end_date: datetime,requested_values):
    """Reshape the values to lie between the given dates"""
    start_time = start_date.timestamp()
    end_time = end_date.timestamp()
    time =  values["time"].astype(np.long)
    ts=time[0]
    te=time[-1]
    if ts < start_time or te > end_time:
        indices = (time >= start_time) & (time <= end_time)
        values["time"] = time[indices]
        for name in requested_values:
            values[name]=values[name][indices]