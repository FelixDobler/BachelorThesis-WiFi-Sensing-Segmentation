from .types import CSI_Result
from . import  config
import numpy as np

def get_sample_rate(data: CSI_Result) -> float:
    first_frame = data.status[0].tstamp
    last_frame = data.status[-1].tstamp

    time_diff = last_frame - first_frame
    duration = time_diff/1e6

    num_frames = len(data.status)

    rate = num_frames/duration
    if config.be_verbose:
        print(f"Collected {num_frames} frames in {duration} seconds. Sample rate: {rate} frames per second")
    return rate

def get_intervals(data: CSI_Result) -> list:
    timestamps = np.array([status.tstamp for status in data.status])
    intervals = np.diff(timestamps).tolist()
    return intervals
