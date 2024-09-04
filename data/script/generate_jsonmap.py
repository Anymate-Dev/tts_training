import os
import json

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def scan_directory(base_path):
    catalog = {'en': {}, 'zh': {}}

    for lang in ['en', 'zh']:
        lang_path = os.path.join(base_path, lang)
        for person in os.listdir(lang_path):
            person_path = os.path.join(lang_path, person)
            if os.path.isdir(person_path):
                catalog[lang][person] = {}
                for emotion in os.listdir(person_path):
                    emotion_path = os.path.join(person_path, emotion)
                    if os.path.isdir(emotion_path):
                        files_info = {}
                        file_names = [os.path.splitext(f)[0] for f in os.listdir(emotion_path)]
                        unique_file_names = set(file_names)
                        for base_name in unique_file_names:
                            wav_path = os.path.join(emotion_path, base_name + '.wav')
                            lab_path = os.path.join(emotion_path, base_name + '.lab')
                            if os.path.isfile(wav_path) and os.path.isfile(lab_path):
                                text_content = read_text_file(lab_path)
                                files_info[base_name] = {'file': wav_path, 'text': text_content}
                        catalog[lang][person][emotion] = list(files_info.values())[:5]  # Only include up to 5 pairs
    return catalog

def write_catalog_to_json(catalog, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=4)








base_directory = '/home/anymate/project/GPT-SoVITS/data/filter_data'
catalog = scan_directory(base_directory)
output_file = 'directory_catalog.json'
write_catalog_to_json(catalog, output_file)
