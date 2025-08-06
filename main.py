import os, json
from pathlib import Path
from google.cloud import texttospeech
from epitran import Epitran

ROOT         = Path("cp mkdir storage/emulated/0/Dokumente")
BLOCKS_DIR   = ROOT / "blocks"
AUDIO_DIR    = ROOT / "audio"
LEXICON_FILE = ROOT / "lexicon.json"

tts_client = texttospeech.TextToSpeechClient()
epi        = Epitran("deu-Latn")

def ipa(word):
    return epi.transliterate(word)

def synthesize(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="de-DE", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_cfg = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    return tts_client.synthesize_speech(input_text, voice, audio_cfg).audio_content

def process_block(n, lex):
    path = BLOCKS_DIR / f"block_{n:03d}.txt"
    if not path.exists():
        return
    words = path.read_text(encoding="utf8").splitlines()
    for w in words:
        token = w[::-1]
        if token in lex:
            continue
        data = {
            "deutsch": w,
            "ipa": ipa(w),
            "bedeutung": f"Bedeutung von {w}",
            "bedeutung_rev": f"{w[::-1]} als Symbol",
            "pos": "Substantiv",
            "audio": ""
        }
        wav_path = AUDIO_DIR / f"{token}.wav"
        wav_path.write_bytes(synthesize(token))
        data["audio"] = f"file://{wav_path}"
        lex[token] = data

def run():
    AUDIO_DIR.mkdir(exist_ok=True)
    lex = {}
    for n in range(1, 1000):
        process_block(n, lex)
    LEXICON_FILE.write_text(json.dumps(lex, indent=2, ensure_ascii=False), encoding="utf8")

if __name__ == "__main__":
    run()
