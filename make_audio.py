from gtts import gTTS

text = "Dobar dan! Ovo je probna audio datoteka za testiranje transkripcije. dinamo zagreb reka san ja moja firma"
tts = gTTS(text, lang="hr")
tts.save("croatian_test.mp3")

print("✅ Generated croatian_test.mp3")
