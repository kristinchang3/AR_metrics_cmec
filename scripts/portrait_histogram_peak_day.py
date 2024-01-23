import numpy as np
import pandas as pd
import json
import panel as pn
from matplotlib import pyplot as plt
import holoviews as hv
import hvplot.pandas
from PIL import Image
import os, os.path
from bokeh.models import HoverTool, HTMLLabel, Rect, ColumnDataSource
import math
from scipy.stats import ttest_ind

#------------------------------------------------------------
def peak_day(clim_mean):
    N = 12
    T = 1.0 / 12     # sample spacing, f = 800 Hz

    xf = np.linspace(0.0, N*T, N)
    y = clim_mean
    yf = np.fft.fft(y)
    phase_angle_day = 365*np.angle(yf[0:N//2])/(2*np.pi)
    peak = -np.arctan2(yf[1].imag, yf[1].real)*365/(2*np.pi)+(365/12/2)
    peak = int(peak)

    return peak

def zscore(a, b):
    na = a.shape[0]
    nb = b.shape[0]

    bias = np.mean(a) - np.mean(b)
    t_statistic, p_value = ttest_ind(a, b, equal_var=True)

    z = bias/np.sqrt(np.var(a)/na + np.var(b)/nb)

    return z, p_value
#------------------------------------------------------------

#peak = np.loadtxt('data/output_diff_all_region.txt')
#angle = peak.reshape(5,-1)
#angle = angle - ref_peak

region_list = ['California','SAmerica', 'NEurope','Australia','SAfrica']
region_list = region_list + ['Baja','PAC NW','New Zealand','Alaska'] + ['UK','WEurope']
region_list = region_list + ['Iceland','Greenland','EAsia','Antarctica','New England',]

#-----------------------------------------------------------------------
list_dir = "/global/cfs/projectdirs/mp193/ARTMIP/list/"
count_dir = "/global/cfs/projectdirs/mp193/ARTMIP/list/"

model_list = ["BCC-CSM2-MR","CanESM2","CCSM4","CSIRO-Mk3-6-0","NorESM1-M","MRI-ESM2-0",'IPSL-CM5A-LR', 'IPSL-CM5B-LR']
ARDT_list = ['arconnect','Lora','Mundhenk','TECA','TE']
region_list = ['Baja']
region = 'Baja'

angle = np.empty([len(model_list), len(ARDT_list)])
z_score = np.empty([len(model_list), len(ARDT_list)])

for i, model_name in enumerate(model_list):
    for j, ARDT in enumerate(ARDT_list):

        count_hist_list = list_dir+model_name+'_'+ARDT+'_'+region+'_mthly_count_hist.txt'
        count_proj_list = list_dir+model_name+'_'+ARDT+'_'+region+'_mthly_count_proj.txt'

#        duration_hist_list = count_dir + model_name+'_'+ARDT+'_'+region+'_duration_hist.txt'
#        duration_proj_list = count_dir + model_name+'_'+ARDT+'_'+region+'_duration_proj.txt'

#        interval_hist_list = count_dir + model_name+'_'+ARDT+'_'+region+'_interval_hist.txt'
#        interval_proj_list = count_dir + model_name+'_'+ARDT+'_'+region+'_interval_proj.txt'


        hist0 = np.loadtxt(count_hist_list)
        proj0 = np.loadtxt(count_proj_list)

        mod = hist0.size%12
        if mod != 0:
            hist0 = hist0[0:hist0.size-mod]
            print(hist0.size,' ',model_name,' ',ARDT)

        mod = proj0.size%12
        if mod != 0:
            proj0 = proj0[0:proj0.size-mod]
            print(proj0.size,' ',model_name,' ',ARDT)


        hist = hist0.reshape(-1,12)
        proj = proj0.reshape(-1,12)

        score_hist = np.empty(hist.shape[0])
        score_proj = np.empty(proj.shape[0])

        for k in range(hist.shape[0]):
            score_hist[k] = peak_day(hist[k,:])

        for k in range(proj.shape[0]):
            score_proj[k] = peak_day(proj[k,:])

        hist_clim = hist.mean(axis=0)
        proj_clim = proj.mean(axis=0)

        hist_peak = peak_day(hist_clim)
        proj_peak = peak_day(proj_clim)

        angle[i,j] = proj_peak - hist_peak
        z_score[i,j],_ = zscore(score_proj, score_hist)


angle = np.where(angle < -182, angle+365, angle)
angle = np.where(angle >  182, angle-365, angle)


#-----------------------------------------------------------------------

da = pd.DataFrame(data=angle, index=model_list, columns=ARDT_list)

dd = da.stack()
dd = dd.reset_index()
dd = dd.rename(columns={"level_0": "model", "level_1": "region", 0 :"peak"})
ddd = dd['peak'].values

#print(dd)

img_path = 'https://raw.githubusercontent.com/kristinchang3/AR_metrics_cmec/main/images/'
img_links = []

for i, model in enumerate(model_list):
    for j, region in enumerate(ARDT_list):
        filename = img_path+'histogram_'+region+'_'+str(i)+"_"+str(j)+'.png'
        img_links.append(filename)

#print(img_links)


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
#aspect_ratio = num_models/num_regions
aspect_ratio = num_regions/num_models

# Define hook function to adjust clabel position
def adjust_clabel(plot, element):
    color_bar = plot.state.right[0]
    color_bar.title = '' # removes default title
    # create a custom title
    label = HTMLLabel(y=100*num_models + 80,
                  x=((100*num_regions)/2) + 20,
                  angle=-math.pi/2,
                  x_units='screen',
                  y_units='screen',
                  text='days',
                  text_font_size='10pt',
                  text_font_style='normal'
                  )
    plot.state.add_layout(label)

def overlay_hatches(plot, element):
    renderer = plot.state  # Access the Bokeh plot

    # Determine the unique categories and their order on the x-axis
    x_categories = element.dimension_values('model', expanded=False)
    y_categories = element.dimension_values('region', expanded=False)

    # Iterate over the data to find which cells meet the condition
    rects_to_add = []
    for idx, row in dd.iterrows():
        if row['peak'] < 0:  # Condition for applying hatches
            # Map the categorical values to their numerical positions
            x_index = np.where(x_categories == row['model'])[0][0] + 0.5
            y_index = np.where(y_categories == row['region'])[0][0] + 0.5
            rects_to_add.append((x_index, y_index))

    # Create a ColumnDataSource for the rectangles
    source = ColumnDataSource(data={'model': [x for x, _ in rects_to_add],
                                    'region': [y for _, y in rects_to_add],
                                    'width': [0.95] * len(rects_to_add),  # Value of 1 moves hatch right on edge of square
                                    'height': [0.95] * len(rects_to_add)})  

    # Overlay hatched rectangles using Bokeh Rect glyph
    rect_glyph = Rect(x='model', y='region', width='width', height='height',
                      fill_alpha=0, line_color=None, hatch_pattern='/', hatch_color='gray')
    renderer.add_glyph(source, rect_glyph)

peak_plot31 = dd.hvplot.heatmap(x='region',
                       y='model',
                       C='peak',
                       hover_cols = ['img'],
                       tools = [hover],
                       #frame_height = 100 * num_regions,
                       frame_height = 100 * num_models,
                       aspect = aspect_ratio,
                       xaxis='top',
                       clim = (-180,180),
                       cmap='RdBu_r'
                       ).opts(xrotation=45,
                              fontsize={
                                  'labels':10,
                                  'xticks': 10, 
                                  'yticks': 10
                                  },
                                  colorbar = True,
                                  hooks=[adjust_clabel,
                                         overlay_hatches
                                         ]
                                  )

peak_plot31 = peak_plot31 * hv.Labels(peak_plot31).opts(text_color='black')

plt.show()

hvplot.save(peak_plot31, '../charts/histogram_peak_day_Baja.html')
