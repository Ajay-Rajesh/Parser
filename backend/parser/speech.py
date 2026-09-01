from pathlib import Path
from piper import PiperVoice
import sounddevice as sd
import numpy as np

VOICE_DIR = Path(__file__).resolve().parent.parent / "Voices"

ta = PiperVoice.load(str(VOICE_DIR / "ta_IN-roja-medium.onnx"))
en = PiperVoice.load(str(VOICE_DIR / "en_GB-alan-medium.onnx"))

def speak(text, lang="ta"):
    voice = ta if lang == "ta" else en

    audio = []

    # synthesize() yields chunks
    for chunk in voice.synthesize(text):
        audio.extend(chunk.audio_int16_bytes)

    audio = np.frombuffer(bytes(audio), dtype=np.int16)
    audio = audio.astype(np.float32) / 32768.0

    sd.play(audio, 22050)
    sd.wait()