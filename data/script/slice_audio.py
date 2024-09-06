import os
import sys
import numpy as np
import traceback
import shutil
from scipy.io import wavfile
from tools.my_utils import load_audio
from slicer2 import Slicer

def slice_audio(input_path, output_root, **slicer_params):
    os.makedirs(output_root, exist_ok=True)
    
    if os.path.isfile(input_path):
        input_files = [input_path]
    elif os.path.isdir(input_path):
        input_files = [os.path.join(input_path, name) for name in sorted(os.listdir(input_path))]
    else:
        return "Input path exists but is neither a file nor a directory"

    slicer = Slicer(sr=32000, **slicer_params)
    
    for inp_path in input_files:
        try:
            process_audio_file(inp_path, output_root, slicer)
        except Exception as e:
            print(f"{inp_path} -> fail -> {traceback.format_exc()}")
    
    return "Execution completed. Please check the output files."

def process_audio_file(input_path, output_root, slicer, max_amplitude=0.9, alpha=0.25):
    name = os.path.basename(input_path)
    audio = load_audio(input_path, 32000)
    
    for chunk, start, end in slicer.slice(audio):
        chunk = normalize_audio_chunk(chunk, max_amplitude, alpha)
        save_audio_chunk(chunk, output_root, name, start, end)

def normalize_audio_chunk(chunk, max_amplitude, alpha):
    tmp_max = np.abs(chunk).max()
    if tmp_max > 1:
        chunk /= tmp_max
    return (chunk / tmp_max * (max_amplitude * alpha)) + (1 - alpha) * chunk

def save_audio_chunk(chunk, output_root, name, start, end):
    output_path = f"{output_root}/{name}_{start:010d}_{end:010d}.wav"
    wavfile.write(output_path, 32000, (chunk * 32767).astype(np.int16))

def process_directory(source_dir, target_dir):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    os.makedirs(target_dir, exist_ok=True)

    for audio_file in os.listdir(source_dir):
        target_audio_dir_name = os.path.splitext(audio_file)[0]
        target_audio_dir = os.path.join(target_dir, target_audio_dir_name)
        os.makedirs(target_audio_dir, exist_ok=True)
        

        slice_audio(os.path.join(source_dir, audio_file), target_audio_dir,
            threshold=-34.0,  # Amplitude threshold for silence detection (in dB)
            min_length=4000,  # Minimum length of a valid audio segment (in milliseconds)
            min_interval=1500, # Minimum length of silence between segments (in milliseconds)
            hop_size=10,      # Step size for the sliding window (in milliseconds)
            max_sil_kept=200  # Maximum silence length kept at the beginning and end of each segment (in milliseconds)
        )
        

if __name__ == "__main__":
    source_audio_dir = '/home/anymate/project/GPT-SoVITS/raw_data/long_aduio/en'
    target_dir = '/home/anymate/project/GPT-SoVITS/raw_data/audio_slicer/en'
    
    #clear target dir
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    process_directory(source_audio_dir, target_dir)
    
    

    





    





