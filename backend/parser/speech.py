# from piper import PiperVoice
# import sounddevice as sd

# ta = PiperVoice.load("backend/voices/ta_IN-medium.onnx")
# en = PiperVoice.load("backend/voices/en_US-medium.onnx")

# def speak(text, lang="ta"):
#     voice = ta if lang == "ta" else en

#     audio = voice.synthesize(text)
#     sd.play(audio.audio_float_array, audio.sample_rate)
#     sd.wait()