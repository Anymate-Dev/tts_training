from faster_whisper import WhisperModel

model = WhisperModel('/home/anymate/project/tts_training/data/script/faster-whisper-large-v3', device="cuda", compute_type="float16")

segments, info = model.transcribe("/home/anymate/project/GPT-SoVITS/raw_data/game_filtered_data/zh/Abeiduo/vo_ABDLQ002_4_albedo_02.wav", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))