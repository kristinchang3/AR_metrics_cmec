from pcmdi_metrics.graphics import portrait_plot
import matplotlib.pyplot as plt
import json
import numpy as np


#peak = np.loadtxt('data/output_diff.txt')
#angle = peak.reshape(5,6)
#
##[[  -5.   11. -156.   -2.  -16.  -77.]
#ref_peak = np.array([5,75,-10,-105,141,154])
#ref_peak = np.atleast_2d(ref_peak)
#ref_peak = np.repeat(ref_peak,repeats=5, axis=0)
#
#ref_peak = np.where(ref_peak < 0, 365+ref_peak, ref_peak)
#angle = np.where(angle < 0, 365+angle, angle)
#
#print(angle)
#print(ref_peak)
#angle = angle - ref_peak
#print(angle)
#print(np.max(angle))
#print(np.min(angle))

peak = np.loadtxt('data/output_peak_reanalysis.txt')
angle = peak.reshape(3,-1)

angle = np.where(angle < -182, angle+365, angle)
angle = np.where(angle >  182, angle-365, angle)



#model_names = ["cmip5_CanESM2","cmip5_CCSM4","cmip5_CSIRO-Mk3-6-0","cmip5_NorESM1-M","cmip6_MRI-ESM2-0"]
model_names = ['ERA5','MERRA2','JRA55C']
region_names = ['California','SAmerica', 'Africa','NEurope','Australia','SAfrica']
region_names = region_names + ['Baja','PAC NW','New Zealand','Alaska'] + ['UK','WEurope']

maxvalue = np.max(angle)
minvalue = np.min(angle)
maxvalue = max(maxvalue, minvalue*-1)
#maxvalue *= 1.2
maxvalue *= 0.7
minvalue = maxvalue*-1

# Use number of models and regions to determine cell size
num_models = len(model_names)
num_regions = len(region_names)

cell_width = 1/num_models
cell_height = 1/num_regions

# set desired figure size
desired_width = 2000
desired_height = 2000

# calculate final width and height based on above parameters
adjusted_width = round(int(cell_width * desired_width), -1)
adjusted_height = round(int(cell_height * desired_height), -1)

fig, ax, cbar = \
portrait_plot(angle.T,
#              xaxis_labels=region_names,
#              yaxis_labels=model_names,
              yaxis_labels=region_names,
              xaxis_labels=model_names,
              annotate=True,
#              annotate_data = parr, 
#              cbar_label='peak day mean bias',
              cbar_label='peak day',
#              width = adjusted_width,
#              height = adjusted_height,
              #vrange = (minvalue, maxvalue), 
              vrange = (-180,180), 
              box_as_square=True,
              logo_off = True)

ax.set_title( 'landfalling AR seasonality', fontsize=20, color="black")

plt.tight_layout()
#plt.savefig('AR_character_'+region+'.png')
plt.show()

