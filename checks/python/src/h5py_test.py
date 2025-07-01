import h5py
import numpy as np      #h5py uses numpy and depends on it

# Create a h5 file
with h5py.File('test.h5', 'w') as f:
    # basic data
    data = [i**2.0 for i in range(100)]
    f.create_dataset('dataset1', data=data)

# Open the test.h5 file and read the saved data
with h5py.File('test.h5', 'r') as f:
    data1 = f['dataset1'][:]
    assert (data==data1).all(), "Read values mismatch saved values."

print ("simple h5py test passed.")