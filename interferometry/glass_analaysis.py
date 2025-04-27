"""
glass_analysis.py
Contains code to analyze experiment III
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

data = {
    'Trial': ['1 IMG 2057', '2 IMG 2058', '3 IMG 2059', '4 IMG 2060', '5 IMG 2061'],
    'Initial angle': [0.8, 0.8, 0.8, 0.8, 0.8],
    'Final angle': [17.0, 18.0, 17.0, 17.0, 17.0],
    'Number of fringes': [262, 296, 263, 263, 260]
}

df = pd.DataFrame(data)

# add column delta theta = theta_f - theta_i
df["delta theta"] = df.apply(
    lambda row: row["Final angle"] - row["Initial angle"],
    axis=1
)

# add delta theta in radians
df["delta theta (rad)"] = df.apply(
    lambda row: row["delta theta"]*np.pi/180,
    axis=1
)

resolution_lim = (0.2/np.sqrt(12))*(np.pi/180)

# calculate n_g 
def n_g(row):
    N = row["Number of fringes"]
    lambda_0 = 632.8
    theta = row["delta theta (rad)"]
    t = 5.0e6
    numerator = (2*t - N*lambda_0) * (1 - np.cos(theta))
    denominator = 2*t*(1 - np.cos(theta)) - N*lambda_0
    return numerator/denominator
df["n_g"] = df.apply(
    lambda row: n_g(row),
    axis=1
)


# calculate delta n_g
def n_g_uncert(row):
    N = row["Number of fringes"]
    delta_theta = resolution_lim
    lambda_0 = 632.8
    theta = row["delta theta"]
    t = 5.0e6
    numerator = N * lambda_0 * (N * lambda_0 - 2 * t) * np.sin(theta)
    denominator = (2 * t * np.cos(theta) + N * lambda_0 - 2 * t)**2
    return (numerator / denominator) * delta_theta
df["n_g uncert"] = df.apply(
    lambda row: n_g_uncert(row),
    axis=1
)

# take the subset n_g and n_g uncert
subset = df[["n_g", "n_g uncert"]]

# print out the latex format
latex_code = subset.to_latex(
    index=False,               # Remove auto-index
    caption=r"Calculated index of refraction for each trial.",  # Add caption
    label="tab:index_refraction",     # Reference label
    position="h",              # Table positioning
    column_format="c|c",       # Alignment: left, right, right
    escape=False,              # Allow LaTeX special chars
    float_format="%.10f"        # Number formatting
)

# print statements
print(df)
print(subset)
print(latex_code)
print(f"Average n_g: {np.average(df["n_g"])}")
print(f"Standard deviation of n_g: {np.std(df["n_g"])}")


