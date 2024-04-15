# imports
import numpy as np
from collections import deque

################ HELPER FUNCTIONS #################

def flatten(lst_of_lsts):
    '''Flattens a list of lists `lst_of_lsts`.'''
    return [elem for lst in lst_of_lsts for elem in lst]

def distinct_elems(lst):
    '''Returns a list of distinct elements from a given list `lst`.'''
    return list(set(lst))

def shortest_lists(lst_of_lists):
    '''Helper function to find the shortest list(s) in a list of lists'''
    if lst_of_lists: # checks that lst_of_lists is not empty

        # initializes list of same-length lists
        current_list = []
        
        for lst in lst_of_lists:

            # adds to current list if current list is empty or the lengths are the same
            if not current_list or len(lst) == len(current_list[0]):
                current_list.append(lst)
            
            # else replaces the entire list with shorter candidates
            elif len(lst) < len(current_list[0]):
                current_list = [lst]

        return current_list
    return []

def filter_dict(dic, lst_of_keys):
    '''Outputs a filtered subset of the dictionary `dic` with only keys in `lst_of_keys`
    '''
    filtered_dic = {key: val for key, val in dic.items() if key in lst_of_keys}

    return filtered_dic

###################################################


# dictionary of mrt stations, organized by line
mrt_info = {'NS': ['Jurong East', 'Bukit Batok', 'Bukit Gombak', 'Choa Chu Kang', 
                   'Yew Tee', 'Kranji', 'Marsiling', 'Woodlands', 'Admiralty', 
                   'Sembawang', 'Canberra', 'Yishun', 'Khatib', 'Yio Chu Kang', 
                   'Ang Mo Kio', 'Bishan', 'Braddell', 'Toa Payoh', 'Novena', 
                   'Newton', 'Orchard', 'Somerset', 'Dhoby Ghaut', 'City Hall', 
                   'Raffles Place', 'Marina Bay', 'Marina South Pier'],
            'EW': ['Pasir Ris', 'Tampines', 'Simei', 'Tanah Merah', 'Bedok', 
                   'Kembangan', 'Eunos', 'Paya Lebar', 'Aljunied', 'Kallang', 
                   'Lavender', 'Bugis', 'City Hall', 'Raffles Place', 'Tanjong Pagar',
                   'Outram Park', 'Tiong Bahru', 'Redhill', 'Queenstown', 'Commonwealth', 
                   'Buona Vista', 'Dover', 'Clementi', 'Jurong East', 'Chinese Garden', 
                   'Lakeside', 'Boon Lay', 'Pioneer', 'Joo Koon', 'Gul Circle', 
                   'Tuas Crescent', 'Tuas West Road', 'Tuas Link'],
            'CG': ['Tanah Merah', 'Expo', 'Changi Airport'],
            'CC': ['Dhoby Ghaut', 'Bras Basah', 'Esplanade', 'Promenade', 
                   'Nicoll Highway', 'Stadium', 'Mountbatten', 'Dakota', 'Paya Lebar', 
                   'MacPherson', 'Tai Seng', 'Bartley', 'Serangoon', 'Lorong Chuan', 
                   'Bishan', 'Marymount', 'Caldecott', 'Botanic Gardens', 'Farrer Road', 
                   'Holland Village', 'Buona Vista', 'one-north', 'Kent Ridge', 
                   'Haw Par Villa', 'Pasir Panjang', 'Labrador Park', 'Telok Blangah', 
                   'HarbourFront'],
            'CE': ['Promenade', 'Bayfront', 'Marina Bay'],
            'DT': ['Bukit Panjang', 'Cashew', 'Hillview', 'Beauty World', 'King Albert Park', 
                   'Sixth Avenue', 'Tan Kah Kee', 'Botanic Gardens', 'Stevens', 'Newton', 
                   'Little India', 'Rochor', 'Bugis', 'Promenade', 'Bayfront', 'Downtown', 
                   'Telok Ayer', 'Chinatown', 'Fort Canning', 'Bencoolen', 'Jalan Besar', 
                   'Bendemeer', 'Geylang Bahru', 'Mattar', 'MacPherson', 'Ubi', 'Kaki Bukit', 
                   'Bedok North', 'Bedok Reservoir', 'Tampines West', 'Tampines', 
                   'Tampines East', 'Upper Changi', 'Expo'],
            'NE': ['Harbourfront', 'Outram Park', 'Chinatown', 'Clarke Quay', 'Dhoby Ghaut', 
                   'Little India', 'Farrer Park', 'Boon Keng', 'Potong Pasir', 'Woodleigh', 
                   'Serangoon', 'Kovan', 'Hougang', 'Buangkok', 'Sengkang', 'Punggol'],
            'TE': ['Woodlands North', 'Woodlands', 'Woodlands South', 'Springleaf', 'Lentor', 
                   'Mayflower', 'Bright Hill', 'Upper Thompson', 'Caldecott', 'Stevens', 
                   'Napier', 'Orchard Boulevard', 'Orchard', 'Great World', 'Havelock', 
                   'Outram Park', 'Maxwell', 'Shenton Way', 'Marina Bay', 'Gardens By The Bay'],
            'BP': ['Choa Chu Kang', 'South View', 'Keat Hong', 'Teck Whye', 'Phoenix', 
                   'Bukit Panjang']}

