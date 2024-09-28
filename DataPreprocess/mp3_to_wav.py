from tqdm import tqdm
import os
from pydub import AudioSegment

MAX_AUDIO_CNT = 20
TOTAL_JOB = 672

# files                                                                         
mp3_base_dir  = "E:\\Sean\\BirdRecognitionTrainingData\\Audio_mp3"
wav_base_dir = "E:\\Sean\\BirdRecognitionTrainingData\\Audio_wav"
src = "DataPreprocess/grbtit1_1.mp3"
dst = "test.wav"

starting_idx = 350
cur_idx = 0

FAILED = []

with tqdm(total=TOTAL_JOB) as pbar:
    for dir_name in os.scandir(mp3_base_dir):

        cur_idx += 1
        if cur_idx < starting_idx:
            pbar.update(1)
            continue
        
        if not dir_name.is_dir():
            continue
        
        wav_dir = f"{wav_base_dir}\\{dir_name.name}"
        if not os.path.exists(wav_dir):
            os.makedirs(wav_dir)
        
        file_cnt = 0
        for filename in os.scandir(dir_name.path):
            if not filename.is_file():
                continue
            
            if file_cnt > MAX_AUDIO_CNT:
                break
            
            try:
                file_dir = filename.path
                name_no_ext = filename.name.split(".")[0]
                
                sound = AudioSegment.from_mp3(file_dir)
                sound.export(f"{wav_dir}\\{name_no_ext}.wav", format="wav")
                file_cnt += 1
                
                if file_cnt >= MAX_AUDIO_CNT:
                    break
        
            except:
                with open("./log.txt", "a") as f:
                    f.write(f"failed on {wav_dir}\\{name_no_ext}.wav \n")
                FAILED.append(file_dir)
        
        pbar.update(1)
        

