import os
import shutil

# 指定目标目录
target_directory = 'target_directory/'

# 情绪文件夹名称列表
emotions = [
    'Happiness', 'Sadness', 'Anger', 'Calm', 
    'Surprise', 'Fear', 'Anticipation', 'Disgust', 'to_process'
]

# 遍历目标目录
for root, dirs, files in os.walk(target_directory):
    for dir_name in dirs:
        # 构建当前人名文件夹的完整路径
        person_path = os.path.join(root, dir_name)
        if os.path.isdir(person_path):
            # 在每个人名文件夹下创建情绪文件夹
            for emotion in emotions:
                emotion_path = os.path.join(person_path, emotion)
                if not os.path.exists(emotion_path):
                    os.mkdir(emotion_path)
            
            # 移动文件到to_process文件夹
            for file in os.listdir(person_path):
                file_path = os.path.join(person_path, file)
                if os.path.isfile(file_path):
                    shutil.move(file_path, os.path.join(person_path, 'to_process'))

print("文件已成功移动到to_process文件夹中。")