# gets a list of distinct mrt stations
mrt_stations = distinct_elems(flatten(list(mrt_info.values())))

# creates a dictionary with stations as keys, and the lines they are part of as values
mrt_station_lines = {}
for station in mrt_stations:
    
    # initializes list of stations
    mrt_station_lines[station] = []

    for line in mrt_info.keys():
        if station in mrt_info[line]:
            mrt_station_lines[station].append(line)


# this is an abstraction layer for readability in the code cell below

def get_line(line_station):
    '''Returns the line in a `(line, station)` tuple'''
    return line_station[0]

def get_station(line_station):
    '''Returns the station in a `(line, station)` tuple'''
    return line_station[1]


# initializes the MRT network dictionary
mrt_network = {}
for station, lines in mrt_station_lines.items():
    for line in lines:
        mrt_network[(line, station)] = []


# populates each key with its neighbouring stations
# transits between lines are counted as separate stations

for line_station in mrt_network:

    # first we populate the transits
    # checks if station is an interchange
    if len(mrt_station_lines[get_station(line_station)]) > 1:
        for line in mrt_station_lines[get_station(line_station)]:

            # appends the other lines for the same station
            if line != get_line(line_station):
                mrt_network[line_station].append((line, get_station(line_station)))


    # now we populate the rest of the adjacent stations
                
    # forward direction
    # checks if station is not a terminal station
    if get_station(line_station) != mrt_info[get_line(line_station)][-1]:
        # gets the station index
        station_index = mrt_info[get_line(line_station)].index(get_station(line_station))
        mrt_network[line_station].append((get_line(line_station), mrt_info[get_line(line_station)][station_index + 1]))
    
    # backward direction
    # checks if station is not an initial station
    if get_station(line_station) != mrt_info[get_line(line_station)][0]:
        # gets the station index
        station_index = mrt_info[get_line(line_station)].index(get_station(line_station))
        mrt_network[line_station].append((get_line(line_station), mrt_info[get_line(line_station)][station_index - 1]))



