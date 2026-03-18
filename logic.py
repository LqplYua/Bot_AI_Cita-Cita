import requests
import json

GEMINI_API_KEY = 'ISI SENDIRI'

class GeminiAPI():
    def __init__(self, api_key):
        self.api_key = api_key
        self.model_path = self._get_available_model()

    def _get_available_model(self):
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
        try:
            res = requests.get(list_url)
            if res.status_code == 200:
                models = res.json().get('models', [])
                for m in models:
                    if 'generateContent' in m.get('supportedGenerationMethods', []):
                        return m['name']
            return None
        except:
            return None

    def analisa_cita_cita(self, hobi_user):
        if not self.model_path:
            return "Koneksi ke otak AI terputus."

        # Prompt khusus untuk konsultasi cita-cita
        prompt = (
            f"Seseorang memiliki hobi atau kesukaan: '{hobi_user}'. "
            "Sebutkan 1 cita-cita atau profesi masa depan yang paling cocok untuknya. "
            "Berikan alasan mengapa itu cocok dan berikan satu kalimat motivasi yang keren. "
            "Format jawaban: \n"
            "🌟 *Profesi:* [Nama Profesi]\n"
            "🤔 *Kenapa Cocok?* [Alasan singkat]\n"
            "🚀 *Motivasi:* [Kalimat penyemangat]"
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model_path}:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            return "Maaf, AI sedang sibuk. Coba lagi nanti."
        except:
            return "Terjadi kesalahan pada server AI."

# Inisialisasi objek agar bisa dipanggil oleh main1.py
gemini_api = GeminiAPI(GEMINI_API_KEY)