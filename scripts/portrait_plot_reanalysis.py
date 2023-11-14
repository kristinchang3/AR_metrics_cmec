import numpy as np
import pandas as pd
import json
import panel as pn
from matplotlib import pyplot as plt
import holoviews as hv
import hvplot.pandas
from PIL import Image
import os, os.path
from bokeh.models import HoverTool

#angle = np.array([[  0,  86, 199],
#       [ 23, 111, 271],
#       [ 16,  97, 226],
#       [ 17, 103, 159]])

#peak = np.loadtxt('data/output_diff.txt')
peak = np.loadtxt('data/output_peak_reanalysis.txt')
angle = peak.reshape(3,-1)

#if angle < -182:
#    angle += 365
#elif angle > 182:
#    angle -= 365


angle = np.where(angle < -182, angle+365, angle)
angle = np.where(angle >  182, angle-365, angle)

print(angle)

#model_names = ["CanESM2","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0"]
#region_names = ['California','S.America', 'W.Africa']
#model_names = ["cmip5_CanESM2","cmip5_CCSM4","cmip5_CSIRO-Mk3-6-0","cmip5_NorESM1-M","cmip6_MRI-ESM2-0"]
model_names = ['ERA5','MERRA2','JRA55C']
region_names = ['California','SAmerica', 'Africa','NEurope','Australia','SAfrica']

da = pd.DataFrame(data=angle, index=model_names, columns=region_names)

dd = da.stack()
dd = dd.reset_index()
dd = dd.rename(columns={"level_0": "model", "level_1": "region", 0 :"peak"})
ddd = dd['peak'].values

#print(dd)

img_path = 'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/'
img_links = []

for i, model in enumerate(model_names):
    for j, region in enumerate(region_names):
        filename = img_path+'fig_re_'+str(i)+"_"+str(j)+'.png'
        img_links.append(filename)

#print(img_links)

#img_links = ['https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CanESM2_California_2_0.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CanESM2_SAmerica_2_1.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CanESM2_Africa_2_2.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CSIRO-Mk3-6-0_California_2_0.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CSIRO-Mk3-6-0_SAmerica_2_1.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CSIRO-Mk3-6-0_Africa_2_2.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/NorESM1-M_California_2_0.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/NorESM1-M_SAmerica_2_1.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/NorESM1-M_Africa_2_2.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MRI-ESM2-0_California_2_0.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MRI-ESM2-0_SAmerica_2_1.png',
#             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MRI-ESM2-0_Africa_2_2.png'
#             ]

dd['img'] = img_links

#print(dd)

# adjust pandas settings to view full column width
pd.set_option('max_colwidth', 1000)

# html for custom hover tool
hover = HoverTool(tooltips="""
    <div>
        <div>
            <img src="@img" width=400 style="float: left; margin: 0px 15px 15px 0px; border="2"></img>
        </div>
    </div>

""")

# Use number of models and regions to determine cell size
num_models = len(dd['model'].unique())
num_regions = len(dd['region'].unique())

cell_width = 1/num_models
cell_height = 1/num_regions

# set desired figure size
desired_width = 2000
desired_height = 2000

# calculate final width and height based on above parameters
adjusted_width = round(int(cell_width * desired_width), -1)
adjusted_height = round(int(cell_height * desired_height), -1)

peak_plot11 = dd.hvplot.heatmap(y='model',
                       x='region',
                       C='peak',
                       hover_cols = ['img'],
                       tools = [hover],
                       height = adjusted_height,
                       width = adjusted_width,
                       colorbar=True,
                       clabel = 'peak day',
                       xaxis='top',
                       clim = (-180,180),
#                       cmap='blues').opts(xrotation=45, fontsize={
                       cmap='RdBu_r').opts(xrotation=45, fontsize={
                           'labels': 14,
                           'xticks': 14,
                           'yticks': 14
                       })

peak_plot11 = peak_plot11 * hv.Labels(peak_plot11)

plt.show()

hvplot.save(peak_plot11, 'charts/peak_plot17.html')
