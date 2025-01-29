import numpy as np
import time

# Define the matrix sizes to test
sizes = [10, 50, 100, 200, 500, 800, 1000, 1500, 2000, 2500]

# Loop over each size and perform matrix multiplication
for size in sizes:
    # Generate random matrices of the given size
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    
    # Perform matrix multiplication and measure the time
    start_time = time.time()
    C = np.dot(A, B)
    end_time = time.time()
    
    # Output the result and the time taken for the current size
    print(f"Matrix size: {size}x{size}")
    print(f"Time taken: {end_time - start_time:.4f} seconds\n")
