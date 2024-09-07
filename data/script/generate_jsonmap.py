import os
import json
import shutil

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def get_file_info(person_path, base_name):
    wav_path = os.path.join(person_path, f"{base_name}.wav")
    lab_path = os.path.join(person_path, f"{base_name}.lab")
    
    if os.path.isfile(wav_path) and os.path.isfile(lab_path):
        text_content = read_text_file(lab_path)
        return {'file': wav_path, 'text': text_content}
    return None

def scan_person_directory(person_path):
    files_info = {}
    file_names = set(os.path.splitext(f)[0] for f in os.listdir(person_path))
    
    for base_name in file_names:
        file_info = get_file_info(person_path, base_name)
        if file_info:
            files_info[base_name] = file_info
    
    return list(files_info.values())  # Only include up to 5 pairs

def scan_directory(base_path):
    catalog = {lang: {} for lang in ['en', 'zh']}

    for lang in catalog:
        lang_path = os.path.join(base_path, lang)
        if os.path.isdir(lang_path):
            for person in os.listdir(lang_path):
                person_path = os.path.join(lang_path, person)
                if os.path.isdir(person_path):
                    person_files = scan_person_directory(person_path)
                    if person_files:
                        catalog[lang][person] = person_files

    return catalog

if __name__ == "__main__":
    base_directory = '/home/anymate/project/GPT-SoVITS/raw_data/filtered_data'
    reference_directory = '/home/anymate/project/GPT-SoVITS/reference'

    # Delete reference directory
    shutil.rmtree(reference_directory, ignore_errors=True)

    # Create reference directory
    os.makedirs(reference_directory, exist_ok=True)

    catalog = scan_directory(base_directory)

    # Copy files to reference directory and generate jsonmap
    jsonmap = {lang: {} for lang in catalog}
    for lang in catalog:
        for person in catalog[lang]:
            person_path = os.path.join(reference_directory, lang, person)
            os.makedirs(person_path, exist_ok=True)
            jsonmap[lang][person] = []

            for file_info in catalog[lang][person]:
                src_file = file_info['file']
                dst_file = os.path.join(person_path, os.path.basename(src_file))
                shutil.copy2(src_file, dst_file)
                jsonmap[lang][person].append(dst_file)

    # Write jsonmap to file
    with open(os.path.join(reference_directory, 'jsonmap.json'), 'w', encoding='utf-8') as f:
        json.dump(jsonmap, f, ensure_ascii=False, indent=4)

    print(f"Jsonmap has been generated at {os.path.join(reference_directory, 'jsonmap.json')}")

