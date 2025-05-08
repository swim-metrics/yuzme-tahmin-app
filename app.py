import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# Dil seçimi
language = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

# Başlık
if language == "English":
    st.title("🏊 Swimming Performance Prediction (50m)")
else:
    st.title("🏊 50m Yüzme Performans Tahmini")

# Girişler
age = st.number_input("Yaş / Age", min_value=10, max_value=20, value=13)
height = st.number_input("Boy (cm) / Height", min_value=130, max_value=210, value=160)
weight = st.number_input("Kilo (kg) / Weight", min_value=30, max_value=120, value=50)
gender = st.selectbox("Cinsiyet / Gender", ["Kadın", "Erkek"])
style = st.selectbox("Yüzme Stili / Stroke", ["Serbest", "Sırtüstü", "Kurbağalama", "Kelebek"])
age_group = st.selectbox("Yaş Grubu / Age Group", ["12_13", "14_15", "16_17"])

# Stil dönüştürücü
style_map = {
    "Serbest": "serbest",
    "Sırtüstü": "sirtustu",
    "Kurbağalama": "kurbagalama",
    "Kelebek": "kelebek"
}
style_code = style_map[style]
gender_code = "kadin" if gender == "Kadın" else "erkek"

# Model dosya adı
model_filename = f"model1_{gender_code}_{age_group}_{style_code}_model.pkl"
model_path = os.path.join("model_dosyalar", model_filename)

# SHAP key
shap_key = f"{gender_code}_{age_group}_{style_code}"

# SHAP özelliği dosyasını yükle
shap_path = os.path.join("model_dosyalar", "shap_features_mapping.pkl")
try:
    with open(shap_path, "rb") as f:
        shap_features = pickle.load(f)
    selected_features = shap_features.get(shap_key, [])
except Exception as e:
    selected_features = []
    st.error("SHAP eşleme dosyası yüklenemedi / SHAP mapping file not found.")

# Girişler
user_inputs = []
if selected_features:
    if language == "English":
        st.subheader("Performance Features")
    else:
        st.subheader("Performansa Etkili 7 Özellik")
        
    for feature in selected_features:
        val = st.number_input(f"{feature}", value=0.0)
        user_inputs.append(val)

    if st.button("Tahmin Et / Predict"):
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            X_input = np.array([[age, height, weight, 0 if gender == "Kadın" else 1] + user_inputs])
            pred = model.predict(X_input)[0]
            st.success(f"Tahmini 50m süresi: {pred:.2f} saniye")
        except FileNotFoundError:
            st.error("Model dosyası bulunamadı / Model file not found.")
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
else:
    st.warning("SHAP verileri bulunamadı, tahmin yapılamıyor.")
