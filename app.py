import streamlit as st
import geemap as geemap
import folium
from streamlit_folium import st_folium
from processing import SpatialProcessor
st.cache_data.clear()
st.cache_resource.clear()

st.title("Mon Premier Portail GEE")

# 1. Connexion au moteur métier
@st.cache_resource
def load_engine():
    return SpatialProcessor()

engine = load_engine()

# 2. Formulaire de saisie
with st.sidebar:
    st.header("Coordonnées")
    lat = st.number_input("Latitude", value=48.85, format="%.4f")
    lon = st.number_input("Longitude", value=2.35, format="%.4f")
    submit = st.button("Afficher la zone")


# 3. Affichage de la carte (Version STABLE)

if submit:

    with st.spinner("Récupération de l'image depuis le Cloud..."):

        # Image Earth Engine
        img = engine.get_satellite_image(lat, lon)

        # Paramètres d'affichage
        vis_params = {
            'bands': ['B4', 'B3', 'B2'],
            'min': 0,
            'max': 3000
        }

        # Création carte Folium
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # Ajout image Sentinel
        geemap.ee_tile_layer(
            img,
            vis_params,
            "Sentinel-2"
        ).add_to(m)

        # Affichage stable Streamlit
        st_folium(m, height=600, width=700)

        st.success(f"Image chargée pour {lat}, {lon}")