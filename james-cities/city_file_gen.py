import sys
from random import randint

# Get specified num of cities and initialise empty matrix
num_cities = 100#int(sys.argv[1])
str_num_cities = str(num_cities)
distance_matrix = [[[] for x in range(num_cities-y-1)] for y in range(num_cities-1)]

# Populate matrix with random distances
for i in range(num_cities-1):
    for j in range(num_cities-i-1):
        #distance_matrix[i][j] = randint(1,100)
        distance_matrix[i][j] = 1

# Create city file and write to it
filename = "AISearchfile" + str_num_cities + ".txt"
with open(filename, "w+") as f:
    f.write("NAME = AISearchfile" + str_num_cities + ",\n")
    f.write("SIZE = " + str_num_cities + ",\n")

    for i in range(num_cities-1):
        if i != num_cities-2:
            f.write(str(distance_matrix[i])[1:-1] + ",\n")
        else:
            f.write(str(distance_matrix[i])[1:-1])

# Inform user of successful file generation
print(filename + " generated successfully.")
