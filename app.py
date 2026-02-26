import streamlit as st
import geemap.foliumap as geemap
from processing import SpatialProcessor

st.title("Mon Premier Portail GEE")

@st.cache_resource
def load_engine():
    return SpatialProcessor()

engine = load_engine()

with st.sidebar:
    st.header("Coordonnées")
    lat = st.number_input("Latitude", value=48.85, format="%.4f")
    lon = st.number_input("Longitude", value=2.35, format="%.4f")
    submit = st.button("Afficher la zone")

map_placeholder = st.empty()

if submit:

    with st.spinner("Récupération de l'image depuis le Cloud..."):

        img = engine.get_satellite_image(lat, lon)

        vis_params = {
            'bands': ['B4', 'B3', 'B2'],
            'min': 0,
            'max': 3000
        }

        m = geemap.Map(center=[lat, lon], zoom=12)
        m.addLayer(img, vis_params, 'Sentinel-2 Image')

        map_placeholder.components.v1.html(
            m.to_html(),
            height=600
        )

        st.success(f"Image chargée pour {lat}, {lon}")