import os
import shutil

def generate_esd_list(base_path):
    date_folder = '2024-01-18'
    source_path = os.path.join(base_path, date_folder)
    raw_folder_path = os.path.join(source_path, 'raw')
    esd_list_path = os.path.join(source_path, 'esd.list')

    if not os.path.exists(raw_folder_path):
        os.makedirs(raw_folder_path)

    with open(esd_list_path, 'w', encoding='utf-8') as esd_list_file:
        for language_folder in os.listdir(source_path):
            language_path = os.path.join(source_path, language_folder)
            if os.path.isdir(language_path):
                for speaker_folder in os.listdir(language_path):
                    speaker_path = os.path.join(language_path, speaker_folder)
                    if os.path.isdir(speaker_path):
                        for filename in os.listdir(speaker_path):
                            if filename.endswith('.wav'):
                                speaker_name = speaker_folder
                                language_id = language_folder

                                lab_file_path = os.path.join(speaker_path, filename.replace('.wav', '.lab'))
                                label_text = ''
                                if os.path.exists(lab_file_path):
                                    with open(lab_file_path, 'r', encoding='utf-8') as lab_file:
                                        label_text = lab_file.read().strip().replace("|", "")

                                src_file_path = os.path.join(speaker_path, filename)
                                dst_file_path = os.path.join(raw_folder_path, language_id+"_"+filename)

                                # shutil.copy(src_file_path, dst_file_path)
                                esd_list_file.write(f'/home/anymate/project/GPT-SoVITS/data/2024-01-18/raw/{language_id+"_"+filename}|{speaker_name}|{language_id}|{label_text}\n')


if __name__ == '__main__':
    base_path = '/home/anymate/project/GPT-SoVITS/data'
    print(1)
    # generate_esd_list(base_path)
