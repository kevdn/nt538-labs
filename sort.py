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

def merge_sort_descending(arr):
    # Sort một mảng theo thứ tự giảm dần
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = merge_sort_descending(arr[:mid])
    right = merge_sort_descending(arr[mid:])
    
    return merge(left, right)

def parallel_sorting_descending(array_a):
    # Số core được sử dụng
    num_cores = 4
    
    # Tính kích thước của mỗi phần
    chunk_size = len(array_a) // num_cores
    
    # Chia mảng thành 4 phần bằng nhau
    chunks = [array_a[i:i + chunk_size] for i in range(0, len(array_a), chunk_size)]
    
    # Nếu số phần tử không chia hết cho 4, gộp phần dư vào chunk cuối
    if len(chunks) > num_cores:
        chunks[num_cores-1].extend(chunks[num_cores:])
        chunks = chunks[:num_cores]
    
    # Tạo pool với 4 processes
    with Pool(processes=num_cores) as pool:
        # Sort song song các chunks
        sorted_chunks = pool.map(merge_sort_descending, chunks)
    
    # Merge các chunks đã sort
    final_result = sorted_chunks[0]
    for i in range(1, len(sorted_chunks)):
        final_result = merge(final_result, sorted_chunks[i])
    
    return final_result
