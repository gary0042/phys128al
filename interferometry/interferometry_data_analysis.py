"""
interferometry_data_analysis.py
Contains code to analyze data for interferometry
"""

import numpy as np 
import pandas as pd
import os


# raw data as data frame
data = {
    'Trial': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'Video': ['IMG_1949', 'IMG_1951', 'IMG_1952', 'IMG_1953', 'IMG_1954', 
              'IMG_1955', 'IMG_1956', 'IMG_1957', 'IMG_1958', 'IMG_1960', 
              'IMG_1961', 'IMG_1962'],
    'David Count': [75, 75.5, 79, 79, 79.5, 78, 80.5, 79.5, 79, 79, 75, 78],
    'Gary Count': [70, 72, 81, 80, 81, 78, 79, 79, 80, 81, 71, 72],
    'Average count for each video': [72.5, 73.75, 80, 79.5, 80.25, 78, 79.75, 79.25, 79.5, 80, 73, 75],
    'Wavelength (nm)': [689.6551724, 677.9661017, 625, 628.9308176, 623.0529595,
                        641.025641, 626.9592476, 630.9148265, 628.9308176, 625,
                        684.9315068, 666.6666667]
}
df = pd.DataFrame(data)

# calculate the uncertainties in the average count
df["avg count uncertainty"] = df.apply(
    lambda row: np.std([row["David Count"], row["Gary Count"]]),
    axis=1
)

# calculate the uncertainties in the wavelength
def wave_uncert(row):
    delta_dm = 1/np.sqrt(12)
    delta_m = row["avg count uncertainty"]
    return np.sqrt((2/row["Average count for each video"])**2 * delta_dm**2 
                   + (2*25/row["Average count for each video"]**2)**2 * delta_m**2)*1000
df["wavelength uncertainty"] = df.apply(
    lambda row: wave_uncert(row),
    axis=1
)


# print(f"uncertainty: {np.std(df["Wavelength (nm)"])}")
# print(f"propagated uncertainty: {np.sqrt(np.sum(df["wavelength uncertainty"]**2))/10}")
# print(f"Average wavelength (nm): {np.average(df["Wavelength (nm)"])}")
# print(df)

# this is the raw data from Fabry-Perot
data = {
    'Trial': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Fringe count': [40, 40, 40, 40, 40, 40, 40, 40, 40, 40],
    'd_m': [16, 17, 16.5, 16, 16, 17, 16.5, 14.5, 14, 15],
    'Wavelength (nm)': [800, 850, 825, 800, 800, 850, 825, 725, 700, 750]
}

df = pd.DataFrame(data)

df['wavelength uncertainty'] = df.apply(
    lambda row: 1000*2/(40*np.sqrt(12)),
    axis=1
)
print(f"uncertainty: {np.std(df["Wavelength (nm)"])}")
print(f"propagated uncertainty: {np.sqrt(np.sum(df["wavelength uncertainty"]**2))/10}")
print(f"Average wavelength (nm): {np.average(df["Wavelength (nm)"])}")
print(df)