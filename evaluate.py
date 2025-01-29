import requests
import time
import numpy as np
from google.cloud import storage

# Cloud Function URLs
MAP_FUNCTION_URL = "https://us-central1-shraddha-kakade-fall2024.cloudfunctions.net/map_function"
REDUCE_FUNCTION_URL = "https://us-central1-shraddha-kakade-fall2024.cloudfunctions.net/reduce_function"

# Google Cloud Storage settings
BUCKET_NAME = "matrix-multiplication-bucket"
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

def generate_and_store_matrices(size):
    """Generate random matrices and store them in GCS."""
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    
    np.save("/tmp/A.npy", A)
    np.save("/tmp/B.npy", B)
    
    bucket.blob("matrices/A.npy").upload_from_filename("/tmp/A.npy")
    bucket.blob("matrices/B.npy").upload_from_filename("/tmp/B.npy")

def measure_execution_time(size):
    """Measure execution time for a given matrix size."""
    generate_and_store_matrices(size)
    
    # Measure map function time
    map_start = time.time()
    map_response = requests.post(MAP_FUNCTION_URL, json={"rows": size, "cols": size, "size": size})
    map_end = time.time()
    map_time = map_end - map_start
    
    # Measure reduce function time
    reduce_start = time.time()
    reduce_response = requests.post(REDUCE_FUNCTION_URL, json={"rows": size, "cols": size, "bucket_name": BUCKET_NAME})
    reduce_end = time.time()
    reduce_time = reduce_end - reduce_start
    
    total_time = map_time + reduce_time
    
    return map_time, reduce_time, total_time

def main():
    matrix_sizes = [10, 50, 100, 200, 500]  # Add or modify sizes as needed
    results = []
    
    for size in matrix_sizes:
        print(f"Processing matrix size: {size}x{size}")
        map_time, reduce_time, total_time = measure_execution_time(size)
        results.append({
            "size": size,
            "map_time": map_time,
            "reduce_time": reduce_time,
            "total_time": total_time
        })
        print(f"Map time: {map_time:.2f}s, Reduce time: {reduce_time:.2f}s, Total time: {total_time:.2f}s")
        print("--------------------")
    
    # Print summary table
    print("\nSummary:")
    print("Size\tMap Time (s)\tReduce Time (s)\tTotal Time (s)")
    for result in results:
        print(f"{result['size']}\t{result['map_time']:.2f}\t\t{result['reduce_time']:.2f}\t\t{result['total_time']:.2f}")

if __name__ == "__main__":
    main()