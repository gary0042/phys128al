"""
air_pressure_analysis.py
Contains code to analyze experiment II.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# air pressure data as a data frame
data = {
    'Trial #': ['1 IMG 2049', '2 IMG 2050', '3 IMG 2051', '4 IMG 2052', '5 IMG 2053'],
    'Count': [14, 18, 17, 16, 16],
    'Initial Pressure (kPa)': [-80, -84, -84, -82, -86],
    'Final Pressure (kPa)': [-12, -10, -8, -10, -8]
}

df = pd.DataFrame(data)

# add column which is the change in pressure
df["delta pressure"] = df.apply(
    lambda row: -row["Initial Pressure (kPa)"] + row["Final Pressure (kPa)"],
    axis=1
)

# add column which is the uncertainty
df["delta pressure uncert"] = df.apply(
    lambda row: np.sqrt(2)*(2/np.sqrt(12)),
    axis=1
)

# add column of slopes
def calc_slope(row):
    d = 3*10**7 
    lamb = 632.8 
    N = row["Count"]
    return N*lamb/(2*d*row["delta pressure"])

df["slopes"] = df.apply(
    lambda row: calc_slope(row),
    axis=1
)

# add slope uncertainty
def calc_slope_uncer(row):
    d = 3*10**7 
    lamb = 632.8 
    N = row["Count"]
    p_uncert = row["delta pressure uncert"]
    p = row["delta pressure"] 
    return N*lamb*p_uncert/(2*d*p**2)
df["slopes uncert"] = df.apply(
    lambda row: calc_slope_uncer(row),
    axis=1
)

print(df)

# extract the slope information

subset = df[["slopes", "slopes uncert"]]

# convert to latex code
latex_code = subset.to_latex(
    index=False,               # Remove auto-index
    caption=r"Calculated slopes in (1/\si{kpa})",  # Add caption
    label="tab:slopes",     # Reference label
    position="h",              # Table positioning
    column_format="lrr",       # Alignment: left, right, right
    escape=False,              # Allow LaTeX special chars
    float_format="%.10f"        # Number formatting
)
#print(latex_code)

print(f"Avg slope {np.average(df["slopes"])}")
print(f"Slope statistical uncertainty {np.std(df["slopes"])}")
print(f"Slope systematic uncertainty {np.sqrt(np.sum(df["slopes uncert"]**2))/5}")

# plotting the slope
# Define the equation and parameters
n0 = 1.0
slope = 2.32e-6
slope_uncertainty = 0.15e-6

# Pressure range (adjust as needed)
p = np.linspace(-100e3, 100e3, 500)  # -100 kPa to +100 kPa

# Calculate n(p) and uncertainty bounds
n_p = n0 + slope * p
upper_bound = n0 + (slope + slope_uncertainty) * p
lower_bound = n0 + (slope - slope_uncertainty) * p

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(p, n_p, label=r'$n(p) = 1 + 2.32 \times 10^{-6} p$', color='blue', linewidth=2)
plt.fill_between(p, lower_bound, upper_bound, color='blue', alpha=0.2, 
                 label=f'Slope uncertainty: $\pm 0.15 \\times 10^{-6}$')
plt.xlim(0, 120)
plt.ylim(1-1e-3, 1+1e-3)

# Formatting
plt.xlabel('Pressure $p$ (kPa)', fontsize=12)
plt.ylabel('Refractive index $n(p)$', fontsize=12)
plt.title('Refractive Index vs. Pressure with Uncertainty', fontsize=14)
plt.axhline(y=1, color='gray', linestyle='--', linewidth=0.5)  # Reference line at n=1
plt.grid(True, linestyle=':', alpha=0.5)
plt.legend(fontsize=10)
plt.tight_layout()


# Save or display
plt.savefig('refractive_index_vs_pressure.png', dpi=300)
plt.show()