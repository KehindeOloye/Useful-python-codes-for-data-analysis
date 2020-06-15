import numpy as np
from math import sqrt, ceil
import cv2
import struct

#Input file name
input_file_name = 'hello-world.apk';

#Read the whole file to data
with open(input_file_name, 'rb') as binary_file:
    data = binary_file.read()

# Data length in bytes
data_len = len(data)

# d is a verctor of data_len bytes
d = np.frombuffer(data, dtype=np.uint8)

data_len_as_bytes = np.frombuffer(struct.pack("Q", data_len), dtype=np.uint8) # Convert data_len to 8 bytes

data_len = data_len + len(data_len_as_bytes) #Update length to include the 8 bytes

# Set data_len as first 8 bytes of d
d = np.hstack((data_len_as_bytes, d))

# Assume image shape should be close to square
sqrt_len = int(ceil(sqrt(data_len)))  # Compute square toot and round up

# Requiered length in bytes.
new_len = sqrt_len*sqrt_len

# Number of bytes to pad (need to add zeros to the end of d)
pad_len = new_len - data_len

# Pad d with zeros at the end.
# padded_d = np.pad(d, (0, pad_len))
padded_d = np.hstack((d, np.zeros(pad_len, np.uint8)))

# Reshape 1D array into 2D array with sqrt_len pad_len x sqrt_len (im is going to be a Grayscale image).
im = np.reshape(padded_d, (sqrt_len, sqrt_len))

# Save image
cv2.imwrite('im.png', im)