
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Başlık
st.set_page_config(page_title="Yüzme Performans Tahmin Uygulaması", layout="centered")

st.title("🏊‍♂️ Yüzme Performans Tahmini (50m)")
st.markdown("Bu uygulama yaş, boy, kilo, cinsiyet ve performans ölçümleri ile 50m yüzme süresini tahmin eder.")

# Sabit girişler
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Yaş", min_value=10, max_value=25, value=13)
    height = st.number_input("Boy (cm)", min_value=120, max_value=220, value=160)
with col2:
    weight = st.number_input("Kilo (kg)", min_value=30, max_value=120, value=50)
    gender = st.selectbox("Cinsiyet", options=["Kadın", "Erkek"])

# Stil ve yaş grubu seçimi
style = st.selectbox("Yüzme Stili", ["Serbest", "Sırtüstü", "Kurbağalama", "Kelebek"])
age_group = st.selectbox("Yaş Grubu", ["12_13", "14_15", "16_17"])

# Model adı oluştur
model_filename = f"model1_{'kadin' if gender=='Kadın' else 'erkek'}_{age_group}_{style.lower()}_model.pkl"
model_path = os.path.join("model_dosyalar", model_filename)

# SHAP eşleme dosyasını yükle
mapping_path = os.path.join("model_dosyalar", "shap_features_mapping.pkl")
try:
    with open(mapping_path, "rb") as f:
        shap_features = pickle.load(f)
except:
    st.error("SHAP eşleme dosyası bulunamadı.")
    st.stop()

# Model yükle
try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except:
    st.error(f"Model dosyası bulunamadı: {model_filename}")
    st.stop()

# SHAP girişleri
user_inputs = {}
st.subheader("📊 Performans Ölçümleri")
for feat in shap_features.get(model_filename, []):
    user_inputs[feat] = st.number_input(f"{feat}", value=0.0)

# Tahmin butonu
if st.button("Tahmin Et"):
    try:
        # Veri çerçevesi oluştur
        df_input = pd.DataFrame([{
            "Yaş": age,
            "Boy": height,
            "Kilo": weight,
            "Grup_Kod": 0 if gender == "Kadın" else 1,
            **user_inputs
        }])

        # Sıralama garantisi
        model_features = model.get_booster().feature_names
        df_input = df_input[model_features]

        # Tahmin
        prediction = model.predict(df_input)[0]
        st.success(f"Tahmini 50m Yüzme Süresi: {round(prediction, 2)} saniye")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
