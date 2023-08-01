"""
Purpose:
    Generate the figure that shows the effect of homophily on the misinformed group.

Inputs:
    None

Outputs:
    - figures_generation/mf_homophiliy_misinformed_effect.pdf

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
CURR_DIR = "figures_generation"
RESULTS_DIR = "../sim_results/effects_of_homophily_on_misinformed"
# Ensure we are in the data_analysis directory for paths to work
if os.path.basename(os.getcwd()) != CURR_DIR:
    raise Exception(f"Must run this script from the `{CURR_DIR}` directory!")

# Load simulation source code
source_dir = "../src"
sys.path.insert(0, source_dir)

### Load simulation results ###
total_infected_df = pd.read_csv(os.path.join(RESULTS_DIR, "total_infected.csv"))

total_infected_df = total_infected_df.rename(
    columns={
        "total_ord_inf": "ordinary",
        "total_mis_inf": "misinformed",
        "total": "all",
    }
)

# Set the font size for all text
plt.rcParams.update({"font.size": 12})

group_color_map = {
    "misinformed": "#FF0060",  # red
    "ordinary": "#0079FF",  # blue
    "all": "#9376E0",  # purple
}

source = total_infected_df[(total_infected_df["beta"] < 0.27)]

betas = source["beta"].unique()
alphas = source["alpha"].unique()

rows = len(alphas)
cols = len(betas)

fig, ax = plt.subplots(ncols=cols, figsize=(12, 5), sharey=True)

for col, beta in enumerate(betas):
    temp_df = source[(source["beta"] == beta)]

    ax[col].plot(
        temp_df["alpha"], temp_df["all"], label="all", color=group_color_map["all"]
    )
    ax[col].plot(
        temp_df["alpha"],
        temp_df["misinformed"],
        label="misinformed",
        color=group_color_map["misinformed"],
    )
    ax[col].plot(
        temp_df["alpha"],
        temp_df["ordinary"],
        label="ordinary",
        color=group_color_map["ordinary"],
    )
    ax[col].set_xlabel(r"$\alpha$")

    ax[col].set_title(r"$\beta_{S}$ = " + f"{np.round(beta,2)}")

    ax[col].grid()
    ax[col].spines["top"].set_visible(False)
    ax[col].spines["right"].set_visible(False)


ax[0].set_ylabel("Proportion of the population infected")
ax[0].legend()
plt.tight_layout()

# Save the plot
plt.savefig(os.path.join(OUT_DIR, "mf_homophiliy_misinformed_effect.pdf"), dpi=800)
plt.savefig(
    os.path.join(OUT_DIR, "mf_homophiliy_misinformed_effect.png"),
    dpi=800,
    transparent=True,
)
