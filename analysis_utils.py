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
import matplotlib.pyplot as plt
import numpy as np

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

def plot_avg_infection_over_time(run_10, run_25, run_40, run_100, label='infected', scenario='Slow Spread'):
    """
    Generates a line graph showing average infection per timestep
    for different compliance levels in a single scenario.

    Parameters:
        run_10, run_25, run_40, run_100: List of padded pandas DataFrames
        label: str - one of 'infected', 'susceptible', 'recovered', etc.
        scenario: str - name of the scenario (used in title)
    """

    def compute_mean(df_list):
        return pd.concat(df_list).groupby(level=0).mean()[label]

    # Compute means
    avg_10 = compute_mean(run_10)
    avg_25 = compute_mean(run_25)
    avg_40 = compute_mean(run_40)
    avg_100 = compute_mean(run_100)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(avg_10.index, avg_10.values, label='10% Non-Compliance', color='#4daf4a')
    plt.plot(avg_25.index, avg_25.values, label='25% Non-Compliance', color='#377eb8')
    plt.plot(avg_40.index, avg_40.values, label='40% Non-Compliance', color='#ff7f00')
    plt.plot(avg_100.index, avg_100.values, label='100% Non-Compliance', color='#e41a1c')

    plt.xlabel('Time Step')
    plt.ylabel(f'Average {label.capitalize()} Count')
    plt.title(f'{scenario} — Average {label.capitalize()} Over Time')
    plt.legend(title='Distancing Compliance')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

import matplotlib.pyplot as plt
import pandas as pd

def plot_scenario_comparison_by_compliance(slow_runs, balanced_runs, rapid_runs,
                                            label='infected', compliance_label='25% Non-Compliance'):
    """
    Plots average percentage of a given status (infected, recovered, etc.)
    over time for the three scenarios at a specific compliance level.

    Parameters:
        slow_runs, balanced_runs, rapid_runs: List of padded DataFrames for each scenario
        label: str – column to visualize ('infected', etc.)
        compliance_label: str – used for plot title and legend
    """
    def compute_percent(df_list, total_pop):
        avg = pd.concat(df_list).groupby(level=0).mean()[label]
        return (avg / total_pop) * 100

    # Known total populations
    pop_slow = 1000
    pop_balanced = 1500
    pop_rapid = 2000

    # Get percentage over time for each scenario
    pct_slow = compute_percent(slow_runs, pop_slow)
    pct_balanced = compute_percent(balanced_runs, pop_balanced)
    pct_rapid = compute_percent(rapid_runs, pop_rapid)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(pct_slow.index, pct_slow.values, label='Slow Spread', color='#4daf4a')
    plt.plot(pct_balanced.index, pct_balanced.values, label='Balanced Spread', color='#377eb8')
    plt.plot(pct_rapid.index, pct_rapid.values, label='Rapid Spread', color='#e41a1c')

    plt.xlabel('Time Step')
    plt.ylabel(f'Average % {label.capitalize()}')
    plt.title(f'{label.capitalize()} Over Time — {compliance_label}')
    plt.legend(title='Scenario')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
