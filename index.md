---
layout: default
#altair-loader:
#  altair-chart-1: "charts/measlesAltair.json"
hv-loader:
  hv-chart-1: ["charts/reanalyses_plot02.html", "1000"] # second argument is the desired height
  hv-chart-2: ["charts/bias_vs_era5_03.html", "1100"]
#folium-loader:
#  folium-chart-1: ["charts/foliumChart.html", "400"] # second argument is the desired height
---
<div style="text-align: center;" markdown="1">
# Welcome! 

This is an internal test page with an interactive data visualization.

[Link to Bo's test page](./bo/bo_index.html)
</div>
<div style="text-align: center;" markdown="1">
# AR Regions 
### MJJAS 
<p align="center">
  <img src="images/MJJAS.png" width="400"/>
</p>
</div>
<div style="text-align: center;" markdown="1">
### NDJFM 
<p align="center">
  <img src="images/NDJFM.png" width="400"/>
</p>
</div>
<div style="text-align: center;" markdown="1">
# Portrait Plot 

Visualizing the Peak Season CMEC data: 

## Landfalling AR Peak Day in Reanalyses
<div id="hv-chart-1"></div>

## Landfalling AR Peak Day Bias vs. ERA5
<div id="hv-chart-2"></div>
</div>

</div>
<div style="text-align: center;" markdown="1">
# AR character metrics
<p align="center">
  <img src="images/AR_character_N. Pacific.png" width="600"/>
</p>

<p align="center">
  <img src="images/AR_character_S. Pacific.png" width="600"/>
</p>

<p align="center">
  <img src="images/AR_character_N. Atlantic.png" width="600"/>
</p>

<p align="center">
  <img src="images/AR_character_S. Atlantic.png" width="600"/>
</p>

<p align="center">
  <img src="images/AR_character_Indian Ocean.png" width="600"/>
</p>

