import os
from shutil import copy2, rmtree
from pydub import AudioSegment
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def delete_existing_target_data(target_dir):
    # 检查目标目录是否存在，如果存在则删除
    if os.path.exists(target_dir):
        logging.info(f"Deleting existing data in {target_dir}")
        rmtree(target_dir)
    else:
        logging.info(f"No existing data found in {target_dir}")

def create_emotion_folders(base_path):
    emotions = [
        "Happiness", "Sadness", "Anger", "Calm", 
        "Surprise", "Fear", "Anticipation", "Disgust", "to_process"
    ]
    for emotion in emotions:
        os.makedirs(os.path.join(base_path, emotion), exist_ok=True)

def copy_files_if_duration_matches(source_dir, target_dir, min_duration=5000, max_duration=9000):
    # 删除目标目录下的现有数据
    delete_existing_target_data(target_dir)

    # 遍历源目录
    for language in ['en', 'zh']:
        lang_path = os.path.join(source_dir, language)
        logging.info(f"Processing language: {language}")
        
        for person in os.listdir(lang_path):
            person_path = os.path.join(lang_path, person)
            if not os.path.isdir(person_path):
                continue

            logging.info(f"Processing person: {person} in {language}")
            
            # 创建目标人物目录并在其中创建情感文件夹
            target_person_path = os.path.join(target_dir, language, person)
            create_emotion_folders(target_person_path)

            # 遍历人名文件夹中的文件
            for file in os.listdir(person_path):
                if file.endswith('.wav'):
                    file_path = os.path.join(person_path, file)
                    audio = AudioSegment.from_wav(file_path)
                    duration = len(audio)

                    # 检查音频时长是否在指定范围内
                    if min_duration <= duration <= max_duration:
                        # 复制音频和文本文件到to_process文件夹
                        to_process_path = os.path.join(target_person_path, "to_process")
                        logging.info(f"Copying audio and text for: {file} with duration {duration}ms to {to_process_path}")
                        for suffix in ['.wav', '.lab']:
                            src_file_path = os.path.splitext(file_path)[0] + suffix
                            if os.path.exists(src_file_path):
                                copy2(src_file_path, to_process_path)
                    else:
                        logging.info(f"Skipping {file}, duration {duration}ms does not meet criteria")

# 设置源目录和目标目录
source_directory = '/home/anymate/project/GPT-SoVITS/data/2024-01-18'
target_directory = '/home/anymate/project/GPT-SoVITS/data/filter_data'

copy_files_if_duration_matches(source_directory, target_directory)
