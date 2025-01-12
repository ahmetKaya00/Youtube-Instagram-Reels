import requests
from twilio.rest import Client
import schedule
import time

# OpenWeatherMap API bilgileri
API_KEY = "OpenWeatherMap_API"  # OpenWeatherMap API anahtarı
CITY = "Mersin"  # Şehrinizi buraya yazın

# Twilio API bilgileri
TWILIO_ACCOUNT_SID = "Twilio_Account_SID"  # Twilio Account SID
TWILIO_AUTH_TOKEN = "Twilio_Auth_Token"    # Twilio Auth Token
TWILIO_PHONE_NUMBER = "+123456789"             # Twilio'dan aldığınız numara
TO_PHONE_NUMBER = "+90123456789"                 # SMS'in gönderileceği telefon numarası

# Hava durumu alma fonksiyonu
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temperature = data['main']['temp']
        weather = data['weather'][0]['description']
        return temperature, weather
    else:
        print("Hava durumu verisi alınamadı!")
        return None, None

# Öneri oluşturma fonksiyonu
def get_recommendations(temperature, weather):
    if temperature < 10:
        clothing = "Kalın bir mont, atkı ve eldiven giyin."
        food = "Sıcak bir çorba içmeyi düşünebilirsiniz."
        activity = "Evde bir film izleyebilir veya kitap okuyabilirsiniz."
    elif 10 <= temperature < 20:
        clothing = "Hafif bir mont ya da kazak giyin."
        food = "Sıcak çay ve hafif yemekler iyi gider."
        activity = "Açık havada yürüyüş yapmayı deneyin."
    else:
        clothing = "T-shirt ve rahat kıyafetler tercih edin."
        food = "Serinletici içecekler ve hafif yemekler iyi olur."
        activity = "Parkta zaman geçirebilir ya da bisiklet sürebilirsiniz."
    return clothing, food, activity

# SMS gönderim fonksiyonu
def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print("SMS başarıyla gönderildi!")
    except Exception as e:
        print(f"SMS gönderiminde hata oluştu: {e}")

# Günlük hatırlatıcı
def daily_reminder():
    temperature, weather = get_weather()
    if temperature and weather:
        clothing, food, activity = get_recommendations(temperature, weather)
        message = (f"Günaydın Ahmet Kaya"
                   f"Hava Durumu: {weather}, {temperature}°C\n"
                   f"👕 Ne Giymelisin: {clothing}\n"
                   f"🍲 Ne Yemelisin: {food}\n"
                   f"🎮 Akşam Ne Yapmalısın: {activity}")
        send_sms(message)
    else:
        send_sms("Bugün hava durumu bilgisi alınamadı. Planlarınızı kontrol edin!")

# Hatırlatıcıyı her gün saat 12:00'de çalıştır
schedule.every().day.at("11:25").do(daily_reminder)

# Sürekli çalıştırma döngüsü
while True:
    schedule.run_pending()
    time.sleep(1)
