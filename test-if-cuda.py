#!/usr/bin/python
import torch

cuda_available = torch.cuda.is_available()

if cuda_available:
    print("CUDA is available.")
else:
    print("CUDA is not available.")

device = torch.device("cuda" if cuda_available else "cpu")
print("Current device:", device)

tensor = torch.tensor([1, 2, 3])
tensor = tensor.to(device)  # Move the tensor to the specified device

if tensor.is_cuda:
    print("The tensor is allocated on a CUDA device.")
else:
    print("The tensor is not allocated on a CUDA device.")