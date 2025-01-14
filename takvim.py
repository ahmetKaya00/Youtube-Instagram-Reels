from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
from twilio.rest import Client

# Twilio ayarları
account_sid = 'account_sid'
auth_token = 'auth_token'
client = Client(account_sid, auth_token)

# Kimlik doğrulama ve yetkilendirme için JSON dosyası
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
credentials_path = 'data/client_secret.json'  # JSON dosyasının doğru yolu

# Google Calendar API hizmetini oluşturma
def get_google_calendar_service():
    try:
        # Kimlik doğrulama işlemi
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Token'i saklama
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"Hizmet oluşturulurken bir hata oluştu: {e}")
        return None

# Google Takvim API'sinden doğum günü bilgilerini kontrol etme
def check_birthdays():
    service = get_google_calendar_service()
    if not service:
        print("Takvim hizmeti oluşturulamadı.")
        return

    try:
        now = datetime.utcnow().isoformat() + 'Z'  # Şu anki zamanı al
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print("Yaklaşan etkinlik yok.")
            return

        for event in events:
            if "doğum günü" in event['summary'].lower():  # "Doğum Günü" olan etkinlikler
                send_birthday_sms(event['summary'])
    except Exception as e:
        print(f"Etkinlikler kontrol edilirken bir hata oluştu: {e}")

# SMS gönderme fonksiyonu
def send_birthday_sms(event_name):
    try:
        message = client.messages.create(
            body=f"Bugün {event_name}! Hemen kutlama yapmayı unutma! 🎉🥳",
            from_='+123456789',  # Twilio numaranız
            to='+90123456789'      # Alıcı numarası
        )
        print(f"SMS gönderildi: {message.sid}")
    except Exception as e:
        print(f"SMS gönderilirken bir hata oluştu: {e}")

# Doğum günlerini kontrol et
if __name__ == "__main__":
    check_birthdays()
