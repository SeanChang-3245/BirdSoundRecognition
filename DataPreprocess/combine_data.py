import numpy as np
import os
import json
from tqdm import tqdm

with open("./data/json/name_to_class.json", encoding="utf-8") as json_file:
    DICT = json.load(json_file)
    

output_feature_arr = np.array([])
output_label_arr = np.array([])
with tqdm(total=663) as pbar:
    for file in os.scandir("E:\\Sean\\BirdRecognitionTrainingData\\picked_training_feature_ndarray"):
        try:
            arr = np.load(file.path)        
            data_cnt = arr.shape[0]
            
            tmp = np.full(shape=(data_cnt,), fill_value=DICT[file.name[:-4]])
            output_label_arr = np.append(arr=output_label_arr, values=tmp)
                    
            if output_feature_arr.ndim != 2:
                output_feature_arr = arr
            else:
                output_feature_arr = np.concatenate([output_feature_arr, arr], axis=0)
                    
            pbar.update(1)
        except:
            with open("./log.txt", "a", encoding="utf-8") as file:
                file.write(f"fail on {file.name}")

np.save("./data/ndarray/feature", output_feature_arr)
np.save("./data/ndarray/label", output_label_arr)

print(output_feature_arr.shape)
print(output_label_arr.shape)