"""
Purpose:
    Print statistics presented in the paper.

Inputs:
    None

Outputs:
    None. Outputs are printed. To record the output, run the following:
        python print_stats.py >> output_file.txt

Author:
    Matthew R. DeVerna
"""
import os
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT_DIR = "../figures"
CURR_DIR = "stats_scripts"
RESULTS_DIR = "../sim_results/effects_of_lambda"
# Ensure we are in the data_analysis directory for paths to work
if os.path.basename(os.getcwd()) != CURR_DIR:
    raise Exception(f"Must run this script from the `{CURR_DIR}` directory!")

# Load simulation source code
source_dir = "../src"
sys.path.insert(0, source_dir)
from simulations import get_peak_day

print("-" * 75)
print("Statistics utilized in the paper")
print("-" * 75)
print("\n")

### Load simulation results ###
totals_df = pd.read_csv(os.path.join(RESULTS_DIR, "total_infected.csv"))
by_day_df = pd.read_csv(os.path.join(RESULTS_DIR, "daily_infected.csv"))

print("VARYING LAMBDA")
print("-" * 50)
print(
    f"Total extra infections incurred by misinformed group (vs. ordinary): {totals_df['diff'].max() : .1%}"
)
print(
    f"Total extra infections incurred by network (lambda 1 vs lambda 4): {totals_df['total_extra'].max() : .1%}"
)
for group in ["misinformed", "ordinary"]:
    temp_slice = by_day_df[(by_day_df["lambda"] == 4) & (by_day_df["group"] == group)]
    peak_day = get_peak_day(temp_slice["value"])
    print(f"Peak day for {group} group: {peak_day}")

# 'combined' here means "the entire network"
combined_by_day = by_day_df[by_day_df["group"] == "combined"].reset_index(drop=True)
lambda4 = combined_by_day[combined_by_day["lambda"] == 4]
lambda1 = combined_by_day[combined_by_day["lambda"] == 1]

lambda4_peak_day = get_peak_day(lambda4["value"])
lambda1_peak_day = get_peak_day(lambda1["value"])

print(f"Network peak, lambda = 4: {lambda4_peak_day} days")
print(f"Network peak, lambda = 1: {lambda1_peak_day} days")
print(f"Network peak, difference: {lambda1_peak_day - lambda4_peak_day} days")
