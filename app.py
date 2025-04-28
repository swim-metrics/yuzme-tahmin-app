import streamlit as st
import pickle
import numpy as np

# --- Başlık ---
st.set_page_config(page_title="Swimming Time Prediction", page_icon="🏊", layout="centered")
st.title("50m Swimming Time Prediction")

# --- Dil Seçimi ---
language = st.radio("Select Language / Dil Seçiniz:", ("English", "Türkçe"))

if language == "English":
    gender = st.selectbox("Gender (0 = Female, 1 = Male):", [0, 1])
    age = st.number_input("Age:", min_value=10, max_value=30, value=15)
    weight = st.number_input("Weight (kg):", min_value=30, max_value=120, value=50)
    height = st.number_input("Height (cm):", min_value=120, max_value=210, value=160)

    style = st.selectbox("Which Style Do You Want to Predict?", ["Freestyle", "Backstroke", "Breaststroke", "Butterfly"])

else:
    gender = st.selectbox("Cinsiyet (0 = Kadın, 1 = Erkek):", [0, 1])
    age = st.number_input("Yaş:", min_value=10, max_value=30, value=15)
    weight = st.number_input("Kilo (kg):", min_value=30, max_value=120, value=50)
    height = st.number_input("Boy Uzunluğu (cm):", min_value=120, max_value=210, value=160)

    style = st.selectbox("Hangi Stilde Tahmin Yapmak İstiyorsunuz?", ["Serbest", "Sırtüstü", "Kurbağalama", "Kelebek"])

# --- Ölçümleri Stil Seçimine Göre Alalım ---
inputs = []

if style in ["Freestyle", "Serbest"]:
    hand_length = st.number_input("Hand Length (cm):", value=18.0)
    vertical_jump = st.number_input("Vertical Jump (cm):", value=35)
    standing_long_jump = st.number_input("Standing Long Jump (cm):", value=160)
    bent_arm_hang = st.number_input("Bent Arm Hang (s):", value=15)
    situp_test = st.number_input("Sit-up Test (1 min repetition):", value=30)
    cooper_test = st.number_input("Cooper Test (meter):", value=1600)
    inputs = [gender, age, weight, height, hand_length, vertical_jump, standing_long_jump, bent_arm_hang, situp_test, cooper_test]

elif style in ["Backstroke", "Sırtüstü"]:
    hand_length = st.number_input("Hand Length (cm):", value=18.0)
    chest_circumference = st.number_input("Chest Circumference (cm):", value=85)
    standing_long_jump = st.number_input("Standing Long Jump (cm):", value=160)
    handgrip_strength = st.number_input("Handgrip Strength (kg):", value=40)
    situp_test = st.number_input("Sit-up Test (1 min repetition):", value=30)
    sit_reach_test = st.number_input("Sit and Reach Test (cm):", value=30)
    ankle_flexibility = st.number_input("Ankle Flexibility (degree):", value=90)
    inputs = [gender, age, weight, hand_length, chest_circumference, standing_long_jump, handgrip_strength, situp_test, sit_reach_test, ankle_flexibility]

elif style in ["Breaststroke", "Kurbağalama"]:
    foot_length = st.number_input("Foot Length (cm):", value=25.0)
    vertical_jump = st.number_input("Vertical Jump (cm):", value=35)
    standing_long_jump = st.number_input("Standing Long Jump (cm):", value=160)
    handgrip_strength = st.number_input("Handgrip Strength (kg):", value=40)
    bent_arm_hang = st.number_input("Bent Arm Hang (s):", value=15)
    situp_test = st.number_input("Sit-up Test (1 min repetition):", value=30)
    shoulder_flexibility = st.number_input("Shoulder Flexibility (cm):", value=30)
    inputs = [gender, age, weight, foot_length, vertical_jump, standing_long_jump, handgrip_strength, bent_arm_hang, situp_test, shoulder_flexibility]

elif style in ["Butterfly", "Kelebek"]:
    hand_length = st.number_input("Hand Length (cm):", value=18.0)
    vertical_jump = st.number_input("Vertical Jump (cm):", value=35)
    standing_long_jump = st.number_input("Standing Long Jump (cm):", value=160)
    bent_arm_hang = st.number_input("Bent Arm Hang (s):", value=15)
    shoulder_flexibility = st.number_input("Shoulder Flexibility (cm):", value=30)
    cooper_test = st.number_input("Cooper Test (meter):", value=1600)
    inputs = [gender, age, weight, height, hand_length, vertical_jump, standing_long_jump, bent_arm_hang, shoulder_flexibility, cooper_test]

# --- Tahmin ---
if st.button("Predict Time / Süreyi Tahmin Et"):
    try:
        # Modeli yükle
        if style in ["Freestyle", "Serbest"]:
            model = pickle.load(open("serbest_model.pkl", "rb"))
        elif style in ["Backstroke", "Sırtüstü"]:
            model = pickle.load(open("sirtustu_model.pkl", "rb"))
        elif style in ["Breaststroke", "Kurbağalama"]:
            model = pickle.load(open("kurbagalama_model.pkl", "rb"))
        elif style in ["Butterfly", "Kelebek"]:
            model = pickle.load(open("kelebek_model.pkl", "rb"))

        prediction = model.predict(np.array(inputs).reshape(1, -1))
        st.success(f"Predicted 50m Swimming Time: {prediction[0]:.2f} seconds / saniye")

    except Exception as e:
        st.error(f"An error occurred: {e}")
