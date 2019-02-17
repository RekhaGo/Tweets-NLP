def find_non_zero_mean(lst):
    min_val = float('inf')
    for val in lst:
        if val != 0:
            if val < min_val:
                min_val = val
    return min_val
