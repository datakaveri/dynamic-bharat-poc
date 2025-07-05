import folium
import streamlit as st
from folium.plugins import Draw
import xarray as xr
import get_results as gr
import warnings
warnings.filterwarnings('ignore')
import plotly.graph_objects as go
import numpy as np


from streamlit_folium import st_folium
st.set_page_config(layout='wide')
st.title("Dynamic Bharat - Changes in Land Use over Time")


c1,c2 = st.columns([0.3, 0.7])
## fixed for hyderabad
locations = [
    [17.48875008265665, 78.32539298515482],
[17.474619897520927, 78.39807339906744],
[17.31654690472666, 78.36400909034819],
[17.33003726964443, 78.28945900216388],
    
]
with c1:
   m = folium.Map(location=[17.365548014635493, 79.26549911841008], zoom_start=13)
   folium.Polygon(
    locations=locations,
    smooth_factor=2,
    color="crimson",
    no_clip=True,
    tooltip="Hi there!",
).add_to(m)
   # folium.TileLayer("OpenStreetMap", overlay=False).add_to(m)
   
   folium.TileLayer(
      tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      attr = 'Esri',
      name = 'Esri Satellite',
      overlay = True,
      control = True, 
               ).add_to(m)
   Draw(export=True).add_to(m)
   
   folium.LayerControl().add_to(m)
   output = st_folium(m, width=10000, height=600)
   
try:
   coords = output['all_drawings'][0]['geometry']["coordinates"][0]
   topLeft = coords[0]
   bottomRight = coords[2]
   print(coords) 
except Exception as e:
   print(e)


# Cache the results to avoid reloading
@st.cache_data
def get_cached_results(topLeft, bottomRight):
    return gr.get_results(topLeft, bottomRight)

r = None
       
try:
   if 'coords' in locals():
      r = get_cached_results(topLeft, bottomRight)
      print('got the results')
   else:
        pass 
except Exception as e:
   print(e)

with c2:  
        
   if r is not None:   
      option = st.radio("Select the class", options=["Buildings", "Roads", "Vegetation Cover", 'Water Bodies'] ) 
         
      if option == 'Buildings':
            results = r[0]
      elif option == 'Roads':
            results = r[1]
      elif option == 'Vegetation Cover':
            results = r[2]
      else:
            results = r[3]

            
      
      count_1_xarr1 = results['count_1_xarr1']
      count_1_xarr2 = results['count_1_xarr2']
      abs_change_1 = results['absolute_change_1']
      pct_change_1 = results['percentage_change_1']
      bs_change_0 = results['absolute_change_0']
      pct_change_0 = results['percentage_change_0']

      area_1 = count_1_xarr1*1.14
      area_2 = count_1_xarr2*1.14
   
      # Get all results for all charts
      buildings_2020 = r[0]['count_1_xarr1'] * 1.14
      buildings_2023 = r[0]['count_1_xarr2'] * 1.14
      roads_2020 = r[1]['count_1_xarr1'] * 1.14
      roads_2023 = r[1]['count_1_xarr2'] * 1.14
      vegetation_2020 = r[2]['count_1_xarr1'] * 1.14
      vegetation_2023 = r[2]['count_1_xarr2'] * 1.14
      water_2020 = r[3]['count_1_xarr1'] * 1.14
      water_2023 = r[3]['count_1_xarr2'] * 1.14

      # Create a 2x2 grid for charts
      chart_col1, chart_col2 = st.columns(2)
      
      with chart_col1:
          # Bar chart for selected option
          labels = ["2020", "2023"]
          values = [area_1, area_2]

          fig = go.Figure()

          # Add bar chart
          fig.add_trace(go.Bar(
             x=labels,
             y=values,
             name="Area",
             textposition="auto"
          ))

          # Add line chart
          fig.add_trace(go.Scatter(
             x=labels,
             y=values,
             mode='lines+markers',
             name="Area Trend",
             line=dict(color='royalblue', width=2),
             marker=dict(size=8)
          ))

          # Customize layout with smaller height
          fig.update_layout(
             title=f"{option} - Area Change",
             xaxis_title="Year",
             yaxis_title="Area (sq.m)",
             template="plotly_white",
             height=400  # Reduced height
          )

          st.plotly_chart(fig, use_container_width=True)

          
          
          # Determine color and status based on change
          if abs_change_1 < 0:
              change_color = "red"
              change_status = "lost"
          else:
              change_color = "green"
              change_status = "gained"
          
          st.markdown(f"**Change in Area:** <span style='color: {change_color}; font-size:20px'>{abs(abs_change_1/10000):.2f} sq.km ({change_status})</span>", unsafe_allow_html=True)

      with chart_col2:
          # Create pie chart for 2020
          fig_pie_2020 = go.Figure(data=[go.Pie(
             labels=['Buildings', 'Roads', 'Vegetation Cover', 'Water Bodies'], 
             values=[buildings_2020, roads_2020, vegetation_2020, water_2020], 
             hole=0.3,
             marker=dict(colors=['red', 'black', 'green', 'blue'])
          )])

          fig_pie_2020.update_layout(
             title="Land Use Composition - 2020",
             template="plotly_white",
             height=400  # Reduced height
          )

          st.plotly_chart(fig_pie_2020, use_container_width=True)

      # Second row for the 2023 pie chart
      chart_col3, chart_col4 = st.columns(2)
      
      with chart_col3:
          # Empty space to maintain alignment
          st.empty()
          
      with chart_col4:
          # Create pie chart for 2023
          fig_pie_2023 = go.Figure(data=[go.Pie(
             labels=['Buildings', 'Roads', 'Vegetation Cover', 'Water Bodies'], 
             values=[buildings_2023, roads_2023, vegetation_2023, water_2023], 
             hole=0.3,
             marker=dict(colors=['red', 'black', 'green', 'blue'])
          )])

          fig_pie_2023.update_layout(
             title="Land Use Composition - 2023",
             template="plotly_white",
             height=400  # Reduced height
          )

          st.plotly_chart(fig_pie_2023, use_container_width=True)