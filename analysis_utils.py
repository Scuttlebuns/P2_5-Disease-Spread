"""
This module is to be used in the python terminal for data processing each test case.
In order to use them execute the following commands:

# Import the class
from analysis_utils import *

# Load all runs and pad data to match max time_steps
runs = load_and_pad_runs("data/{dir name}")

# Print the stats
print("Avg Duration:", avg_duration("data/{dir name}"))
print("Peak Infected:", peak_infected(runs))
print("Avg Peak Infected:", avg_peak_infected(runs))
print("Peak Dead:", peak_dead(runs))
print("Avg Peak Dead:", avg_peak_dead(runs))

"""
import os
import pandas as pd

def load_and_pad_runs(folder_path):
    """
    Loads all CSV run files from the specified folder and pads them to the length of the longest run
    by repeating the last known values for each attribute.
    
    Returns a list of padded DataFrames.
    """
    runs = []
    max_len = 0

    # Load each run
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            path = os.path.join(folder_path, file)
            df = pd.read_csv(path)
            runs.append(df)
            max_len = max(max_len, len(df))

    # Pad each run to match max_len
    padded_runs = []
    for df in runs:
        if len(df) < max_len:
            last_row = df.iloc[-1]
            pad_rows = pd.DataFrame([last_row] * (max_len - len(df)))
            padded_df = pd.concat([df, pad_rows], ignore_index=True)
        else:
            padded_df = df
        padded_runs.append(padded_df)

    return padded_runs

def avg_duration(folder_path):
    # Returns the average number of time steps for unpadded runs.
    lengths = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            path = os.path.join(folder_path, file)
            df = pd.read_csv(path)
            lengths.append(len(df))
    return sum(lengths) / len(lengths) if lengths else 0

def peak_infected(runs):
    # Returns the maximum infected percentage from all runs.
    return max(df['infected'].max() for df in runs)

def avg_peak_infected(runs):
    # Returns the average of peak infected percentages from all runs.
    peaks = [df['infected'].max() for df in runs]
    return sum(peaks) / len(peaks) if peaks else 0

def peak_dead(runs):
    # Returns the maximum dead percentage from all runs.
    return max(df['dead'].max() for df in runs)

def avg_peak_dead(runs):
    # Returns the average of peak dead percentages from all runs.
    peaks = [df['dead'].max() for df in runs]
    return sum(peaks) / len(peaks) if peaks else 0
