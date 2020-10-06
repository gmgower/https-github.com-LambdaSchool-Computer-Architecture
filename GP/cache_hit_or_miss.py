import time


matrix = []

size = 10000

# make a matrix
for i in range(size):
    row = [0] * size
    matrix.append(row)
	
# Cache hit - iterating across rows, processor can predict what to cache
start_time = time.time()
for row in range(size):
    for col in range(size):
        matrix[row][col]

print(time.time() - start_time)

# Cache miss - iterating down cols
start_time = time.time()
for row in range(size):
    for col in range(size):
        matrix[col][row]

print(time.time() - start_time)