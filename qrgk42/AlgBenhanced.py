import os
import sys
import time
import random

def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file,'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string

def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0,a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""              # "middle_string" and "to_index" play no role in the case of error
    to_index = -1                   # but need to initialized to something as they are returned
    start = a_string.find(from_string,from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        #trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string,start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            #trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string,to_index,flag

def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        #trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1         # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0,row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag

def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1,num_cities):
        for j in range(0,i):
            distance_matrix[i][j] = distance_matrix[j][i]

# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile175.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
file_string = file_string + ","         # we need to add a final comma to find the city distances
                                        # as we look for numbers between commas
print("I'm working with the file " + input_file + ".")
                                        
# get the name of the file

name_of_file,to_index,flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string,to_index,flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1             # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "qrgk42"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "Zac"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "Robinson"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "AS"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = "If no solution found after a set time (110s for submitted version), a greedy method will be used to complete the tour from the node on the fringe with the lowest f-value. *This may result in different tours for the same input depending on the current speed of the computer.*"

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF' : 'brute-force search',
                   'BG' : 'basic greedy search',
                   'BS' : 'best_first search without heuristic data',
                   'ID' : 'iterative deepening search',
                   'BH' : 'best_first search with heuristic data',
                   'AS' : 'A* search',
                   'HC' : 'hilling climbing search',
                   'SA' : 'simulated annealing search',
                   'GA' : 'genetic algorithm'}

#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

import math
import datetime
import operator
import heapq

# UTILITY FUNCTIONS
def get_closest_city_and_distance(tour, unvisited):
    # initialise current city to last in tour
    current_city = tour[-1]
    # enumerate each (next_city, distance_to_next_city), but only for unvisited cities
    unvisited_cities_and_distances = {(next_city, distance_matrix[current_city][next_city]) for next_city in unvisited}
    # return closest city-distance pair; break ties by choosing the lowest-indexed city (for consistency, as sets are unordered)
    return(min(unvisited_cities_and_distances, key=operator.itemgetter(1,0)))

# FRINGE NODE ACQUISITION FUNCTIONS
def add_all_unvisited_nodes(fringe, chosen_node):
    # iterate through all cities to add them to fringe
    unvisited_cities = chosen_node.state.unvisited
    current_city = chosen_node.state.tour[-1]
    for new_city in unvisited_cities:
        new_node_state = state(chosen_node.state.tour + [new_city])
        new_node_path_cost = chosen_node.path_cost + distance_matrix[current_city][new_city]
        new_node_depth = chosen_node.depth + 1
        new_node = Node(new_node_state, new_node_path_cost, new_node_depth)
        heapq.heappush(fringe, new_node)

def add_nearest_unvisited_node(fringe, chosen_node):
    # iterate through all cities; add to fringe the unvisited city that is closest to the last city in the current tour
    tour = list(chosen_node.state.tour)
    unvisited = set(chosen_node.state.unvisited)
    closest_city, closest_city_distance = get_closest_city_and_distance(tour, unvisited)
    new_node_state = state(tour + [closest_city])
    new_node_path_cost = chosen_node.path_cost + closest_city_distance
    new_node_depth = chosen_node.depth + 1
    new_node = Node(new_node_state, new_node_path_cost, new_node_depth)
    heapq.heappush(fringe, new_node)

def add_next_nodes(fringe, chosen_node, rush_mode=False):
    # add nodes to fringe via some function dependent on whether rush mode is active
    if not rush_mode:
        add_all_unvisited_nodes(fringe, chosen_node)
    else:
        add_nearest_unvisited_node(fringe, chosen_node)

# HEURISTIC FUNCTIONS
def h_shortest_distance_to_next(node, divby_node_num_cities=False):
    # return the distance of the closest city to the last city in the current tour
    # (optionally divided by number of cities in the node's state's tour)
    closest_city_distance = get_closest_city_and_distance(node.state.tour, node.state.unvisited)[1]
    return closest_city_distance/(len(node.state.tour)**divby_node_num_cities)

def h_greedy_completion_distance(node):
    # shallow copy state elements so as to not modify them in place, and initialise greedy completion distance
    tour = list(node.state.tour)
    unvisited = set(node.state.unvisited)
    completion_distance = 0

    # iterate until all cities have been added
    while len(tour) < num_cities:
        # get closest city and its distance, and update the greedy completion tour and distance with it
        closest_city, closest_city_distance = get_closest_city_and_distance(tour, unvisited)
        completion_distance += closest_city_distance
        tour.append(closest_city)
        unvisited.remove(closest_city)
    
    # add on the distance of final transition from last distinct city to start city and return the final greedy completion distance
    completion_distance += distance_matrix[tour[-1]][tour[0]]
    return completion_distance

# CLASS DECLARATIONS
class state:
    # node state contains tour (list) and unvisited cities (set)
    def __init__(self, tour):
        self.tour = tour
        self.unvisited = {city for city in range(num_cities) if city not in set(tour)}

