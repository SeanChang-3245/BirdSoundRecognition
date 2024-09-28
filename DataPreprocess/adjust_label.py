import numpy as np


# turn class number in to one-hot vector

arr = np.load("./data/ndarray/label.npy")
output_label_arr = np.full(shape=(41520, 672), fill_value=float(0.0))

for i in range(41520):
    ans = int(arr[i])
    output_label_arr[i,ans] = float(1.0)
    

print(output_label_arr.shape)
np.save("./data/ndarray/one_hot_label", output_label_arr)