import os
import logging
from shutil import copy2, rmtree
from pydub import AudioSegment
from faster_whisper import WhisperModel
from pydub import AudioSegment
from pydub.silence import detect_silence

# Add this constant
MIN_DURATION = 6000
MAX_DURATION = 10000
MAX_SILENCE_DURATION = 2500  # 2.5 seconds in milliseconds

MAX_FILES_PER_PERSON = 30
WHISPER_MODEL_PATH = '/home/anymate/project/tts_training/data/script/faster-whisper-large-v3'

# Initialize logging and Whisper model
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
model = WhisperModel(WHISPER_MODEL_PATH, device="cuda", compute_type="float16")

def delete_existing_target_data(target_dir):
    if os.path.exists(target_dir):
        logging.info(f"Deleting existing data in {target_dir}")
        rmtree(target_dir)
    else:
        logging.info(f"No existing data found in {target_dir}")

def audio_to_text(audio_path):
    segments, _ = model.transcribe(audio_path, beam_size=5)
    return ''.join(segment.text for segment in segments)

def process_audio_file(file_path, target_path, language):
    audio = AudioSegment.from_wav(file_path)
    duration = len(audio)

    if MIN_DURATION <= duration <= MAX_DURATION:
        # Detect silence
        silence_chunks = detect_silence(audio, min_silence_len=MAX_SILENCE_DURATION, silence_thresh=-40)
        
        if not silence_chunks:
            logging.info(f"Processing: {file_path} with duration {duration}ms")
            file_name = os.path.basename(file_path)
            target_file_path = os.path.join(target_path, file_name)
            
            copy2(file_path, target_file_path)
            
            if language == 'en':
                text = audio_to_text(file_path)
                logging.info(f"Generated text: {text}")
                
                txt_file_path = target_file_path.replace('.wav', '.lab')
                with open(txt_file_path, 'w') as f:
                    f.write(text)
                return True
            elif language == 'zh':
                lab_file = file_path.replace('.wav', '.lab')
                if os.path.exists(lab_file):
                    copy2(lab_file, target_path)
                return True
        else:
            logging.info(f"Skipping {file_path} due to long silence periods")
    
    return False

def filter_files(source_dir, target_dir):


    for language in ['en', 'zh']:
        lang_path = os.path.join(source_dir, language)
        logging.info(f"Processing language: {language}")
        
        for person in os.listdir(lang_path):
            person_path = os.path.join(lang_path, person)
            if not os.path.isdir(person_path):
                continue

            logging.info(f"Processing person: {person} in {language}")
            
            target_person_path = os.path.join(target_dir, language, person)
            os.makedirs(target_person_path, exist_ok=True)

            file_count = 0
            for file in os.listdir(person_path):
                if file_count >= MAX_FILES_PER_PERSON:
                    break
                
                if file.endswith('.wav'):
                    file_path = os.path.join(person_path, file)
                    if process_audio_file(file_path, target_person_path, language):
                        file_count += 1

def main():
    source_dir ='/home/anymate/project/GPT-SoVITS/raw_data/long_game_audio/'
    target_directory = '/home/anymate/project/GPT-SoVITS/raw_data/filtered_data/'

    delete_existing_target_data(target_directory)

    filter_files(source_dir, target_directory)

    source_dir = '/home/anymate/project/GPT-SoVITS/raw_data/audio_slicer/'
    filter_files(source_dir, target_directory)


if __name__ == "__main__":
    main()
