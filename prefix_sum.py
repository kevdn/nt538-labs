import multiprocessing

def prefix_sum_chunk(chunk_data):
    start, end, chunk = chunk_data
    prefix_sum = []
    current_sum = 0
    for num in chunk:
        current_sum += num
        prefix_sum.append(current_sum)
    return (start, end, prefix_sum)

def MAIN(arr_a):
    n = len(arr_a)
    num_cores = multiprocessing.cpu_count()
    chunk_size = n // num_cores

    chunks = [(i, min(i + chunk_size, n), arr_a[i:min(i + chunk_size, n)]) 
              for i in range(0, n, chunk_size)]

    pool = multiprocessing.Pool(processes=num_cores)
    partial_results = pool.map(prefix_sum_chunk, chunks)
    pool.close()
    pool.join()
    offsets = [0]
    for i in range(num_cores - 1):
        offsets.append(offsets[-1] + partial_results[i][2][-1])

    result = [0] * n
    for start, _, partial_sum in partial_results:
        for i, value in enumerate(partial_sum):
            result[start + i] = value + offsets[start // chunk_size]

    return result    