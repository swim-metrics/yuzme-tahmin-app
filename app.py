import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

# DİL SEÇİMİ
lang = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

# Başlık
if lang == "English":
    st.title("🏊 Swimming Performance Prediction")
else:
    st.title("🏊 50m Yüzme Performans Tahmini")

# Girişler
age = st.number_input("Yaş / Age", 10, 20, 13)
height = st.number_input("Boy (cm) / Height", 130, 210, 160)
weight = st.number_input("Kilo (kg) / Weight", 30, 120, 50)
gender = st.selectbox("Cinsiyet / Gender", ["Kadın", "Erkek"])
style = st.selectbox("Yüzme Stili / Stroke", ["Serbest", "Sırtüstü", "Kurbağalama", "Kelebek"])
age_group = st.selectbox("Yaş Grubu / Age Group", ["12_13", "14_15", "16_17"])

# Kodlar
style_map = {"Serbest": "serbest", "Sırtüstü": "sirtustu", "Kurbağalama": "kurbagalama", "Kelebek": "kelebek"}
gender_code = "kadin" if gender == "Kadın" else "erkek"
style_code = style_map[style]
model_key = f"{gender_code}_{age_group}_{style_code}"
model_filename = f"model1_{model_key}_model.pkl"
mapping_file = "shap_features_mapping.pkl"

# SHAP ile seçilen değişkenleri yükle
try:
    with open(mapping_file, "rb") as f:
        shap_map = pickle.load(f)
    selected_features = shap_map.get(model_key, [])
except:
    selected_features = []

if selected_features:
    if lang == "English":
        st.subheader("Enter performance test results below:")
    else:
        st.subheader("Lütfen aşağıdaki performans ölçümlerini girin:")

    input_features = []
    for feat in selected_features:
        val = st.number_input(f"{feat}", value=0.0)
        input_features.append(val)

    if st.button("Tahmin Et / Predict"):
        try:
            with open(model_filename, "rb") as f:
                model = pickle.load(f)

            # Veriyi hazırla
            X_input = np.array([[age, height, weight, 0 if gender == "Kadın" else 1] + input_features])
            y_pred = model.predict(X_input)

            if hasattr(model, "score"):
                y_true = model.predict(X_input)
                r2 = r2_score(y_true, y_pred)
                mae = mean_absolute_error(y_true, y_pred)
                rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            else:
                r2 = mae = rmse = 0.0

            if lang == "English":
                st.success(f"Predicted 50m time: {y_pred[0]:.2f} seconds")
                st.info(f"R² Score: {r2:.3f} | MAE: {mae:.3f} | RMSE: {rmse:.3f}")
            else:
                st.success(f"Tahmini 50m süresi: {y_pred[0]:.2f} saniye")
                st.info(f"R² Skoru: {r2:.3f} | MAE: {mae:.3f} | RMSE: {rmse:.3f}")
        except Exception as e:
            st.error(f"Model yükleme hatası: {e}")
else:
    st.warning("Bu kombinasyon için SHAP verisi bulunamadı.")