# Serverless Matrix-Multiplication using FaaS

## 1. Components:

### generate_store_matrices.py

o Generates two matrices to pass to Map function

### main.py

o Contains “map_function()” and “reduce_function()”

o These functions are deployed as “Functions as a Service”

### evaluate.py

o This file is used to evaluate the performance of “map_function()” and “reduce_function” as FaaS for different sizes of matrices

### requirements.py

o Contains list of required python libraries to run above python files

### Cloud Shell Commands

o This file contains commands used to perform a trial run on Map and Reduce functions for matrix multiplication

### matrices

o This folder contains input matrices and output result matrix

o Link to "matrices" folder: https://drive.google.com/drive/folders/1fS6D1rXtw-x0g-q0Iv9FWKCKxYy8ThAW?usp=sharing 

### map_reduce.py

o This python file implements matrix multiplication in VM – “matrix-multiplication”

## 2. Implementation:

• The system uses a MapReduce paradigm implemented with Cloud Functions for distributed matrix multiplication.

• Input matrices are stored in Google Cloud Storage, in “matrix-multiplication-bucket”.

• The map function distributes the computation of individual cells of the result matrix.

• The reduce function aggregates these partial results to form the final output matrix.

• The use of HTTP-triggered functions allows for easy scaling and parallel processing of matrix multiplication tasks.

## 3. Analysis

#### Performance of Parallel Computing:

![Map-Reduce Performance](https://github.com/user-attachments/assets/791521c5-5329-4ab4-b23d-ec9953ec6b43)

#### Performance of GCP VM:

<img width="1470" alt="VM Performance" src="https://github.com/user-attachments/assets/60987155-d069-4907-9324-47484d2db01f" />




