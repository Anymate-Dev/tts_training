import os,sys,numpy as np
import traceback
import shutil
from scipy.io import wavfile
# parent_directory = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(parent_directory)
from tools.my_utils import load_audio
from slicer2 import Slicer

def slice(inp,opt_root,threshold=-34,min_length=4000,min_interval=1000,hop_size=10,max_sil_kept=500,_max=0.9,alpha=0.25,i_part=0,all_part=30):
    os.makedirs(opt_root,exist_ok=True)
    if os.path.isfile(inp):
        input=[inp]
    elif os.path.isdir(inp):
        input=[os.path.join(inp, name) for name in sorted(list(os.listdir(inp)))]
    else:
        return "输入路径存在但既不是文件也不是文件夹"
    slicer = Slicer(
        sr=32000,  # 长音频采样率
        threshold=      int(threshold),  # 音量小于这个值视作静音的备选切割点
        min_length=     int(min_length),  # 每段最小多长，如果第一段太短一直和后面段连起来直到超过这个值
        min_interval=   int(min_interval),  # 最短切割间隔
        hop_size=       int(hop_size),  # 怎么算音量曲线，越小精度越大计算量越高（不是精度越大效果越好）
        max_sil_kept=   int(max_sil_kept),  # 切完后静音最多留多长
    )
    _max=float(_max)
    alpha=float(alpha)
    for inp_path in input[int(i_part)::int(all_part)]:
        # print(inp_path)
        try:
            name = os.path.basename(inp_path)
            audio = load_audio(inp_path, 32000)
            # print(audio.shape)
            for chunk, start, end in slicer.slice(audio):  # start和end是帧数
                tmp_max = np.abs(chunk).max()
                if(tmp_max>1):chunk/=tmp_max
                chunk = (chunk / tmp_max * (_max * alpha)) + (1 - alpha) * chunk
                wavfile.write(
                    "%s/%s_%010d_%010d.wav" % (opt_root, name, start, end),
                    32000,
                    # chunk.astype(np.float32),
                    (chunk * 32767).astype(np.int16),
                )
        except:
            print(inp_path,"->fail->",traceback.format_exc())
    return "执行完毕，请检查输出文件"



# slice('/home/anymate/project/GPT-SoVITS/raw_data/audio/famale001.mp3','/home/anymate/project/GPT-SoVITS/raw_data/audio_slicer')


source_audio_dir = '/home/anymate/project/GPT-SoVITS/raw_data/audio'
target_dir = '/home/anymate/project/GPT-SoVITS/raw_data/audio_slicer/en'

#if target_dir exists, delete it
if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
    
os.makedirs(target_dir, exist_ok=True)

#list all files in the source audio directory
audio_files = os.listdir(source_audio_dir)

#slice each audio file
for audio_file in audio_files:
    target_audio_dir_name = audio_file.split('.')[0]
    #create a directory for each audio file
    target_audio_dir = os.path.join(target_dir, target_audio_dir_name)
    os.makedirs(target_audio_dir, exist_ok=True)
    #slice the audio file
    slice(os.path.join(source_audio_dir, audio_file), target_audio_dir)
    
    

    





    





