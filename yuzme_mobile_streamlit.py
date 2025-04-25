
import streamlit as st
import pandas as pd
import joblib

# Modeli yükle
model = joblib.load("yuzme_model3_cinsiyetli.pkl")

# Sayfa başlığı
st.set_page_config(page_title="100m Yüzme Süresi Tahmini", layout="centered")
st.title("🏊 100m Serbest Stil Tahmini (Mobil)")

st.markdown("Yaş, boy, reaksiyon süresi, 50m split ve cinsiyet bilgilerinizi girin:")

# Girdi alanları (mobil uyumlu)
age = st.number_input("Yaş", min_value=10, max_value=100, value=20)
height = st.number_input("Boy (cm)", min_value=120, max_value=230, value=180)
reaction = st.number_input("Reaksiyon Süresi (saniye)", min_value=0.4, max_value=1.2, value=0.7, step=0.01)
split_50 = st.number_input("50m Split Süresi (saniye)", min_value=20.0, max_value=30.0, value=24.0, step=0.1)
gender_input = st.radio("Cinsiyet", ["Erkek", "Kadın"])

# Cinsiyet kodlama
gender_code = 0 if gender_input == "Erkek" else 1

# Tahmin butonu
if st.button("Tahmini Hesapla"):
    new_data = pd.DataFrame([{
        "Age": age,
        "Height": height,
        "ReactionTime": reaction,
        "Split_50m": split_50,
        "Gender_Code": gender_code
    }])
    predicted_time = model.predict(new_data)[0]
    st.success(f"🏁 Tahmini Final Süresi: {predicted_time:.2f} saniye")
