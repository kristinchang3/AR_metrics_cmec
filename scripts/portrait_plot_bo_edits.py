import numpy as np
import pandas as pd
import json
import panel as pn
from matplotlib import pyplot as plt
import holoviews as hv
import hvplot.pandas
from PIL import Image
import os, os.path
from bokeh.models import HoverTool, HTMLLabel, ColumnDataSource, Rect
from bokeh.models import Label
import math

#angle = np.array([[  0,  86, 199],
#       [ 23, 111, 271],
#       [ 16,  97, 226],
#       [ 17, 103, 159]])

#peak = np.loadtxt('data/output_diff.txt')
#angle = peak.reshape(5,6)
peak = np.loadtxt('data/output_diff_all_region.txt')
angle = peak.reshape(5,-1)
#[[  -5.   11. -156.   -2.  -16.  -77.]
#   5.   75.  -40. -102.  166.  151.]
#ref_peak = np.array([5,75,-10,-105,141,154]) ## !!!! wrong numbers  !!!!
#ref_peak = np.array([5,75,-40,-102,166,151])
#ref_peak = np.atleast_2d(ref_peak)
#ref_peak = np.repeat(ref_peak,repeats=5, axis=0)

#angle = angle - ref_peak

#if angle < -182:
#    angle += 365
#elif angle > 182:
#    angle -= 365

angle = np.where(angle < -182, angle+365, angle)
angle = np.where(angle >  182, angle-365, angle)

print(angle)

#model_names = ["CanESM2","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0"]
#region_names = ['California','S.America', 'W.Africa']
model_names = ["cmip5_CanESM2","cmip5_CCSM4","cmip5_CSIRO-Mk3-6-0","cmip5_NorESM1-M","cmip6_MRI-ESM2-0"]
region_names = ['California','SAmerica', 'Africa','NEurope','Australia','SAfrica']
region_names = region_names + ['Baja','PAC NW','New Zealand','Alaska']

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
        filename = img_path+'fig_'+str(i)+"_"+str(j)+'.png'
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

# select reference dataset
dd_ref = dd.loc[dd['model']=='ERA5']
dd_cmap = dd.loc[dd['model']!='ERA5']

# create custom hover tools to display histogram images
hover_L = HoverTool(tooltips="""
    <div>
        <div>
            <img src="@img" width=500 style="float: left; margin: 0px 15px 15px 0px; border="2"></img>
        </div>
    </div>

""")
hover_R = HoverTool(tooltips="""
    <div>
        <div>
            <img src="@img" width=500 style="float: right; margin: 0px 15px 15px 0px; border="2"></img>
        </div>
    </div>

""")

# Use number of models and regions to determine cell size
num_models = len(dd['model'].unique())
num_regions = len(dd['region'].unique())
aspect_ratio = num_models/num_regions

# Define hook function to adjust clabel position
def adjust_clabel(plot, element):
    color_bar = plot.state.right[0]
    color_bar.title = '' # removes default title
    color_bar.major_label_text_font_size = '14pt' # adjust font size of colorbar tick labels
    # create a custom title
    label = HTMLLabel(x=100*num_models + 80,
                  y=((100*num_regions)/2) + 20,
                  angle=-math.pi/2,
                  x_units='screen',
                  y_units='screen',
                  text='peak day',
                  text_font_size='14pt',
                  text_font_style='normal'
                  )
    plot.state.add_layout(label)
    
# Define hook function to add hatch pattern
def overlay_hatches(plot, element):
    renderer = plot.state  # Access the Bokeh plot

    # Determine the unique categories and their order on the x-axis
    x_categories = element.dimension_values('model', expanded=False)
    y_categories = element.dimension_values('region', expanded=False)

    # Iterate over the data to find which cells meet the condition
    rects_to_add = []
    for idx, row in dd_cmap.iterrows():
        if row['peak'] < 0:  # Condition for applying hatches
            # Map the categorical values to their numerical positions
            x_index = np.where(x_categories == row['model'])[0][0] + 0.5
            y_index = np.where(y_categories == row['region'])[0][0] + 0.5
            rects_to_add.append((x_index, y_index))

    # Create a ColumnDataSource for the rectangles
    source = ColumnDataSource(data={'model': [x for x, _ in rects_to_add],
                                    'region': [y for _, y in rects_to_add],
                                    'width': [0.95] * len(rects_to_add),  # Adjust as needed
                                    'height': [0.95] * len(rects_to_add)})  # Adjust as needed

    # Overlay hatched rectangles using Bokeh Rect glyph
    rect_glyph = Rect(x='model', y='region', width='width', height='height',
                      fill_alpha=0, line_color=None, hatch_pattern='/', hatch_color='black', hatch_scale=20)
    renderer.add_glyph(source, rect_glyph)

peak_cmap = dd_cmap.hvplot.heatmap(y='region',
                       x='model',
                       C='peak',
                       hover_cols = ['img'],
                       tools = [hover_R],
                       frame_height = 100 * num_regions,
                       aspect = aspect_ratio,
                       xaxis='top',
                       clim = (-180,180),
                       cmap='twilight_shifted_r'
                       ).opts(xrotation=45,
                              fontsize={
                                  'labels':10,
                                  'xticks': 10, 
                                  'yticks': 10
                                  },
                                  colorbar = True,
                                  )
                       
peak_ref = dd_ref.hvplot.heatmap(y='region',
                       x='model',
                       C='peak',
                       frame_height = 100 * num_regions,
                       aspect = aspect_ratio,
                       xaxis='top',
                       cmap= ['#FFFFFF', '#ffffff'],
                       line_color='gray',
                       line_width=0.5, 
                       hover_cols='img',
                       tools=[hover_L],
                       ).opts(xrotation=45, 
                              fontsize={
                                  'labels':14,
                                  'xticks': 14, 
                                  'yticks': 14
                                  },
                              colorbar = False
                              )

# custom cmap for label text colors
bins = [-180, -80, 0, 80, 180]
label_colors = ['white','black','black','white']

peak_ref = peak_ref * hv.Labels(peak_ref).opts(text_color='black')
peak_cmap = peak_cmap * hv.Labels(peak_cmap).opts(text_color='peak',
                                                  color_levels=bins,
                                                  cmap=label_colors,
                                                  )
peak_plot = (peak_ref * peak_cmap).opts(hooks=[adjust_clabel, overlay_hatches])

plt.show()

hvplot.save(peak_plot, 'charts/peak_test20240221.html')
