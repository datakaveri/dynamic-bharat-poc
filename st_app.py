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
st.title("Dynamic Bharat - Changes in Land Use over time")


c1,c2 = st.columns([0.3, 0.7])
locations = [
    [35.6762, 139.7795],
    [35.6718, 139.7831],
    [35.6767, 139.7868],
    [35.6795, 139.7824],
    
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


r = None
       
try:
   if r == None:
      r = gr.get_results(topLeft, bottomRight)
      print('got the results')
   else:
        pass 
except Exception as e:
   print(e)

with c2:  
        
   if r is not None:   
      option = st.radio("Select the class", options=["buildings", "roads", "trees", 'water'] ) 
         
      if option == 'buildings':
            results = r[0]
      elif option == 'roads':
            results = r[1]
      elif option == 'trees':
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
   



      labels = ["2020", "2023"]
      values = [count_1_xarr1, count_1_xarr2]
      co1, co2 = st.columns(2)
      # Create a bar chart with Plotly for count values only

      fig = go.Figure()

      # Add bar chart
      fig.add_trace(go.Bar(
         x=labels,
         y=values,
         name="Counts",
         text=values,
         textposition="auto"
      ))

      # Add line chart
      fig.add_trace(go.Scatter(
         x=labels,
         y=values,
         mode='lines+markers',
         name="Count Trend",
         line=dict(color='royalblue', width=2),
         marker=dict(size=8)
      ))

      # Customize layout
      fig.update_layout(
         title="Counts with Bar and Line Chart",
         xaxis_title="Variables",
         yaxis_title="Values",
         template="plotly_white"
      )

      # Display the plot in Streamlit
      co1.plotly_chart(fig)


      # Create labels and values for the pie chart
      area_labels = ["2020", "2023"]
      area_values = [area_1, area_2]

      # Create a pie chart for area values
      fig_pie = go.Figure(data=[go.Pie(labels=area_labels, values=area_values, hole=0.3)])

      # Customize layout for pie chart
      fig_pie.update_layout(
         title="Area Distribution",
         template="plotly_white"
      )

      # Display the pie chart in Streamlit
      co2.plotly_chart(fig_pie)

      annotations = [
      f"abs_change_1: {abs_change_1}",
      f"pct_change_1: {pct_change_1}",
      f"bs_change_0: {bs_change_0}",
      f"pct_change_0: {pct_change_0}"
      ]

   

      # Display the plot in Streamlit
      
      st.write("### Key Changes")
      col1, col2, col3 = st.columns(3)
      col1.metric(label="Absolute Change 1", value=f"{abs_change_1/10000}sq.km")
      col2.metric(label="Percentage Change 1", value=f"{pct_change_1:2f}%")
      col3.metric(label="Percentage Change 0", value=f"{pct_change_0:2f}%")  

