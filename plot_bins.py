import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys, utils

# Read from CSV.
df = utils.read_csv('{}.csv'.format(sys.argv[1]))

# List of relevant features.
wind_features = ['WTP_AW_angle', 'WTP_AW_speed']

# Combine positive and negative wind angle.
df[wind_features[0]] = df[wind_features[0]].apply(lambda x: abs(x))

# Plot the bins.
fig = plt.figure()
ax = fig.gca()
ax.set_xticks(np.arange(0, 181, 10))
ax.set_yticks(np.arange(0, 53, 2))
plt.plot(df[wind_features[0]].tolist(), df[wind_features[1]].tolist(), 'ko', markersize=0.25)
plt.grid()
plt.show()
