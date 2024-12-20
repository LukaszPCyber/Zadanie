import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

# Wykres 2: Rozkład metod płatności
st.write("### Rozkład metod płatności")
if not filtered_data.empty:
    payment_counts = filtered_data["Payment Method"].value_counts()
    fig, ax = plt.subplots()
    payment_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90, cmap="viridis")
    ax.set_ylabel("")  # Usunięcie domyślnego opisu osi
    ax.set_title("Procentowy rozkład metod płatności")
    st.pyplot(fig)
else:
    st.write("Brak danych do analizy rozkładu metod płatności.")

# Wykres 3: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
if not filtered_data.empty:
    season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
    fig, ax = plt.subplots()
    season_mean.plot(kind="bar", ax=ax)
    ax.set_xlabel("Sezon")
    ax.set_ylabel("Średnia kwota zakupów (USD)")
    st.pyplot(fig)
else:
    st.write("Brak danych do analizy kwot zakupów wg sezonu.")

# Wykres 4: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
if not filtered_data.empty:
    fig, ax = plt.subplots()
    filtered_data["Age"].hist(bins=20, ax=ax)
    ax.set_xlabel("Wiek")
    ax.set_ylabel("Liczba klientów")
    st.pyplot(fig)
else:
    st.write("Brak danych do analizy liczby klientów wg wieku.")

# Podsumowanie statystyk klientów
def display_customer_summary(filtered_data):
    """
    Wyświetla podsumowanie statystyk klientów w formie tabeli.

    Args:
    - filtered_data (pd.DataFrame): Dane po zastosowaniu filtrów.
    """
    st.write("### Podsumowanie klientów")

    if not filtered_data.empty:
        # Obliczanie statystyk
        avg_age = filtered_data["Age"].mean()
        total_customers = filtered_data["Customer ID"].nunique()
        popular_payment = filtered_data["Payment Method"].mode()[0]

        # Przygotowanie tabeli do wyświetlenia
        summary_data = {
            "Statystyka": ["Średni wiek", "Liczba klientów", "Najpopularniejsza metoda płatności"],
            "Wartość": [f"{avg_age:.2f} lat", total_customers, popular_payment],
        }
        summary_table = pd.DataFrame(summary_data)

        # Wyświetlanie tabeli
        st.table(summary_table)
    else:
        st.write("Brak danych do podsumowania statystyk klientów.")

# Wywołanie funkcji podsumowania
display_customer_summary(filtered_data)
