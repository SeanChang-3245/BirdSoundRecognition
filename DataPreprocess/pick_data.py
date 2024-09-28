import os
import numpy as np
from tqdm import tqdm
from math import ceil

RATIO = 0.2
SPECIES_CNT = 663
SAVE_PATH = "E:\\Sean\\BirdRecognitionTrainingData\\picked_training_feature_ndarray"

arr = np.load("E:\\Sean\\BirdRecognitionTrainingData\\training_feature_ndarray\\八哥(冠八哥).npy")
print(arr.shape)

with tqdm(total=SPECIES_CNT) as pbar:
    for file in os.scandir("E:\\Sean\\BirdRecognitionTrainingData\\training_feature_ndarray"): 
        arr = np.load(file.path)
        
        data_cnt = arr.shape[0]
        pick_cnt = np.int64(ceil(data_cnt * RATIO))
        np.random.shuffle(arr)
        
        arr = arr[:pick_cnt, :]
        if arr.shape[0] == 0:
            with open("./log.txt", "w") as file:
                file.write(f"no data on {file.name}")
        
        np.save(f"{SAVE_PATH}\\{file.name}", arr)
        
        pbar.update(1)
    
    pass
    