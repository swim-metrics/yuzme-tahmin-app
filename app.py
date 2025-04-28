import streamlit as st
import pickle
import numpy as np

# Model yükleme fonksiyonu
def load_model(style):
    models = {
        "Serbest": "serbest_model.pkl",
        "Sırtüstü": "sirtustu_model.pkl",
        "Kurbağalama": "kurbagalama_model.pkl",
        "Kelebek": "kelebek_model.pkl",
        "Freestyle": "serbest_model.pkl",
        "Backstroke": "sirtustu_model.pkl",
        "Breaststroke": "kurbagalama_model.pkl",
        "Butterfly": "kelebek_model.pkl"
    }
    model_path = models.get(style)
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Ana uygulama fonksiyonu
def main():
    st.set_page_config(page_title="50m Swimming Time Prediction", layout="centered")

    # Dil seçimi
    language = st.radio("Select Language / Dil Seçiniz:", ("English", "Türkçe"))

    # Sayfa başlığı
    if language == "English":
        st.title("50m Swimming Time Prediction")
    else:
        st.title("50m Yüzme Süre Tahmini")

    # Temel bilgiler
    gender = st.selectbox("{}".format("Gender (0 = Female, 1 = Male):" if language == "English" else "Cinsiyet (0 = Kadın, 1 = Erkek):"), [0, 1])
    age = st.number_input("{}".format("Age:" if language == "English" else "Yaş:"), min_value=5, max_value=100, value=15)
    weight = st.number_input("{}".format("Weight (kg):" if language == "English" else "Vücut Ağırlığı (kg):"), min_value=20, max_value=150, value=50)
    height = st.number_input("{}".format("Height (cm):" if language == "English" else "Boy Uzunluğu (cm):"), min_value=100, max_value=220, value=160)

    # Stil seçimi
    style = st.selectbox(
        "{}".format("Which Swimming Style do you want to predict?" if language == "English" else "Hangi Yüzme Stilinde Tahmin Yapmak İstersiniz?"),
        ("Serbest" if language == "Türkçe" else "Freestyle", "Sırtüstü" if language == "Türkçe" else "Backstroke", "Kurbağalama" if language == "Türkçe" else "Breaststroke", "Kelebek" if language == "Türkçe" else "Butterfly")
    )

    # Stil bazlı ölçüm girişleri
    inputs = []

    if style in ("Serbest", "Freestyle"):
        hand_length = st.number_input("{}".format("Hand Length (cm):" if language == "English" else "El Uzunluğu (cm):"))
        vertical_jump = st.number_input("{}".format("Vertical Jump Height (cm):" if language == "English" else "Dikey Sıçrama Yüksekliği (cm):"))
        standing_long_jump = st.number_input("{}".format("Standing Long Jump Distance (cm):" if language == "English" else "Ayakta Uzun Atlama Mesafesi (cm):"))
        bent_arm_hang = st.number_input("{}".format("Bent Arm Hang Duration (seconds):" if language == "English" else "Bükülü Kol Asılı Kalma Süreti (saniye):"))
        situp_test = st.number_input("{}".format("1-Minute Sit-up Test (repetitions):" if language == "English" else "1 Dakikalık Mekik Testi (tekrar):"))
        cooper_test = st.number_input("{}".format("12-Minute Cooper Test (meters):" if language == "English" else "12 Dakikalık Cooper Koşu Testi (metre):"))
        inputs = [gender, age, weight, height, hand_length, vertical_jump, standing_long_jump, bent_arm_hang, situp_test, cooper_test]

    elif style in ("Sırtüstü", "Backstroke"):
        hand_length = st.number_input("{}".format("Hand Length (cm):" if language == "English" else "El Uzunluğu (cm):"))
        chest_circumference = st.number_input("{}".format("Chest Circumference (cm):" if language == "English" else "Göğüs Çevresi (cm):"))
        standing_long_jump = st.number_input("{}".format("Standing Long Jump Distance (cm):" if language == "English" else "Ayakta Uzun Atlama Mesafesi (cm):"))
        handgrip_strength = st.number_input("{}".format("Handgrip Strength (kg):" if language == "English" else "El Kavrama Gücü (kg):"))
        situp_test = st.number_input("{}".format("1-Minute Sit-up Test (repetitions):" if language == "English" else "1 Dakikalık Mekik Testi (tekrar):"))
        sit_reach_test = st.number_input("{}".format("Sit and Reach Test (cm):" if language == "English" else "Belden Öne Uzanma Testi (cm):"))
        ankle_flexibility = st.number_input("{}".format("Ankle Plantar Flexibility (degrees):" if language == "English" else "Ayak Bileği Plantar Esnekliği (derece):"))
        inputs = [gender, age, weight, hand_length, chest_circumference, standing_long_jump, handgrip_strength, situp_test, sit_reach_test, ankle_flexibility]

    elif style in ("Kurbağalama", "Breaststroke"):
        foot_length = st.number_input("{}".format("Foot Length (cm):" if language == "English" else "Ayak Uzunluğu (cm):"))
        vertical_jump = st.number_input("{}".format("Vertical Jump Height (cm):" if language == "English" else "Dikey Sıçrama Yüksekliği (cm):"))
        standing_long_jump = st.number_input("{}".format("Standing Long Jump Distance (cm):" if language == "English" else "Ayakta Uzun Atlama Mesafesi (cm):"))
        handgrip_strength = st.number_input("{}".format("Handgrip Strength (kg):" if language == "English" else "El Kavrama Gücü (kg):"))
        bent_arm_hang = st.number_input("{}".format("Bent Arm Hang Duration (seconds):" if language == "English" else "Bükülü Kol Asılı Kalma Süreti (saniye):"))
        situp_test = st.number_input("{}".format("1-Minute Sit-up Test (repetitions):" if language == "English" else "1 Dakikalık Mekik Testi (tekrar):"))
        shoulder_flexibility = st.number_input("{}".format("Shoulder Flexibility Test (cm):" if language == "English" else "Omuz Esnekliği Testi (cm):"))
        inputs = [gender, age, weight, foot_length, vertical_jump, standing_long_jump, handgrip_strength, bent_arm_hang, situp_test, shoulder_flexibility]

    elif style in ("Kelebek", "Butterfly"):
        hand_length = st.number_input("{}".format("Hand Length (cm):" if language == "English" else "El Uzunluğu (cm):"))
        vertical_jump = st.number_input("{}".format("Vertical Jump Height (cm):" if language == "English" else "Dikey Sıçrama Yüksekliği (cm):"))
        standing_long_jump = st.number_input("{}".format("Standing Long Jump Distance (cm):" if language == "English" else "Ayakta Uzun Atlama Mesafesi (cm):"))
        bent_arm_hang = st.number_input("{}".format("Bent Arm Hang Duration (seconds):" if language == "English" else "Bükülü Kol Asılı Kalma Süreti (saniye):"))
        shoulder_flexibility = st.number_input("{}".format("Shoulder Flexibility Test (cm):" if language == "English" else "Omuz Esnekliği Testi (cm):"))
        cooper_test = st.number_input("{}".format("12-Minute Cooper Test (meters):" if language == "English" else "12 Dakikalık Cooper Koşu Testi (metre):"))
        inputs = [gender, age, weight, height, hand_length, vertical_jump, standing_long_jump, bent_arm_hang, shoulder_flexibility, cooper_test]

    # Tahmin butonu
    if st.button("{}".format("Predict Swimming Time" if language == "English" else "Yüzme Süre Tahmin Et")):
        try:
            model = load_model(style)
            prediction = model.predict(np.array(inputs).reshape(1, -1))
            if language == "English":
                st.success(f"Predicted 50m Swimming Time: {prediction[0]:.2f} seconds")
            else:
                st.success(f"Tahmini 50m Yüzme Süretiniz: {prediction[0]:.2f} saniye")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
