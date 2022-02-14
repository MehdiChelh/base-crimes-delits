import streamlit as st
import plotly.express as px
from urllib.request import urlopen
import json
from data import read_police_data


@st.cache
def load_data():
    # Data - Police
    df, df_libelle = read_police_data()
    df_departement = df.iloc[:, 0:108].groupby("Départements").sum()
    df_departement["Département"] = df_departement.index
    # Data - Geojson
    with urlopen('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson') as response:
        counties = json.load(response)
        counties = {**counties, "features": [{"id":e["properties"]["code"], **e} for e in counties["features"]]}
    return df_departement, df_libelle, counties


df_departement, df_libelle, counties = load_data()

# UI
st.write("""# Crimes et délits""")
option = st.selectbox(
    'Type de crime ou délit:',
    df_libelle)
option_id = df_libelle[df_libelle == option].index[0]

# UI - Plot
fig = px.choropleth_mapbox(df_departement[0:96], geojson=counties, locations="Département", color=option_id,
                           color_continuous_scale="Viridis",
                           range_color=(df_departement[option_id].min(),
                                        df_departement[option_id].max()),
                           mapbox_style="carto-positron",
                           zoom=4.5, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                           labels={option_id: option})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Plot!
st.plotly_chart(fig, use_container_width=True)