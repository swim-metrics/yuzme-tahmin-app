
import streamlit as st
import pandas as pd
import joblib

# Modeli yükle
model = joblib.load("yuzme_model5_cinsiyetli.pkl")

# Başlık
st.markdown("🏊‍♂️ **100m Serbest Stil Tahmini (Mobil)**")

st.markdown("Yaş, boy, reaksiyon süresi, 50m split ve cinsiyet bilgilerinizi girin:")

# Girdi alanları
age = st.number_input("Yaş", min_value=10, max_value=100, value=20)
height = st.number_input("Boy (cm)", min_value=100, max_value=250, value=180)
reaction = st.number_input("Reaksiyon Süresi (saniye)", min_value=0.1, max_value=2.0, value=0.70, step=0.01)
split_50 = st.number_input("50m Split Süresi (saniye)", min_value=15.0, max_value=40.0, value=24.00, step=0.01)

gender = st.radio("Cinsiyet", ("Erkek", "Kadın"))
gender_code = 0 if gender == "Erkek" else 1

if st.button("Tahmini Hesapla"):
    try:
        new_data = pd.DataFrame([[
            age,
            height,
            reaction,
            split_50,
            gender_code
        ]])
        predicted_time = model.predict(new_data)[0]
        st.success(f"🏁 Tahmini 100m Final Süresi: {predicted_time:.2f} saniye")
    except Exception as e:
        st.error("Bir hata oluştu. Lütfen bilgilerinizi kontrol edin.")
        st.exception(e)
