# module importation
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

#https://raw.githubusercontent.com/YonQwon/visulization_of_kenya_voters/main/data/voters.csv
#data importing
df=pd.read_csv("https://raw.githubusercontent.com/YonQwon/visulization_of_kenya_voters/main/data/voters.csv")
subgeo=gpd.read_file("https://raw.githubusercontent.com/YonQwon/visulization_of_kenya_voters/main/data/map.geojson")


df.drop(columns="Unnamed: 0",inplace=True)
#st.write(df.head(20))
add_selectbox=st.sidebar.selectbox(
    'Name of the County?',
    (df["County Name"].unique())

)
map_selectbox=st.sidebar.selectbox(
    'Select map type?',
    ('open-street-map','white-bg', 'carto-positron', 'carto-darkmatter','stamen-terrain','stamen-toner', 'stamen-watercolor'))



st.write(f"You have chosen  {add_selectbox} county")


#masking the county name
mask=df[df["County Name"]==add_selectbox]
dtx=mask.groupby("Constituency")["Registered Voters"].sum().sort_values(ascending=False)
fig=px.bar(data_frame=dtx,
           color=dtx,
           color_continuous_scale="thermal",
           height=600,
           width=1200,
           
        )
#Number of voters
numvoters=mask["Registered Voters"].sum()
numvoters=numvoters
p=print(f"{add_selectbox} County  have {numvoters} number of voters")

#piechat
pie=px.pie(mask,
           names="Constituency",
           values="Registered Voters",
           #color="Registered Voters",
           hole=.3,
           color_discrete_sequence=px.colors.sequential.RdBu,
           labels="Constituency",
           height=600,
           width=1200
           )
pie.update_traces(textposition='inside',textinfo='percent+label')


#sunbrust
sun=px.sunburst(mask,
                path=["Constituency","CAW Name"],
                values="Registered Voters",
                color="Registered Voters",
                color_continuous_scale='RdBu',
                width=1200,
                height=800,
                title="A sunbrurt of voters in constituency and locations"
                )

#streamlight code 

with st.container():  
    
 st.write(numvoters,f"is the number of voter in  {add_selectbox} county")   
 tab1, tab2, = st.tabs(["Bar chart","Pie chart"])


with tab1:
    st.write(fig)
    st.write(numvoters,f"is the number of voter in  {add_selectbox} county")
with tab2:         
  
    st.write(pie.update_traces(textposition='inside',textinfo='percent+label'))

with st.container():
    st.write(sun)
    
    
#code for operation for subgeo and greating a data frame for constituency
subdf=df.groupby("Constituency")["Registered Voters"].sum()
sd=pd.DataFrame().from_dict(subdf).reset_index()
#Code to capitilize shapeName and Constituency name
subgeo.rename(columns={"shapeName":"Constituency"},inplace=True)
subgeo["Constituency"]=subgeo["Constituency"].str.upper()
#maping
consmap=px.choropleth_mapbox(
              data_frame=sd,
              geojson=subgeo,
              locations="Constituency",
              featureidkey="properties.Constituency",
              color="Registered Voters",
              hover_data="Registered Voters",
              mapbox_style=map_selectbox,
              #mapbox_style="carto-positron",
              #mapbox_style="carto-darkmatter",
              opacity=.6,
              center={"lat":0.10,"lon":36.54},
              zoom=6,
              height=800,
              width=1200,
              color_continuous_scale="Viridis"
              )
with st.container():
    st.write(consmap.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        ))
st.write("                                                                                                                                                                           My is Samy Migwi an entry-level (at the time of working on this project) data scientist. I started this project with a pdf file from the IEBC website https://www.iebc.or.ke . From the pdf file, I wrote a Python script to convert it to .csv(excel file). I then cleaned the data using pandas. The next step was to find the .geojson file(map coordinates for every sub-county (which took weeks). From there I combined my geojson file my clean csv file and my favorite visualization library Plotly.express to do visualization. For me to deploy my app I started with dash but later shifted to the strealit library because of many becauses.In the following project i have used the following libraries geopandas,pandas,numpy json, geojson ,re,plotly.expess,streamlit among ohers")
