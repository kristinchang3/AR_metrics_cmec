# - Generate a static portrait plot with two different color palettes
# - Author: Kristin Chang (Feb. 2024)
# - Last Updated: Feb. 2024

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.transforms

# Load dataset
peak = np.loadtxt('data/output_diff_all_region.txt')

# Reshape data and select target results
angle = peak.reshape(5,-1)
angle = np.where(angle < -182, angle+365, angle)
angle = np.where(angle >  182, angle-365, angle)
print(angle)

# Define models and regions
models = ["cmip5_CanESM2","cmip5_CCSM4","cmip5_CSIRO-Mk3-6-0","cmip5_NorESM1-M","cmip6_MRI-ESM2-0"]
regions = ['California','SAmerica', 'Africa','NEurope','Australia','SAfrica']
regions = regions + ['Baja','PAC NW','New Zealand','Alaska']

# Create custom color palette
custom_cmap = colors.ListedColormap(['white','white'])

# Initialize plot figure and axes
fig, ax = plt.subplots(figsize=(6, 8))

# Plot reference and model data on separate heatmaps using pcolormesh()
plt.pcolormesh(models[0], regions, angle.T[:,0:1], cmap=custom_cmap, vmin=-180, vmax=180)
plt.pcolormesh(models[1:], regions, angle.T[:,1:], cmap='twilight_shifted_r', vmin=-180, vmax=180)

ax.set_xticks(np.arange(len(models)),labels=models, minor=False) # set xaxis labels
ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False) # move xaxis labels to the top
plt.setp(ax.get_xticklabels(),rotation=30,ha="left",rotation_mode="anchor") # angle and orient xaxis labels
ax.set_yticks(np.arange(len(regions)), labels=regions) # set yaxis labels

ax.set_xticks(np.arange(-.5, 5, 1), minor=True) # create minoir ticks
ax.set_yticks(np.arange(-.5, 10, 1), minor=True)
ax.grid(which='minor',color='black', linewidth=0.5) # create grid lines based off of minor ticks
ax.tick_params(which='minor', bottom=False, left=False) # remove minor ticks

# add hatch pattern where data falls within certain range
patterns = ['', 'oo', '///', 'XXXXX']
pattern = patterns[2]
hatch_above = -5
hatch_below = 5

hatch = ax.pcolor((np.arange(angle.T[:,1:].shape[1])),
          (np.arange(angle.T[:,1:].shape[0])),
          np.where((angle.T[:,1:] >= hatch_above) & (angle.T[:,1:]< hatch_below), angle.T[:,1:], np.nan),
          alpha=0,
          hatch=pattern,
          ec='none',
          lw=1
          )
# define a transform to set overlay at correct data coords
x_shift = 1
y_shift = 0
trans = matplotlib.transforms.Affine2D().translate(x_shift, y_shift)
hatch.set_transform(trans + hatch.get_transform())

# Loop over data dimensions and create text annotations.
text_color_above = 100
text_color_below = -100
for i in range(len(regions)):
    for j in range(len(models)):
        if j>0 and angle.T[i,j] > text_color_above:
            text = ax.text(j, i, angle.T[i, j],
                        ha="center", va="center", color="w")
        elif j>0 and angle.T[i,j] < text_color_below:
            text = ax.text(j, i, angle.T[i, j],
                        ha="center", va="center", color="w")
        else:
            text = ax.text(j, i, angle.T[i, j],
                        ha="center", va="center", color="black")
            
# add plot elements
ax.set_aspect(1) # set square cells
plt.colorbar().set_label('peak day', rotation=270, labelpad=10)
#ax.set_title('AR Peak Day Difference', pad=30)
ax.set_xlabel('Model')
ax.xaxis.set_label_position('top')
ax.set_ylabel('Region')

fig.tight_layout()
plt.show()

# save figure
#fig.savefig('../charts/static_portrait_plot.png')