import json
import os
import numpy as np
from tqdm import tqdm

WINDOW_DURATION = 3 # second
WINDOW_SHIFT = 3 # second
FRAME_IN_ONE_SEC = 200

# One row represent a training data, which has WINDOW_DURATION * FRAME_IN_ONE_SEC * 39 columns
# One ndarray for one species

arr_base_dir = "E:\\Sean\\BirdRecognitionTrainingData\\ndarray"
output_dir = "E:\\Sean\\BirdRecognitionTrainingData\\training_feature_ndarray"


with tqdm(total=671) as pbar:

    # Iterate bird
    for dir in os.scandir(arr_base_dir):
            
        dir_path = dir.path
        dir_name = dir.name
        output_arr = np.zeros(39 * WINDOW_DURATION * FRAME_IN_ONE_SEC)
        
        
        # Iterate .wav of a bird
        for file in os.scandir(dir_path):

            try:
                file_path = file.path
                arr = np.load(file=file_path)
                length = arr.shape[0]

                # Iterate frames of a .wav of a bird
                # window is shorter than 3 seconds, pad 0 at the end 
                for begin in range(0, length, WINDOW_SHIFT * FRAME_IN_ONE_SEC):
                    
                    tmp = np.array([])

                    if begin + WINDOW_DURATION * FRAME_IN_ONE_SEC > length:
                        diff = WINDOW_DURATION * FRAME_IN_ONE_SEC - (length - begin)
                        tmp = np.pad(arr[begin:, :], [(0, diff), (0, 0)], mode="constant", constant_values=0)
                    else:
                        tmp = arr[begin:begin + WINDOW_DURATION*FRAME_IN_ONE_SEC, :]    

                    tmp = tmp.reshape(-1)
                    output_arr = np.vstack(tup=(output_arr, tmp))
            except:
                with open("log.txt", "a") as file:
                    file.write(f"fail on {file.path}\n")


        try: 
            # Ignore the first row
            if output_arr.ndim != 2:
                print(f"{dir.path} is empty\n")
                continue
            
            np.save(f"{output_dir}/{dir_name}.npy", output_arr[1:, :])
        except:
            with open("log.txt", "a") as file:
                file.write(f"fail on {dir.name}\n")
        
        pbar.update(1)