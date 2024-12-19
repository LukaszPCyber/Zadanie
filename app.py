import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Wczytaj dane
@st.cache
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

# Wykresy
st.write("## Analiza wizualna")

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

# Zliczanie metod płatności
payment_counts = filtered_data["Payment Method"].value_counts()

# Wykres kołowy metod płatności
fig, ax = plt.subplots()
payment_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90, cmap="viridis")
ax.set_ylabel("")  # Usunięcie domyślnego opisu osi
ax.set_title("Procentowy rozkład metod płatności")

# Wyświetlenie wykresu
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

# Dynamiczne mapowanie lokalizacji na współrzędne
st.write("### Mapa lokalizacji zakupów")

def get_coordinates(location):
    geolocator = Nominatim(user_agent="shopping_trends_app")
    try:
        loc = geolocator.geocode(location)
        return [loc.latitude, loc.longitude] if loc else None
    except:
        return None

# Dodanie współrzędnych do danych
filtered_data = filtered_data.copy()
filtered_data["Coordinates"] = filtered_data["Location"].apply(get_coordinates)
filtered_data = filtered_data.dropna(subset=["Coordinates"])

# Przygotowanie danych dla pydeck
import pydeck as pdk
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
