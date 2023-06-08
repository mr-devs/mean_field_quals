"""
Purpose:
    Generate the figure that shows the effect of lambda.

Inputs:
    None

Outputs:
    - figures_generation/mf_lambda_effect.pdf

Author:
    Matthew R. DeVerna
"""
import os

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd


OUT_DIR = "../figures"
CURR_DIR = "figures_generation"
RESULTS_DIR = "../sim_results/effects_of_lambda"
# Ensure we are in the data_analysis directory for paths to work
if os.path.basename(os.getcwd()) != CURR_DIR:
    raise Exception(f"Must run this script from the `{CURR_DIR}` directory!")

### Load simulation results ###
totals_df = pd.read_csv(os.path.join(RESULTS_DIR, "total_infected.csv"))
by_day_df = pd.read_csv(os.path.join(RESULTS_DIR, "daily_infected.csv"))


less_combined = by_day_df[
    (by_day_df.group == "combined") & (by_day_df["lambda"].isin([1, 2, 3, 4]))
].copy()
less_mis = by_day_df[
    (by_day_df.group == "misinformed") & (by_day_df["lambda"].isin([1, 2, 3, 4]))
].copy()
less_ord = by_day_df[
    (by_day_df.group == "combined") & (by_day_df["lambda"].isin([1, 2, 3, 4]))
].copy()

# Set the font size for all text
plt.rcParams.update({"font.size": 12})

# Create color map based on Tableu10 found here: https://vega.github.io/vega/docs/schemes/
color_map = {1: "#4c78a8", 2: "#f58518", 3: "#e45756", 4: "#72b7b2"}

# Create the figure and grid layout
fig = plt.figure(figsize=(10, 6))
grid = gridspec.GridSpec(3, 2, width_ratios=[2, 1])

# Create subplots for the first column
ax1 = plt.subplot(grid[0, 0])
ax2 = plt.subplot(grid[1, 0])
ax3 = plt.subplot(grid[2, 0])

## Combined figure
for mult in less_combined["lambda"].unique():
    temp_df = less_combined[less_combined["lambda"] == mult]
    ax1.plot(temp_df["day"], temp_df["value"], color=color_map[mult], label=int(mult))

## Misinformed figure
for mult in less_mis["lambda"].unique():
    temp_df = less_mis[less_mis["lambda"] == mult]
    ax2.plot(temp_df["day"], temp_df["value"], color=color_map[mult], label=int(mult))

## Ordinary figure
for mult in less_ord["lambda"].unique():
    temp_df = less_ord[less_ord["lambda"] == mult]
    ax3.plot(temp_df["day"], temp_df["value"], color=color_map[mult], label=int(mult))


# Set the y-axis limits for the first column
ax1.set_ylim(0, 0.4)
ax2.set_ylim(0, 0.4)
ax3.set_ylim(0, 0.4)

# Share y-axis limits for the first column
ax2.sharey(ax1)
ax3.sharey(ax1)

# Add gridlines to all subplots
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

# Remove spines
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

# Remove x-axis ticks
ax1.xaxis.set_ticklabels([])
ax2.xaxis.set_ticklabels([])

### Create right panel

# Create subplot for the second column spanning all three rows
ax4 = plt.subplot(grid[:, 1])

# Plot extra infections
ax4.plot(
    totals_df["lambda"],
    totals_df["total_extra"],
    color="black",
)

# Move the y-axis of the right spanning plot to the right side
ax4.yaxis.tick_right()
ax4.yaxis.set_label_position("right")

# # Set the y-axis limits for the second column
# ax4.set_ylim(0, 1)

# Add gridlines to the subplot in the second column
ax4.grid(True)

# Remove spines
ax4.spines["left"].set_visible(False)
ax4.spines["top"].set_visible(False)

# Set labels for each subplot
ax1.set_ylabel("all")
ax2.set_ylabel("proportion infected\n\nmisinformed")
ax3.set_ylabel("ordinary")
ax3.set_xlabel("day")
ax4.set_ylabel(
    "proportion of extra infections with two subpopulations", rotation=-90, va="bottom"
)
ax4.set_xlabel("$\lambda$")


# Add a legend above the top left panel
ax1.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, 1),
    ncol=4,
    frameon=False,
    title="$\lambda$",
)

plt.tight_layout()

# Save the plot
plt.savefig(os.path.join(OUT_DIR, "mf_lambda_effect.pdf"), dpi=800)
plt.savefig(os.path.join(OUT_DIR, "mf_lambda_effect.png"), dpi=800, transparent=True)
