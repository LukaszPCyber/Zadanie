import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import pydeck as pdk

# Wczytaj dane
@st.cache_data
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())

# Filtruj dane
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Category"].isin(category_filter))]

# Wyświetlanie danych
st.write("### Filtrowane dane", filtered_data)

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Nowy wykres: Rozkład metod płatności
st.write("### Rozkład metod płatności")
payment_counts = filtered_data["Payment Method"].value_counts()
fig, ax = plt.subplots()
payment_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90, cmap="viridis")
ax.set_ylabel("")  # Usunięcie domyślnego opisu osi
ax.set_title("Procentowy rozkład metod płatności")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
season_mean.plot(kind="bar", ax=ax)
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots()
filtered_data["Age"].hist(bins=20, ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
st.pyplot(fig)

# Statyczne współrzędne dla stanów USA
state_coordinates = {
    "Kentucky": [37.8393, -84.2700],
    "Maine": [45.2538, -69.4455],
    "Massachusetts": [42.4072, -71.3824],
    "Rhode Island": [41.5801, -71.4774],
    "Oregon": [43.8041, -120.5542],
    "Wyoming": [43.0760, -107.2903],
    "Louisiana": [30.9843, -91.9623],
    "West Virginia": [38.5976, -80.4549],
    "Missouri": [37.9643, -91.8318],
    "Arkansas": [34.7465, -92.2896],
    "Hawaii": [20.7967, -156.3319],
    "Alabama": [32.3182, -86.9023],
    "Mississippi": [32.3547, -89.3985],
    "Montana": [46.8797, -110.3626],
    "North Carolina": [35.7596, -79.0193],
    "California": [36.7783, -119.4179],
    "Oklahoma": [35.0078, -97.0929],
    "Florida": [27.9944, -81.7603],
    "Texas": [31.9686, -99.9018],
    "Nevada": [38.8026, -116.4194],
    "Kansas": [39.0119, -98.4842],
    "Colorado": [39.5501, -105.7821],
    "North Dakota": [47.5515, -101.0020],
    "Illinois": [40.6331, -89.3985],
    "Indiana": [40.2672, -86.1349]
}

# Dodanie współrzędnych do danych
filtered_data = filtered_data.copy()
filtered_data["Coordinates"] = filtered_data["Location"].map(state_coordinates)
filtered_data = filtered_data.dropna(subset=["Coordinates"])

# Przygotowanie danych dla pydeck
map_data = pd.DataFrame(
    filtered_data["Coordinates"].tolist(),
    columns=["lat", "lon"]
)

# Wyświetlenie mapy
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=37.0902,
        longitude=-95.7129,
        zoom=3,
        pitch=50
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=100000,
        ),
    ],
))
