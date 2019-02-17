def find_non_zero_mean(lst):
    min_val = float('inf')
    for val in lst:
        if val != 0:
            if val < min_val:
                min_val = val
    return min_val

def get_kb_movies():
    with open('kb_movies.txt', 'r') as filehandle:
        movies = set()
        for line in filehandle:
            movies.add(line[:-1])
    return movies

def get_kb_actors():
    with open('kb_actors.txt', 'r') as filehandle:
        movies = set()
        for line in filehandle:
            movies.add(line[:-1])
    return movies