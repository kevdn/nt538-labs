import time
import random
import threading
import multiprocessing 

# Matrix addition helper function
def matrixAdd(A, B):
    return [[a + b for a, b in zip(row_a, row_b)] for row_a, row_b in zip(A, B)]

# Single-threaded matrix multiplication
def single_thread_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sum_value = sum(A[i][k] * B[k][j] for k in range(n))
            result[i][j] = sum_value
    return result

# Multithreaded matrix multiplication using threading
def multi_thread_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]

    def multiply_elements(i, j):
        result[i][j] = sum(A[i][k] * B[k][j] for k in range(n))

    threads = []
    for i in range(n):
        for j in range(n):
            thread = threading.Thread(target=multiply_elements, args=(i, j))
            threads.append(thread)
            thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return result

# Helper function for multiprocessing 
# Calculate the product of a single element in the resulting matrix
def multiply_elements(args):
    i, j, A, B, n = args
    return i, j, sum(A[i][k] * B[k][j] for k in range(n))

# Multiprocessing matrix multiplication using multiprocessing.Pool
def parallel_multiply_matrices(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]

    # Prepare arguments for each matrix element
    indices = [(i, j, A, B, n) for i in range(n) for j in range(n)]
    
    # Create a pool of processes and map the function to each element
    pool = multiprocessing.Pool(4) #4 cores
    results = pool.map(multiply_elements, indices)

    for i, j, value in results:
        result[i][j] = value

    pool.close()
    pool.join()

    return result

# Matrix generation without numpy
def generate_matrix(size, value_range=(0, 10)):
    return [[random.randint(*value_range) for _ in range(size)] for _ in range(size)]

# Timing function
def time_execution(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result
    

def test(size): # Smaller size for testing; replace with 5000 for actual benchmarking
    A = generate_matrix(size)
    B = generate_matrix(size)

    # Single-threaded execution
    single_time, _ = time_execution(single_thread_multiply, A, B)
    print("Single-threaded execution time: {:.2f} seconds".format(single_time))

    # Multithreaded execution
    multi_thread_time, _ = time_execution(multi_thread_multiply, A, B)
    print("Multithreaded execution time: {:.2f} seconds".format(multi_thread_time))

    # Multiprocessing execution
    multi_process_time, _ = time_execution(parallel_multiply_matrices, A, B)
    print("Multiprocessing execution time: {:.2f} seconds".format(multi_process_time))


# Main function to execute and time the modes
if __name__ == '__main__':
    for size in [10, 100, 500, 1000, 2000]:
        print("\nMatrix size: {}x{}".format(size, size))
        test(size)
        print("-" * 40)
    
