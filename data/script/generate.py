import os
import shutil

BASE_PATH = '/home/anymate/project/GPT-SoVITS/raw_data/filtered_data'
TARGET_PATH = '/home/anymate/project/GPT-SoVITS/data/'
RAW_TARGET_PATH = os.path.join(TARGET_PATH, 'raw')
ESD_LIST_PATH = os.path.join(TARGET_PATH, 'esd.list')

def read_lab_file(lab_file_path):
    if os.path.exists(lab_file_path):
        with open(lab_file_path, 'r', encoding='utf-8') as lab_file:
            return lab_file.read().strip().replace("|", "")
    return ''

def process_wav_file(speaker_path, filename, language_id, speaker_name, esd_list_file):
    src_file_path = os.path.join(speaker_path, filename)
    dst_file_name = f"{language_id}_{filename}"
    dst_file_path = os.path.join(RAW_TARGET_PATH, dst_file_name)

    lab_file_path = os.path.join(speaker_path, filename.replace('.wav', '.lab'))
    label_text = read_lab_file(lab_file_path)

    shutil.copy(src_file_path, dst_file_path)
    esd_list_file.write(f'{dst_file_path}|{speaker_name}|{language_id}|{label_text}\n')

def generate_esd_list(base_path):
    os.makedirs(RAW_TARGET_PATH, exist_ok=True)

    with open(ESD_LIST_PATH, 'w', encoding='utf-8') as esd_list_file:
        for language_folder in os.listdir(base_path):
            language_path = os.path.join(base_path, language_folder)
            if not os.path.isdir(language_path):
                continue

            for speaker_folder in os.listdir(language_path):
                speaker_path = os.path.join(language_path, speaker_folder)
                if not os.path.isdir(speaker_path):
                    continue



                #if file count is less than 20, skip
                if len(os.listdir(speaker_path)) < 20:
                    continue

                #print speaker folder name and count of files
                print(language_folder,speaker_folder, len(os.listdir(speaker_path)))

                speaker_path = os.path.join(language_path, speaker_folder)

                for filename in os.listdir(speaker_path):
                    if filename.endswith('.wav'):
                        process_wav_file(speaker_path, filename, language_folder, speaker_folder, esd_list_file)

if __name__ == '__main__':
    #delete existing esd list and raw data
    if os.path.exists(ESD_LIST_PATH):
        os.remove(ESD_LIST_PATH)
    if os.path.exists(RAW_TARGET_PATH):
        shutil.rmtree(RAW_TARGET_PATH)

    generate_esd_list(BASE_PATH)
