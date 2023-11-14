from pcmdi_metrics.graphics import portrait_plot
import matplotlib.pyplot as plt
import json
import numpy as np


#peak = np.loadtxt('data/output_peak_reanalysis.txt')
#angle = peak.reshape(3,-1)

#peak = np.loadtxt('data/output_diff.txt')
#angle = peak.reshape(5,6)

peak = np.loadtxt('data/output_diff_all_region.txt')
angle = peak.reshape(5,-1)

#[[  -5.   11. -156.   -2.  -16.  -77.]
#ref_peak = np.array([5,75,-10,-105,141,154]) ##!!!  these numbers are wrong !!!!
#ref_peak = np.array([5,75,-40,-102,166,151])
#ref_peak = np.atleast_2d(ref_peak)
#ref_peak = np.repeat(ref_peak,repeats=5, axis=0)

#print(angle)

#angle = np.where(angle < -182, angle+365, angle)
#angle = np.where(angle >  182, angle-365, angle)



model_names = ["cmip5_CanESM2","cmip5_CCSM4","cmip5_CSIRO-Mk3-6-0","cmip5_NorESM1-M","cmip6_MRI-ESM2-0"]
#model_names = ['ERA5','MERRA2','JRA55C']
region_names = ['California','SAmerica', 'Africa','NEurope','Australia','SAfrica']
region_names = region_names + ['Baja','PAC NW','New Zealand','Alaska']


maxvalue = np.max(angle)
minvalue = np.min(angle)
maxvalue = max(maxvalue, minvalue*-1)
#maxvalue *= 1.2
maxvalue *= 0.7
minvalue = maxvalue*-1

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
              #vrange = (minvalue, maxvalue), 
              vrange = (-180,180), 
              box_as_square=True,
              logo_off = True)

ax.set_title( 'landfalling AR seasonality', fontsize=20, color="black")

plt.tight_layout()
#plt.savefig('AR_character_'+region+'.png')
plt.show()

