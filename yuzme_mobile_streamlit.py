import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="100m Serbest Stil Tahmini (Mobil)", layout="centered")

st.title("🏊‍♂️ 100m Serbest Stil Tahmini (Mobil)")
st.markdown("Yaş, boy, reaksiyon süresi, 50m split ve cinsiyet bilgilerinizi girin:")

# Girdi alanları
age = st.number_input("Yaş", min_value=10, max_value=100, value=20)
height = st.number_input("Boy (cm)", min_value=100, max_value=250, value=180)
reaction_time = st.number_input("Reaksiyon Süresi (saniye)", min_value=0.0, max_value=2.0, step=0.01, value=0.70)
split_50m = st.number_input("50m Split Süresi (saniye)", min_value=20.0, max_value=30.0, step=0.01, value=24.00)
gender = st.radio("Cinsiyet", ["Erkek", "Kadın"])

# Cinsiyeti sayısal değere çevir (Erkek: 1, Kadın: 0)
gender_code = 1 if gender == "Erkek" else 0

# Modeli yükle (5 değişkenli model)
model = joblib.load("yuzme_model5_cinsiyetli.pkl")

if st.button("Tahmini Hesapla"):
    input_data = np.array([[age, height, reaction_time, split_50m, gender_code]])
    predicted_time = model.predict(input_data)[0]
    st.success(f"✅ Tahmini 100m Final Süresi: {predicted_time:.2f} saniye")
  
