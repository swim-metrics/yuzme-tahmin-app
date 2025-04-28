import streamlit as st
import pickle
import numpy as np

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

def main():
    st.set_page_config(page_title="50m Swimming Time Prediction", layout="centered")

    language = st.radio("Select Language / Dil Seçiniz:", ("English", "Türkçe"))

    if language == "English":
        st.title("50m Swimming Time Prediction")
    else:
        st.title("50m Yüzme Süre Tahmini")

    gender = st.selectbox("{}".format("Gender (0 = Female, 1 = Male):" if language == "English" else "Cinsiyet (0 = Kadın, 1 = Erkek):"), [0, 1])
    age = st.number_input("{}".format("Age:" if language == "English" else "Yaş:"), min_value=5, max_value=100, value=15)
    weight = st.number_input("{}".format("Weight (kg):" if language == "English" else "Vücut Ağırlığı (kg):"), min_value=20, max_value=150, value=50)
    height = st.number_input("{}".format("Height (cm):" if language == "English" else "Boy Uzunluğu (cm):"), min_value=100, max_value=220, value=160)

    style = st.selectbox(
        "{}".format("Which Swimming Style do you want to predict?" if language == "English" else "Hangi Yüzme Stilinde Tahmin Yapmak İstersiniz?"),
        ("Serbest" if language == "Türkçe" else "Freestyle", "Sırtüstü" if language == "Türkçe" else "Backstroke", "Kurbağalama" if language == "Türkçe" else "Breaststroke", "Kelebek" if language == "Türkçe" else "Butterfly")
    )

    if (style == "Serbest" or style == "Freestyle") or (style == "Sırtüstü" or style == "Backstroke") or (style == "Kelebek" or style == "Butterfly"):
        hand_length = st.number_input("{}".format("Hand Length (cm):" if language == "English" else "El Uzunluğu (cm):"))
        vertical_jump = st.number_input("{}".format("Vertical Jump Height (cm):" if language == "English" else "Dikey Sıçrama Yüksekliği (cm):"))
        long_jump = st.number_input("{}".format("Standing Long Jump Distance (cm):" if language == "English" else "Ayakta Uzun Atlama Mesafesi (cm):"))
        bent_arm_hang = st.number_input("{}".format("Bent Arm Hang (s):" if language == "English" else "Bükülü Kol Asılı Kalma (s):"))
        situp_test = st.number_input("{}".format("Sit-up Test (repetitions in 1 min):" if language == "English" else "Bir Dakika Mekik Testi (tekrar):"))
        cooper_test = st.number_input("{}".format("12-Minute Cooper Test (m):" if language == "English" else "12 Dakika Cooper Koşusu (m):"))

        inputs = np.array([[gender, age, weight, height, hand_length, vertical_jump, long_jump, bent_arm_hang, situp_test, cooper_test]])

    elif style == "Kurbağalama" or style == "Breaststroke":
        foot_length = st.number_input("{}".format("Foot Length (cm):" if language == "English" else "Ayak Uzunluğu (cm):"))
        vertical_jump = st.number_input("{}".format("Vertical Jump Height (cm):" if language == "English" else "Dikey Sıçrama Yüksekliği (cm):"))
        long_jump = st.number_input("{}".format("Standing Long Jump Distance (cm):" if language == "English" else "Ayakta Uzun Atlama Mesafesi (cm):"))
        bent_arm_hang = st.number_input("{}".format("Bent Arm Hang (s):" if language == "English" else "Bükülü Kol Asılı Kalma (s):"))
        situp_test = st.number_input("{}".format("Sit-up Test (repetitions in 1 min):" if language == "English" else "Bir Dakika Mekik Testi (tekrar):"))
        ankle_flexibility = st.number_input("{}".format("Ankle Flexibility (degrees):" if language == "English" else "Ayak Bileği Plantar Esnekliği (derece):"))

        inputs = np.array([[gender, age, weight, height, foot_length, vertical_jump, long_jump, bent_arm_hang, situp_test, ankle_flexibility]])

    if st.button("{}".format("Predict Time / Süreyi Tahmin Et" if language == "English" else "Tahmini Süreyi Hesapla")):
        model = load_model(style)
        prediction = model.predict(inputs)

        if language == "English":
            st.success(f"Predicted 50m Swimming Time: {prediction[0]:.2f} seconds")
        else:
            st.success(f"50m Tahmini Yüzme Süreniz: {prediction[0]:.2f} saniye")

if __name__ == "__main__":
    main()
