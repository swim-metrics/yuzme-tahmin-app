import streamlit as st
import pickle
import numpy as np

# Modeli yukleme fonksiyonu
def load_model(style):
    model_path = f"{style.lower()}_model.pkl"
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    return model

def main():
    st.set_page_config(page_title="50m Swimming Time Prediction", page_icon="🏊")

    # Dil Seçimi
    language = st.radio("Select Language / Dil Seçiniz:", ("English", "Türkçe"))

    # Başlık
    if language == "Türkçe":
        st.title("50m Yüzme Süre Tahmini")
    else:
        st.title("50m Swimming Time Prediction")

    # Ortak alanlar
    gender = st.selectbox("Cinsiyet (0 = Kadın, 1 = Erkek):" if language == "Türkçe" else "Gender (0 = Female, 1 = Male):", [0,1])
    age = st.number_input("Yaş:" if language == "Türkçe" else "Age:", min_value=5, max_value=100, value=15)
    weight = st.number_input("Vücut Ağırlığı (kg):" if language == "Türkçe" else "Weight (kg):", min_value=20, max_value=200, value=50)
    height = st.number_input("Boy Uzunluğu (cm):" if language == "Türkçe" else "Height (cm):", min_value=100, max_value=220, value=160)

    # Stil Seçimi
    if language == "Türkçe":
        style = st.selectbox("Hangi Yüzme Stilinde Tahmin Yapmak İstersiniz?", ("Serbest", "Sırtüstü", "Kurbagalama", "Kelebek"))
    else:
        style = st.selectbox("Which Swimming Style Do You Want to Predict?", ("Freestyle", "Backstroke", "Breaststroke", "Butterfly"))

    # Ölçüm Verileri
    if style in ["Serbest", "Freestyle"]:
        hand_length = st.number_input("El Uzunluğu (cm):" if language == "Türkçe" else "Hand Length (cm):", value=18.0)
        vertical_jump = st.number_input("Dikey Sıçrama Yüksekliği (cm):" if language == "Türkçe" else "Vertical Jump Height (cm):", value=35)
        standing_long_jump = st.number_input("Ayakta Uzun Atlama Mesafesi (cm):" if language == "Türkçe" else "Standing Long Jump Distance (cm):", value=160)
        bent_arm_hang = st.number_input("Bükülü Kol Asılı Kalma (s):" if language == "Türkçe" else "Bent Arm Hang (s):", value=20)
        situp_test = st.number_input("Bir Dakikada Mekik Testi (tekrar):" if language == "Türkçe" else "Sit-up Test (reps):", value=30)
        cooper_test = st.number_input("12 Dakika Cooper Koşusu (m):" if language == "Türkçe" else "12-Minute Cooper Test (m):", value=1600)

        input_data = np.array([[gender, age, weight, height, hand_length, vertical_jump, standing_long_jump, bent_arm_hang, situp_test, cooper_test]])

    elif style in ["Sırtüstü", "Backstroke"]:
        hand_length = st.number_input("El Uzunluğu (cm):" if language == "Türkçe" else "Hand Length (cm):", value=18.0)
        chest_circumference = st.number_input("Göğüs Çevresi (cm):" if language == "Türkçe" else "Chest Circumference (cm):", value=85)
        standing_long_jump = st.number_input("Ayakta Uzun Atlama Mesafesi (cm):" if language == "Türkçe" else "Standing Long Jump Distance (cm):", value=160)
        bent_arm_hang = st.number_input("Bükülü Kol Asılı Kalma (s):" if language == "Türkçe" else "Bent Arm Hang (s):", value=20)
        shoulder_flexibility = st.number_input("Omuz Esnekliği (cm):" if language == "Türkçe" else "Shoulder Flexibility (cm):", value=30)
        ankle_flexibility = st.number_input("Ayak Bileği Esnekliği (derece):" if language == "Türkçe" else "Ankle Flexibility (degree):", value=90)

        input_data = np.array([[gender, age, weight, height, hand_length, chest_circumference, standing_long_jump, bent_arm_hang, shoulder_flexibility, ankle_flexibility]])

    elif style in ["Kurbagalama", "Breaststroke"]:
        foot_length = st.number_input("Ayak Uzunluğu (cm):" if language == "Türkçe" else "Foot Length (cm):", value=22)
        vertical_jump = st.number_input("Dikey Sıçrama Yüksekliği (cm):" if language == "Türkçe" else "Vertical Jump Height (cm):", value=30)
        standing_long_jump = st.number_input("Ayakta Uzun Atlama Mesafesi (cm):" if language == "Türkçe" else "Standing Long Jump Distance (cm):", value=160)
        bent_arm_hang = st.number_input("Bükülü Kol Asılı Kalma (s):" if language == "Türkçe" else "Bent Arm Hang (s):", value=20)
        situp_test = st.number_input("Bir Dakikada Mekik Testi (tekrar):" if language == "Türkçe" else "Sit-up Test (reps):", value=30)
        cooper_test = st.number_input("12 Dakika Cooper Koşusu (m):" if language == "Türkçe" else "12-Minute Cooper Test (m):", value=1600)

        input_data = np.array([[gender, age, weight, height, foot_length, vertical_jump, standing_long_jump, bent_arm_hang, situp_test, cooper_test]])

    elif style in ["Kelebek", "Butterfly"]:
        hand_length = st.number_input("El Uzunluğu (cm):" if language == "Türkçe" else "Hand Length (cm):", value=18.0)
        vertical_jump = st.number_input("Dikey Sıçrama Yüksekliği (cm):" if language == "Türkçe" else "Vertical Jump Height (cm):", value=35)
        standing_long_jump = st.number_input("Ayakta Uzun Atlama Mesafesi (cm):" if language == "Türkçe" else "Standing Long Jump Distance (cm):", value=160)
        bent_arm_hang = st.number_input("Bükülü Kol Asılı Kalma (s):" if language == "Türkçe" else "Bent Arm Hang (s):", value=20)
        shoulder_flexibility = st.number_input("Omuz Esnekliği (cm):" if language == "Türkçe" else "Shoulder Flexibility (cm):", value=30)
        cooper_test = st.number_input("12 Dakika Cooper Koşusu (m):" if language == "Türkçe" else "12-Minute Cooper Test (m):", value=1600)

        input_data = np.array([[gender, age, weight, height, hand_length, vertical_jump, standing_long_jump, bent_arm_hang, shoulder_flexibility, cooper_test]])

    # Tahmin Butonu
    if st.button("Süreyi Tahmin Et" if language == "Türkçe" else "Predict Time"):
        try:
            model = load_model(style.split(" ")[0])  # stil adından ilk kelimeyi al
            prediction = model.predict(input_data)

            if language == "Türkçe":
                st.success(f"50m Yüzme Süre Tahmininiz: {prediction[0]:.2f} saniye")
            else:
                st.success(f"Predicted 50m Swimming Time: {prediction[0]:.2f} seconds")

        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