# implementing Dijkstra's algorithm using deque from Python's collections module
def shortest_mrt_line_station_path(start_line_station, end_line_station, network=mrt_network):
    '''This uses Dijkstra's algorithm to find the shortest route between two MRT stations.
    
    For the purposes of simplicity, this function uses the `(line, station_name)` format for both start and end stations.'''

    # initializes a dictionary of visited stations
    # keys: visited stations
    # values: routes to station in key
    # we start the traversal by visiting start_line_station
    visited_stations = {start_line_station: [start_line_station]}

    # a queue of stations to visit
    # this will be updated as we traverse the network
    stations_to_visit = deque([start_line_station])

    # while there are still stations to visit
    while len(stations_to_visit):
        
        # pops the first station in the deque to check
        current_station = stations_to_visit.popleft()

        # checks adjacent stations to current station
        for next_station in network[current_station]:
            
            # checks if this station has already been visited
            # we do not want to repeat any visits in the shortest path
            # this works because the shortest route (i.e., the route with least number of stations) will be recorded first
            # any longer route would not pass this check
            if next_station not in visited_stations:

                # records the path taken to this station
                visited_stations[next_station] = visited_stations[current_station] + [next_station]

                # queues this station to check later
                stations_to_visit.append(next_station)
    
    # returns the shortest path to the end station
    return visited_stations[end_line_station]

########################################################

# test cases
# start_point = ('CC', 'Kent Ridge')
# end_point = ('NS', 'Bukit Batok')

# shortest_mrt_line_station_path(start_point, end_point)

def shortest_mrt_station_path(start_station, end_station):

    '''Finds the shortest path(s) from `start_station` to `end_station`, taking into account which lines the route starts and ends on.

    Returns a list of routes that have the shortest route length. Transiting between different lines is counted as +1 length.
    
    Both `start_station` and `end_station` are just the station names themselves. Specifying the line is unneeded since 
    this function would search through all possible combinations of start and end MRT lines.'''

    # initializes list of possible routes
    possible_routes = []

    # checks all possible routes using the different lines from start and end stations
    for start_lines in mrt_station_lines[start_station]:
        for end_lines in mrt_station_lines[end_station]:

            # finds shortest route for each start_line end_line combination
            # and appends it to possible_routes
            start_line_station = (start_lines, start_station)
            end_line_station = (end_lines, end_station)
            possible_routes.append(shortest_mrt_line_station_path(start_line_station, end_line_station))
    
    # picks out the shortest routes from all the possible routes
    shortest_route = shortest_lists(possible_routes)

    return shortest_route

#####################################################

# test case
# shortest_mrt_station_path('Orchard', 'Bukit Batok')

def shortest_route_to_targets(target_stations, start_point, output='route'):
    '''Finds the shortest route from an MRT station `start_point` to a station in `target_stations`.
    
    Parameters
    ----------
    - `start_point`: The name of the station.
    - `output`: Either `'route'`, `'score'`, or `'both'`.
        - `'route'` to output a list of the shortest route(s)
        - `'score'` to output only the score
        - `'both'` to output a tuple `(score, route(s))`'''
    
    # initializing the outputs
    possible_routes = []
    best_score = 0

    # helper list
    current_routes = []

    for target_station in target_stations:

        # routes to current city station
        current_routes = shortest_mrt_station_path(start_point, target_station)

        # appends the current routes if possible_routes is empty, or there is a score tie
        if not possible_routes or (len(current_routes[0]) == best_score):
            possible_routes += current_routes
            
        # else replaces the current shortest route(s) with the better route(s)
        elif len(current_routes[0]) < best_score:
            possible_routes = current_routes

        best_score = len(possible_routes[0])

    if output == 'route':
        return possible_routes
    
    if output == 'score':
        # we want to reflect the number of stations traversed
        # excluding the start station
        return best_score - 1 
    
    if output == 'both':
        return (best_score - 1, possible_routes)
    
    return 0

##################################################

# test cases
# shortest_route_to_targets('Orchard', output='both')

def get_mrt_scores(target_stations: list[str]):
    '''
    Returns a dictionary of `station`-`score` key-value pairs, 
    where `score` is the minimal number of stations from `station` to a station in `target_stations`, 
    among all stations in `target_stations`.

    Parameters
    ---
    - `target_stations`: A list of MRT stations
    '''

    mrt_scores_per_station = {station: shortest_route_to_targets(target_stations, station, output='score') for station in mrt_stations}
    return mrt_scores_per_station