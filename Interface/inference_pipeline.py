import os
import winsound
from gtts import gTTS
from pydub import AudioSegment
import whisper
from googletrans import Translator

import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

import threading
import os
from pydub import AudioSegment
import winsound

def play_audio(output_path):
    def _play():
        try:
            wav_path = output_path.replace('.mp3', '.wav')
            AudioSegment.from_mp3(output_path).export(wav_path, format='wav')
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
            os.remove(wav_path)
        except Exception as e:
            print(f"[❌ AUDIO ERROR] {e}")

    threading.Thread(target=_play, daemon=True).start()

def inference(audio_path, detected_lang, dest_lang, result_dir="results"):
    os.makedirs(result_dir, exist_ok=True)

    # Step 1: Transcribe
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=detected_lang.lower())
    transcription = result['text']

    # Step 2: Translate
    translator = Translator()
    translated = translator.translate(transcription, src=detected_lang.lower(), dest=dest_lang.lower())
    translated_text = translated.text

    # Step 3: Text-to-Speech
    tts = gTTS(text=translated_text, lang=dest_lang.lower())
    tts_filename = f"tts_{os.path.basename(audio_path).split('.')[0]}_{dest_lang}.mp3"
    output_path = os.path.join(result_dir, tts_filename)
    tts.save(output_path)

    return {
        "transcription": transcription,
        "translation": translated_text,
        "tts_path": output_path
    }
