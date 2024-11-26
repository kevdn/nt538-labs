from multiprocessing import Pool

def merge(left, right):
    # Merge 2 mảng đã sort theo thứ tự giảm dần
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] >= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def sort_descending(arr):
    return sorted(arr, reverse=True)

def parallel_sorting_descending(array_a):
    # Số core được sử dụng
    num_cores = 4
    
    # Tính kích thước của mỗi phần
    chunk_size = len(array_a) // num_cores
    
    # Chia mảng thành các chunks
    chunks = [array_a[i:i + chunk_size] for i in range(0, len(array_a), chunk_size)]
    # Tạo pool với 4 processes
    with Pool(processes=num_cores) as pool:
        # Sort tuần tự
        sorted_chunks = pool.map(sort_descending, chunks)
    
    # Merge các chunks đã sort
    final_result = []
    for chunk in sorted_chunks: 
        final_result = merge(final_result, chunk)
    
    return final_result

a = [1, 2, 3, 4, 5, 6, 7,8, 1, 2, 3, 4, 5]
print(parallel_sorting_descending(a))
