import os
import numpy as np
import librosa
import webrtcvad
import joblib
import tempfile
from sklearn.preprocessing import StandardScaler
from pydub import AudioSegment
from scipy.io.wavfile import write as wav_write

# Silence Removal
def remove_silence(audio, sr=16000, aggressiveness=3, frame_duration=30):
    vad = webrtcvad.Vad(aggressiveness)
    frame_len = int(sr * frame_duration / 1000)
    offset = 0
    voiced = []

    while offset + frame_len < len(audio):
        frame = audio[offset:offset + frame_len]
        pcm = (frame * 32768).astype(np.int16).tobytes()
        if vad.is_speech(pcm, sample_rate=sr):
            voiced.extend(frame)
        offset += frame_len

    return np.array(voiced)

# Feature Extraction
def extract_features(file_path, sr=16000, n_mfcc=13):
    y, _ = librosa.load(file_path, sr=sr)
    y_clean = remove_silence(y, sr=sr)

    if len(y_clean) == 0:
        return np.zeros((1, n_mfcc * 3))

    mfcc = librosa.feature.mfcc(y=y_clean, sr=sr, n_mfcc=n_mfcc)
    delta = librosa.feature.delta(mfcc)
    delta2 = librosa.feature.delta(mfcc, order=2)
    mfcc_all = np.vstack([mfcc, delta, delta2])

    # CMVN
    mfcc_all = (mfcc_all - np.mean(mfcc_all, axis=1, keepdims=True)) / (np.std(mfcc_all, axis=1, keepdims=True) + 1e-10)

    return mfcc_all.T

# Convert to WAV if needed
def convert_to_wav(input_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.wav':
        return input_path  # already a wav file

    # Convert to wav using pydub
    audio = AudioSegment.from_file(input_path)
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio.set_frame_rate(16000).set_channels(1).export(temp_wav.name, format="wav")
    return temp_wav.name

# Main Detection Function
def detect_language(audio_path, model_dir="gmm_models"):
    wav_path = convert_to_wav(audio_path)
    features = extract_features(wav_path)

    models = {
        # "Arabic": joblib.load(os.path.join(model_dir, "Arabic_gmm_512.joblib")),
        # "Darija": joblib.load(os.path.join(model_dir, "Darija_gmm_512.joblib")),
        # "English": joblib.load(os.path.join(model_dir, "English_gmm_512.joblib")),
        # "Spanish": joblib.load(os.path.join(model_dir, "Spanish_gmm_512.joblib")),
        # "French": joblib.load(os.path.join(model_dir, "French_gmm_512.joblib")),
        # "Korean": joblib.load(os.path.join(model_dir, "Korean_gmm_512.joblib")),
        # "Spanish": joblib.load(os.path.join(model_dir, "Spanish_gmm_512.joblib")),

        "Arabic": joblib.load(os.path.join(model_dir, "Arabic_gmm_1024.joblib")),
        "Spanish": joblib.load(os.path.join(model_dir, "Spanish_gmm_1024.joblib")),
        "English": joblib.load(os.path.join(model_dir, "English_gmm_1024.joblib")),
        "Spanish": joblib.load(os.path.join(model_dir, "Spanish_gmm_1024.joblib")),

    }

    scores = {lang: model.score(features) for lang, model in models.items()}
    predicted_language = max(scores, key=scores.get)

    return predicted_language
