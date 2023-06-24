"""
Purpose:
    Generate the figure that shows the effect of beta (no misinformed population).

Inputs:
    None

Outputs:
    - figures_generation/mf_beta_effect.pdf
    - figures_generation/mf_beta_effect.png

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
RESULTS_DIR = "../sim_results/effects_of_beta"
# Ensure we are in the data_analysis directory for paths to work
if os.path.basename(os.getcwd()) != CURR_DIR:
    raise Exception(f"Must run this script from the `{CURR_DIR}` directory!")

### Load simulation results ###
tot_df = pd.read_csv(os.path.join(RESULTS_DIR, "cum_infections.csv"))
daily_infection_df = pd.read_csv(os.path.join(RESULTS_DIR, "daily_infections.csv"))
r0_df = pd.read_csv(os.path.join(RESULTS_DIR, "r0s.csv"))

### Set up some stuff for the figure ###

# Set the font size for all text
plt.rcParams.update({"font.size": 12})

# Create color map based on Tableu10 found here: https://vega.github.io/vega/docs/schemes/
# The "purple" was manually added :)
color_map = {0.2: "#4c78a8", 0.4: "#f58518", 0.6: "#e45756", 0.8: "#72b7b2", 1.0: "purple"}

# Generate the figure #
# ------------------- #
# Create the figure and grid layout
fig = plt.figure(figsize=(10, 6))
grid = gridspec.GridSpec(2, 2, width_ratios=[1.5, 1])

# Create subplots for the first column
ax1 = plt.subplot(grid[:, 0])
ax2 = plt.subplot(grid[0, 1])
ax3 = plt.subplot(grid[1, 1])

# Less beta values highlighted for one of the plots
less_betas = [0.2, 0.4, 0.6, 0.8, 1. ]
for beta in less_betas:
    selected_df = daily_infection_df[daily_infection_df['beta']==beta]
    
    ax1.plot(
        selected_df['day'],
        selected_df['prop_infected'],
        color = color_map[beta],
        label = beta
    )
    
ax1.spines["right"].set_visible(False)
ax1.spines["top"].set_visible(False)

ax1.grid()

ax1.set_xlim((0,100))
ax1.set_ylim((0,.6))

ax1.set_ylabel("proportion of population infected")
ax1.set_xlabel("day")


ax2.plot(
    r0_df['beta'],
    r0_df['r0'],
    color='black',
    linewidth=1,
)
ax2.scatter(
    r0_df['beta'],
    r0_df['r0'],
    color='black',
    s=5,
)

r0_is_one = r0_df[np.isclose(r0_df['r0'], 1)]
x = r0_is_one.beta.unique().item()
y = r0_is_one.r0.unique().item()
ax2.plot(
    [x,x],
    [0,y+1],
    color='red',
    linewidth=1
)
ax2.annotate(
    r"$R_{0} = 1$ ($\beta = 0.2$)",
    (x,y+1.1),
    va='bottom',
    ha='center',
    fontsize=10
)

ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")

ax2.spines["left"].set_visible(False)
ax2.spines["top"].set_visible(False)

ax2.set_xlim((0,1))
ax2.set_ylim((0,5))

ax2.grid()

ax2.xaxis.set_ticklabels([])
ax2.xaxis.set_tick_params(length=0)

ax2.set_ylabel(r"$R_{0}$", rotation=270, va='bottom')

ax3.plot(
    tot_df['beta'],
    tot_df['total_infected'],
    color='black'
)
ax3.scatter(
    tot_df['beta'],
    tot_df['total_infected'],
    color='black',
    s=5,
)

ax3.plot(
    [x,x],
    [0,1],
    color='red',
    linewidth=1
)

ax3.grid()

ax3.set_xlabel(r"$\beta$")


ax3.yaxis.tick_right()
ax3.yaxis.set_label_position("right")

ax3.spines["left"].set_visible(False)
ax3.spines["top"].set_visible(False)

ax3.set_xlim((0,1))
ax3.set_ylim((0,1))


ax3.set_ylabel("proportion of\npopulation infected", rotation=270, va='bottom')


# Add a legend above the top left panel
ax1.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, 1),
    ncol=5,
    frameon=False,
    title=r"$\beta$",
)

plt.tight_layout()

ax1.annotate(
    "(a)",
    xy=(-0.13, .975),
    xycoords=ax1.transAxes,
    fontsize=14,
    ha="center",
    va="center",
)
ax2.annotate(
    "(b)",
    xy=(-0.07, .95),
    xycoords=ax2.transAxes,
    fontsize=14,
    ha="center",
    va="center",
)
ax3.annotate(
    "(c)",
    xy=(-0.07, .95),
    xycoords=ax3.transAxes,
    fontsize=14,
    ha="center",
    va="center",
)

# Save the plot
plt.savefig(os.path.join(OUT_DIR, "mf_beta_effect.pdf"), dpi=800)
plt.savefig(os.path.join(OUT_DIR, "mf_beta_effect.png"), dpi=800, transparent=True)