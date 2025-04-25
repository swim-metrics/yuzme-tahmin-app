
import joblib
import pandas as pd

# Model dosyasını yükle
model = joblib.load("yuzme_model3_cinsiyetli.pkl")

print("🏊‍♀️ Cinsiyet Destekli Yüzme Final Süresi Tahmini (Model 3)")
print("Lütfen aşağıdaki bilgileri giriniz:")

# Giriş verilerini al
try:
    age = int(input("Yaş: "))
    height = float(input("Boy (cm): "))
    reaction = float(input("Reaksiyon Süresi (s): "))
    split_50 = float(input("50m Split Süresi (s): "))
    gender_input = input("Cinsiyet (Erkek/Kadın): ").strip().lower()

    if gender_input in ["erkek", "e", "m"]:
        gender_code = 0
    elif gender_input in ["kadın", "k", "f"]:
        gender_code = 1
    else:
        print("❌ Geçersiz cinsiyet girdiniz. Erkek ya da Kadın girilmeli.")
        exit()

    # Veri çerçevesi oluştur
    new_data = pd.DataFrame([{
        "Age": age,
        "Height": height,
        "ReactionTime": reaction,
        "Split_50m": split_50,
        "Gender_Code": gender_code
    }])

    # Tahmin yap
    predicted_time = model.predict(new_data)[0]
    print(f"✅ Tahmini 100m Final Süresi: {predicted_time:.2f} saniye")

except Exception as e:
    print(f"❌ Hata oluştu: {e}")
