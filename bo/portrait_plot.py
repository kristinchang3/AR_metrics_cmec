import numpy as np
import pandas as pd
import json
import panel as pn
from matplotlib import pyplot as plt
import hvplot.pandas
from PIL import Image
import os, os.path
from bokeh.models import HoverTool

# load data from json file
f = 'data/peak_season_cmec.json'
with open(f) as og_file:
    dat = json.load(og_file)


# convert json data to pandas dataframe 
ps_df = pd.DataFrame.from_dict(dat['RESULTS'], orient='index')

# format pandas df for portrait plot
ps_df['Model'] = ps_df.index
ps_df = ps_df.reset_index()
ps_df = ps_df[['Model', 'peak season']]
ps_df['var_name'] = 'peak season'



# load histogram png files
imgs = []
path = "./images/"
for p in os.listdir(path):
    ext = os.path.splitext(p)[1]
    imgs.append(Image.open(os.path.join(path,p)))

# view one image to confirm
#imgs[0].show()


# add image links to df
# edit hyperlinks from github repo to match format below (add 'raw.githubusercontent.com', remove 'blob' from path)
# link order should match order of models displayed in df above

img_links = ['https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/BCC-CSM2-MR.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CSIRO-Mk3.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/CanESM2.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/ERA5.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MERRA2.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/MRI-ESM2.png',
             'https://raw.githubusercontent.com/kristinchang3/peak_season_cmec/main/images/NorESM1.png',
             ]

ps_df['img'] = img_links

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


peak_plot01 = ps_df.hvplot.heatmap(y='var_name',
                       x='Model',
                       C='peak season',
                       hover_cols = ['img'],
                       tools = [hover],
                       height = 300,
                       width=950,
                       colorbar=True,
                       xaxis='top',
                       cmap='bwr').opts(xrotation=45, fontsize={
                           'labels': 14,
                           'xticks': 14,
                           'yticks': 14
                       })
peak_plot01




# save portrait plot to charts folder as an html file
# change file name each time saving a new version
# update index.md file to match new html file name

# hvplot.save(peak_plot01, 'charts/peak_plot12.html')

# push changes to github to see updates on live webpage




