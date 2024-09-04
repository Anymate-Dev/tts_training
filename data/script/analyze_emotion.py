from openai import OpenAI
import os
import shutil


client = OpenAI(api_key='')

def copy_files_to_emotion_folder(root_dir, emotion, text_file, audio_file):
    """Copy the text and audio files to the specified emotion folder."""
    # 构造正确的目标文件夹路径，去除`To_process`部分
    destination_folder = os.path.join(root_dir, os.path.dirname(text_file).replace('to_process', ''), emotion)
    print('copy to :'+ destination_folder)
    if not os.path.exists(destination_folder):
        return
    shutil.copy(text_file, os.path.join(destination_folder, os.path.basename(text_file)))
    shutil.copy(audio_file, os.path.join(destination_folder, os.path.basename(audio_file)))


def analyze_text_emotion(text):
    response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "I'll give you a character line, and I'll ask you to judge for me the mood of this character. Choose the best one from Happiness, Sadness, Anger, Calm, Surprise, Fear, Anticipation, Disgust. just tell me the type, don't reply to other messages"},
        {"role": "assistant", "content": "Of course! Go ahead and share the character line with me."},
        {"role": "user", "content": "Dear customer, Wangsheng Funeral Parlor does appreciate your patronage, but you needn't hasten the inevitable! Are you alright?"},
        {"role": "assistant", "content": "Calm"},
        {"role": "user", "content": text},
    ]
    )
    print(text)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def analyze_emotion_and_copy_files(root_dir):
    """Analyze the emotion of text in .lab files and copy files to the corresponding emotion folder."""
    for language_folder in os.listdir(root_dir):
        language_path = os.path.join(root_dir, language_folder)
        if os.path.isdir(language_path):
            for person_folder in os.listdir(language_path):
                person_path = os.path.join(language_path, person_folder)
                to_process_folder = os.path.join(person_path, 'to_process')
                if os.path.exists(to_process_folder):
                    for file in os.listdir(to_process_folder):
                        if file.endswith('.lab'):
                            text_file_path = os.path.join(to_process_folder, file)
                            with open(text_file_path, 'r', encoding='utf-8') as file:
                                text_content = file.read()

                            emotion = analyze_text_emotion(text_content)
                            audio_file_path = text_file_path.replace('.lab', '.wav')
                            
                            # Copy files to the corresponding emotion folder
                            copy_files_to_emotion_folder(root_dir, emotion, text_file_path, audio_file_path)

root_dir = '/home/anymate/project/GPT-SoVITS/data/filter_data'
analyze_emotion_and_copy_files(root_dir)