class Node:

    def __init__(self, state, path_cost, depth):
        # initialise values associated with node
        self.state = state
        self.path_cost = path_cost
        self.depth = depth
        self.is_goal_state = (self.depth == num_cities-1)
        self.g = self.path_cost
        self.h = 0
        if not self.is_goal_state: # don't change h from 0 if it's a goal node
            # seperate statements form h to make it easier to measure time taken on each using line_profiler
            self.h += h_greedy_completion_distance(self) 
            if multi_heuristic:
                self.h += h_shortest_distance_to_next(self)
            # multiplier for h to increase its influence over g if needed
            h_mult = 1
            self.h *= h_mult
        self.f = self.g + self.h

    def print(self):
        s = "state: {}, path_cost: {}, depth: {}, h: {}, g: {}, f: {}"
        print(s.format(self.state.tour, self.path_cost, self.depth, self.h, self.g, self.f))

    def __lt__(self, other):    
        if self.f == other.f:
            if self.depth == other.depth:
                return self.state.tour < other.state.tour
            return self.depth > other.depth
        return self.f < other.f


# MAIN FUNCTION
def find_tour():

    # initialise global variables
    global multi_heuristic
    global rush_mode
    global start_time
    global verbose
    
    # early goal-node test:
    if num_cities == 1:
        return [0], 0
    
    # initialise fringe data structure:
    fringe = []
    # the fringe will be a heap organised by the smallest f-value (max depth, then min tour, are used to break ties)
    for start_city in range(num_cities):
        heapq.heappush(fringe, Node(state=state([start_city]), path_cost=0, depth=0))

    while len(fringe) > 0:

        # if not already in rush mode, check if it should be
        if (not rush_mode) and (time.time() - start_time >= rush_start_time):
            # clear the fringe of all nodes except current optimal, and set rush flag
            fringe = [fringe[0]]
            rush_mode = True
            if verbose:
                print("Time exceeded - starting rush mode on new root_node:")
                fringe[0].print()

        # pop optimal node from top of fringe minheap
        chosen_node = heapq.heappop(fringe)

        # goal test is performed on node creation; if passed, return route and cost of full tour
        if chosen_node.is_goal_state:
            final_tour = list(chosen_node.state.tour)
            final_tour_cost = chosen_node.path_cost + distance_matrix[final_tour[-1]][final_tour[0]]
            return final_tour, final_tour_cost
        
        # if goal test not passed, add child node(s) of chosen node to fringe
        add_next_nodes(fringe, chosen_node, rush_mode)

# optionally print tours, tour length and execution time:
verbose = False
time_limit = True # if True, algorithm must finish within 2 minutes

# record starting time in order to later determine whether algorithm has been running long enough to start rushing
start_time = time.time()

# set when to stop using A* search in order to return a full tour
if time_limit:
    rush_start_time = 110
    strict_rush_limit = True # if True, both runs have the same time limit; if false, the time limit resets between runs
else:
    rush_start_time = 1200
    strict_rush_limit = False

rush_mode = False
multi_heuristic = False

ex_start = datetime.datetime.now()
tour, tour_length = find_tour()
ex_end = datetime.datetime.now()
if verbose:
    print("Execution time for single heuristic: ", end="")
    print(ex_end-ex_start)
    print(tour)
    print(tour_length)
    print()

if not rush_mode:
    if not strict_rush_limit:
        start_time = time.time() # restart rush timer, because the rushed multi-heuristic tends not to get better tours than the 
    multi_heuristic = True
    ex_start = datetime.datetime.now()
    tour2, tour_length2 = find_tour()
    ex_end = datetime.datetime.now()
    if verbose:
        print("Execution time for multi-heuristic: ", end="")
        print(ex_end-ex_start)
        print(tour2)
        print(tour_length2)
        print()
    

    if tour_length2 < tour_length:
        tour, tour_length = tour2, tour_length2



#######################################################################################################
############ the code for your algorithm should now be complete and you should have        ############
############ computed a tour held in the list "tour" of length "tour_length"               ############
#######################################################################################################

# you do not need to worry about the code below; that is, do not touch it

#######################################################################################################
############ start of code to verify that the constructed tour and its length are valid    ############
#######################################################################################################

check_tour_length = 0
for i in range(0,num_cities-1):
    check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i+1]]
check_tour_length = check_tour_length + distance_matrix[tour[num_cities-1]][tour[0]]
flag = "good"
if tour_length != check_tour_length:
    flag = "bad"
if flag == "good":
    print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
else:
    print("***** ERROR: Your claimed tour-length of " + str(tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

#######################################################################################################
############ start of code to write a valid tour to a text (.txt) file of the correct      ############
############ format; if your tour is not valid then you get an error message on the        ############
############ standard output and the tour is not written to a file                         ############
############                                                                               ############
############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters);      ############
############ for example, dcs0iasSep22105857.txt; if dcs0iasSep22105857.txt already exists ############
############ then it is overwritten                                                        ############
#######################################################################################################

if flag == "good":
    local_time = time.asctime(time.localtime(time.time()))   # return 24-character string in form "Tue Jan 13 10:17:09 2009"
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
                                                             # output_file_time = mon + day + hour + min + sec (11 characters)
    output_file_name = my_user_name + output_file_time + ".txt"
    f = open(output_file_name,'w')
    f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
    f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
    f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
    f.write(str(tour[0]))
    for i in range(1,num_cities):
        f.write("," + str(tour[i]))
    if added_note != "":
        f.write("\nNOTE = " + added_note)
    f.close()
    print("I have successfully written the tour to the output file " + output_file_name + ".")
    
    

