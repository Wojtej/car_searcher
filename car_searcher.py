git add requirements.txt
git commit -m "Added joblib to requirements.txt"
git push origin car_searcher

import streamlit as st
import webbrowser
import pandas as pd
import joblib
import numpy as np

# Wczytanie wytrenowanego modelu AI do oceny ofert
try:
    model = joblib.load("model.pkl")
except FileNotFoundError:
    model = None
    
# Funkcja generująca linki wyszukiwania
def generuj_linki(marka, model, cena_max):
    base_mobile = "https://suchen.mobile.de/fahrzeuge/search.html?"
    url_mobile = f"{base_mobile}isSearchRequest=true&makeModelVariant1.makeId=3500&makeModelVariant1.modelId=9&maxPrice={cena_max}"

    base_autoscout = f"https://www.autoscout24.de/lst/{marka.lower()}?price=0-{cena_max}"
    
    return url_mobile, base_autoscout

# Funkcja symulująca pobranie ofert (zamiast scrapingu)
def pobierz_oferty(marka, model, cena_max):
    dane = [
        {"Serwis": "Mobile.de", "Marka": marka, "Model": model, "Cena": np.random.randint(5000, cena_max), "Rok": np.random.randint(2010, 2023)},
        {"Serwis": "AutoScout24", "Marka": marka, "Model": model, "Cena": np.random.randint(5000, cena_max), "Rok": np.random.randint(2010, 2023)}
    ]
    return pd.DataFrame(dane)

# Funkcja oceny atrakcyjności
def ocen_atrakcyjnosc(oferty):
    if model:
        cechy = oferty[["Cena", "Rok"]]
        oferty["Atrakcyjność"] = model.predict(cechy)
    else:
        oferty["Atrakcyjność"] = np.random.uniform(0, 1, len(oferty))  # Losowa wartość w przypadku braku modelu
    return oferty

# Interfejs użytkownika
st.title("🔎 Inteligentna Wyszukiwarka Samochodów")

marka = st.text_input("Marka", "BMW")
model = st.text_input("Model", "3er")
cena_max = st.number_input("Cena maksymalna (EUR)", min_value=1000, value=15000)

if st.button("Szukaj 🚀"):
    url_mobile, url_autoscout = generuj_linki(marka, model, cena_max)
    oferty = pobierz_oferty(marka, model, cena_max)
    oferty = ocen_atrakcyjnosc(oferty)
    
    st.write("🔗 [Otwórz Mobile.de](%s)" % url_mobile)
    st.write("🔗 [Otwórz AutoScout24](%s)" % url_autoscout)
    
    st.write("### 📊 Zestawienie ofert:")
    st.dataframe(oferty.sort_values("Atrakcyjność", ascending=False))
