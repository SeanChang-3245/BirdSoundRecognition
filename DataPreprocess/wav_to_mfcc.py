import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from scipy.io import wavfile
from python_speech_features import mfcc, logfbank


# 1 sec = 200 frame

wav_base_dir = "E:\\Sean\\BirdRecognitionTrainingData\\Audio_wav"
npy_base_dir = "E:\\Sean\\BirdRecognitionTrainingData\\ndarray"
TOTAL_AUDIO_CNT = 12484


def main():
    total_second = 0
    with tqdm(total=TOTAL_AUDIO_CNT) as pbar:    
        for dir in os.scandir(wav_base_dir):

            dir_name = dir.name
            
            if not os.path.exists(f"{npy_base_dir}\\{dir_name}"):
                os.makedirs(f"{npy_base_dir}\\{dir_name}")

            for file in os.scandir(dir.path):

                try:
                    file_path = file.path
                    file_no_ext = file.name.split(".")[0]

                    frequency_sampling, audio_signal = wavfile.read(file_path)

                    features_mfcc = mfcc(audio_signal, frequency_sampling, numcep=39, nfilt=39, nfft=1200)

                    np.save(file=f"{npy_base_dir}\\{dir_name}\\{file_no_ext}.npy", arr=features_mfcc)
                    
                    
                    pbar.update(1)
                    total_second += features_mfcc.shape[0] / 200.0
                except:
                    with open("log.txt", "a") as file:
                        file.write(f"fail on {file_path}\n")
                
    print(f"total {total_second} seconds of audio")

# total 592587 second
if __name__ == "__main__":
    main()