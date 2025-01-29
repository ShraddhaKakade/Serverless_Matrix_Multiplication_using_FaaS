import numpy as np
from google.cloud import storage

def generate_and_upload_matrices(bucket_name, size):
    # Generate two random matrices
    matrix_A = np.random.rand(size, size)
    matrix_B = np.random.rand(size, size)

    # Save matrices to .npy files
    np.save('A.npy', matrix_A)
    np.save('B.npy', matrix_B)

    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Upload .npy files to the GCS bucket
    blobs = {
        'A.npy': 'matrices/A.npy',
        'B.npy': 'matrices/B.npy'
    }
    
    for local_filename, gcs_filename in blobs.items():
        blob = bucket.blob(gcs_filename)
        blob.upload_from_filename(local_filename)
        print(f'Uploaded {local_filename} to {gcs_filename} in bucket {bucket_name}')

# Example usage
if __name__ == "__main__":
    bucket_name = "matrix-multiplication-bucket"  # Replace with your GCS bucket name
    size = 100  # Size of the matrices
    generate_and_upload_matrices(bucket_name, size)
