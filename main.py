from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import json
import os
import io
from io import BytesIO
import logging


# Initialize GCS client
storage_client = storage.Client()
bucket_name = "matrix-multiplication-bucket"
bucket = storage_client.get_bucket(bucket_name)

def map_function(request):
    # Parse request data
    request_json = request.get_json(silent=True)
    if request_json and 'rows' in request_json and 'cols' in request_json and 'size' in request_json:
        # This means we are invoking for multiple rows and columns
        rows = request_json['rows']
        cols = request_json['cols']
        size = request_json['size']
        responses = []

        for row in range(rows):
            for col in range(cols):
                payload = {
                    'row': row,
                    'col': col,
                    'size': size
                }
                response = process_single_mapping(payload)
                responses.append(f"Response for row {row}, col {col}: {response}")

        return {"responses": responses}
    
    elif request_json and 'row' in request_json and 'col' in request_json and 'size' in request_json:
        # This means we are invoking for a specific row and column
        row = request_json['row']
        col = request_json['col']
        size = request_json['size']
        return process_single_mapping({'row': row, 'col': col, 'size': size})

    else:
        return "Invalid request. Please provide rows, cols, and size in JSON format.", 400

def process_single_mapping(payload):
    row = payload['row']
    col = payload['col']
    size = payload['size']

    # Load matrices from GCS
    A = load_matrix_from_gcs("matrices/A.npy")
    B = load_matrix_from_gcs("matrices/B.npy")

    # Calculate the partial product
    partial_product = np.dot(A[row, :], B[:, col])

    # Store the result in GCS as a single-element array to keep it as an .npy file
    output_blob_name = f"partial_product_row_{row}_col_{col}.npy"
    np.save(f"/tmp/{output_blob_name}", np.array([partial_product]))  # Save as an array for .npy format
    blob = bucket.blob(output_blob_name)
    blob.upload_from_filename(f"/tmp/{output_blob_name}")

    return f"Partial product for row {row} and column {col} computed and saved."


def download_blob(bucket_name, blob_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        return np.load(BytesIO(blob.download_as_bytes()))
    except Exception as e:
        logging.error(f"Error downloading {blob_name}: {e}")
        return None  # Return None if the blob is missing

def reduce_function(request):

    request_json = request.get_json(silent=True)
    rows = request_json.get('rows')
    cols = request_json.get('cols')
    bucket_name = request_json.get('bucket_name')
    
    if rows is None or cols is None or bucket_name is None:
        return {"error": "Missing 'rows', 'cols', or 'bucket_name' in request JSON."}, 400
    
    partial_products = []
    blob_names = [f'partial_product_row_{row}_col_{col}.npy' for row in range(rows) for col in range(cols)]

    # Download all partial products in parallel
    with ThreadPoolExecutor() as executor:
        downloaded_data = list(executor.map(lambda name: download_blob(bucket_name, name), blob_names))
    
    # Filter out any None entries (missing blobs)
    downloaded_data = [data for data in downloaded_data if data is not None]
    
    if downloaded_data:
        # Proceed with reduction logic if data is available
        result_matrix = sum(downloaded_data)
        
        # Save the result back to Google Cloud Storage
        output_blob_name = "result_matrix.npy"
        output_bucket = storage_client.bucket(bucket_name)
        output_blob = output_bucket.blob(output_blob_name)
        
        # Save the result matrix to .npy format and upload
        np.save('/tmp/result_matrix.npy', result_matrix)
        output_blob.upload_from_filename('/tmp/result_matrix.npy')
        
        return {"message": "Matrix reduction completed successfully."}
    else:
        return {"message": "No partial products were available for reduction."}, 404

def load_matrix_from_gcs(blob_name):
    """Load a matrix from a blob in Google Cloud Storage."""
    blob = bucket.blob(blob_name)
    if blob.exists():
        data = blob.download_as_bytes()
        return np.load(io.BytesIO(data), allow_pickle=True)
    else:
        raise FileNotFoundError(f"Blob {blob_name} not found in bucket {bucket_name}.")
