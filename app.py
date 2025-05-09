import streamlit as st
import pickle
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os

# Dil seçimi
language = st.sidebar.selectbox("Dil / Language", ["Türkçe", "English"])

# Başlık
st.title("🏊 50m Yüzme Performans Tahmini" if language == "Türkçe" else "🏊 Swimming Performance Prediction")

# Kullanıcı girişleri
age = st.number_input("Yaş / Age", 10, 20, 13)
height = st.number_input("Boy (cm) / Height", 130, 210, 160)
weight = st.number_input("Kilo (kg) / Weight", 30, 120, 50)
gender = st.selectbox("Cinsiyet / Gender", ["Kadın", "Erkek"])
style = st.selectbox("Yüzme Stili / Stroke", ["Serbest", "Sırtüstü", "Kurbağalama", "Kelebek"])
age_group = st.selectbox("Yaş Grubu / Age Group", ["12_13", "14_15", "16_17"])

# Kodlama
style_map = {"Serbest": "serbest", "Sırtüstü": "sirtustu", "Kurbağalama": "kurbagalama", "Kelebek": "kelebek"}
style_code = style_map[style]
gender_code = "kadin" if gender == "Kadın" else "erkek"
model_key = f"{gender_code}_{age_group}_{style_code}"
model_filename = f"model1_{model_key}_model.pkl"

# SHAP değişken eşlemesi
selected_features = []
try:
    with open("shap_features_mapping.pkl", "rb") as f:
        shap_map = pickle.load(f)
        selected_features = shap_map.get(model_key, [])
except:
    st.warning("SHAP verisi yüklenemedi / SHAP mapping file missing.")

# Giriş formu
input_values = []
if selected_features:
    st.subheader("Performans Ölçümleri / Performance Measurements")
    for feature in selected_features:
        val = st.number_input(feature, value=0.0)
        input_values.append(val)

    if st.button("Tahmin Et / Predict"):
        try:
            with open(model_filename, "rb") as f:
                model = pickle.load(f)

            X = np.array([[age, height, weight, 0 if gender == "Kadın" else 1] + input_values])
            y_pred = model.predict(X)

            r2 = r2_score(y_pred, y_pred)
            mae = mean_absolute_error(y_pred, y_pred)
            rmse = mean_squared_error(y_pred, y_pred, squared=False)

            if language == "Türkçe":
                st.success(f"Tahmini 50m süresi: {y_pred[0]:.2f} saniye")
                st.info(f"R²: {r2:.3f} | MAE: {mae:.3f} | RMSE: {rmse:.3f}")
            else:
                st.success(f"Predicted 50m time: {y_pred[0]:.2f} seconds")
                st.info(f"R²: {r2:.3f} | MAE: {mae:.3f} | RMSE: {rmse:.3f}")
        except Exception as e:
            st.error(f"Model yüklenemedi: {e}")
else:
    st.warning("Bu kombinasyon için giriş alanı bulunamadı / No entry section for this combination.")