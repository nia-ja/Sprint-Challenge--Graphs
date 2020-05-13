from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


## BFT to traverse all rooms
## keep track of how many moves to traverse
traversal_path = []
## a dictionary of all the rooms we have visited
visited = {}
## path array
path = []
## reverse directions to get back out of a room
directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# append the current room to the visited dictionary
# "getExists" to navigate throughout the world
visited[player.current_room.id] = player.current_room.get_exits()

## loop till player have visited all the rooms
while len(visited) < len(room_graph) - 1:
    ## check if the player's room is not in visited
    if player.current_room.id not in visited:
        ## add it to the visited dictionary
        ## remove the previous set of exists and replace it with the current rooms exists
        visited[player.current_room.id] = player.current_room.get_exits()
        previous_direction = path[-1]
        visited[player.current_room.id].remove(previous_direction)

    ## up until this point we have a BFT
    ## however we need to find ALL rooms.
    ## find num of rooms
    ## check is len(visited) >= len(rooms)

    ## while the len of the visited rooms directions are 0.
    ## Reached end, or a dead end

    while len(visited[player.current_room.id]) == 0:
        ## backtrack/pop path return to previous direction
        previous_direction = path.pop()
        traversal_path.append(previous_direction)
        ## travel function from player class allows to move to the previous room
        player.travel(previous_direction)

    ## find the current rooms get_exits and then we find the last value on that list with pop
    move = visited[player.current_room.id].pop(0)
    ## we then append it to the path since its the direction we want to go
    traversal_path.append(move)
    ## we append it to the path so we can record the room we just visited
    path.append(directions[move])
    ##  move direction with the players function travel. will be backtracking via the direction dictionary at top
    player.travel(move)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")