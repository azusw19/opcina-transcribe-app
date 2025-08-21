# Flask Transcribe App

Jednostavna web aplikacija za transkripciju audio datoteka pomoću **OpenAI Whisper** modela.  
Korisnici mogu učitati audio (`.mp3`, `.wav`), odabrati jezik i dobiti transkript koji mogu kopirati ili preuzeti.

---

## 🚀 Instalacija i pokretanje

1. Kloniraj repo:

```bash
git clone https://github.com/TVOJE_IME/flask-transcribe-app.git
cd flask-transcribe-app
Kreiraj i aktiviraj virtualno okruženje:

Windows (PowerShell / CMD):

bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate
macOS / Linux:

bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate
Instaliraj ovisnosti:

bash
Copy
Edit
pip install -r requirements.txt
Dodaj .env datoteku s OpenAI API ključem:

ini
Copy
Edit
OPENAI_API_KEY=sk-xxxx
Pokreni aplikaciju:

bash
Copy
Edit
python app.py
Aplikacija će biti dostupna na http://127.0.0.1:5000.

📦 Struktura projekta
csharp
Copy
Edit
flask-transcribe-app/
│
├── app.py                # Flask backend
├── requirements.txt      # Python ovisnosti
├── templates/            # HTML predlošci (frontend)
├── static/               # CSS, JS i slike
├── .gitignore            # Ignorirani fajlovi (env, venv, cache...)
└── README.md             # Ovaj dokument
🛡️ Napomena o privatnosti
API ključ se nikad ne push-a na GitHub — drži ga u .env.

Audio datoteke se obrađuju samo za generiranje transkripta i po potrebi brišu.

Limit učitavanja je 50 MB po datoteci.

✨ Planirana poboljšanja
Batch upload (više datoteka odjednom)

Export u .srt i .vtt (podnaslovi)

Sažetak i analiza transkripta

UI poboljšanja (drag & drop, dark mode)
