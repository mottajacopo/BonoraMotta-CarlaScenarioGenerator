
import random
import carla
import pyoscx
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

#connect to carla server and get informations of the world
client = carla.Client('localhost', 2000)
client.set_timeout(5.0)
world = client.get_world()
iteration = -1

def check_town(town):
    current_map = world.get_map()

    if(current_map.name != town):
        client.load_world(town)
        print("The CARLA server uses the wrong map:")
        print("Loading correct map: ...wait")
        time.sleep(10)


def shift_lane(pos, direction):
    current_map = world.get_map()

    new_pos = pos
    carla_loc = carla.Location(new_pos.position.x, (-1)*new_pos.position.y, new_pos.position.z)
    waypoint = current_map.get_waypoint(carla_loc)

    if (direction == 'right'):
        lane_change = waypoint.get_right_lane()
        new_c = lane_change.transform.location

    elif(direction == 'left'):
        lane_change = waypoint.get_left_lane()
        new_c = lane_change.transform.location

    new_pos.position.x = new_c.x
    new_pos.position.y = new_c.y *(-1)
    new_pos.position.z = new_c.z

    return new_pos


def get_random_spawn_points(offset, check_lane):   #get spawn points for ego, adversary and npcs

    current_map = world.get_map()

    # spawn_transforms will be a list of carla.Transform
    spawn_transforms = current_map.get_spawn_points()

    # get a single random spawn transformation over the map
    random_spawn = random.choice(spawn_transforms)

    #convert transform to waypoint
    waypoint = current_map.get_waypoint(random_spawn.location)

    npc_spawns = []

    #check_intersection = waypoint.is_intersection or waypoint.is_junction


    #if scenario requested do a lane check to see if left lane is free
    if(check_lane == "left"):
        while (not(waypoint.lane_change != carla.libcarla.LaneChange.Right and waypoint.get_left_lane() != None)):
            random_spawn = random.choice(spawn_transforms)
            waypoint = current_map.get_waypoint(random_spawn.location)  
    elif(check_lane == "right"):
        while (not(waypoint.lane_change != carla.libcarla.LaneChange.Left and waypoint.get_right_lane() != None)):
            random_spawn = random.choice(spawn_transforms)
            waypoint = current_map.get_waypoint(random_spawn.location)   
    elif(check_lane == "both"):
        while (not(waypoint.lane_change == carla.libcarla.LaneChange.Both)):
            random_spawn = random.choice(spawn_transforms)
            waypoint = current_map.get_waypoint(random_spawn.location)  

    back_spawn = random_spawn
    back_waypoint = current_map.get_waypoint(back_spawn.location)   
           
    #compute adversary spawn point 
    front_spawn_offset = get_offset_waypoint(back_waypoint, offset)

    #convert carla location to pyxosc location
    back_start = carla2pyxosc(back_spawn)
    front_start = carla2pyxosc(front_spawn_offset.transform)

    npc_spawns = get_random_npc_spawn(current_map, front_spawn_offset.transform, 150, offset, check_lane)


    return back_start, front_start, npc_spawns 


def get_random_vehicles():   #get random vehicle name

    blueprint_library = world.get_blueprint_library()

    vehicles_blacklist = ['vehicle.bh.crossbike',
                        'vehicle.kawasaki.ninja',
                        'vehicle.yamaha.yzf',
                        'vehicle.harley-davidson.low_rider',
                        'vehicle.gazelle.omafiets',
                        'vehicle.diamondback.century',
                        'vehicle.tesla.cybertruck',
                        'vehicle.bmw.isetta',
                        'vehicle.tesla.model3']

    vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))
    vehicle_name = vehicle_bp.id

    while (vehicle_name in vehicles_blacklist):
        vehicle_bp = random.choice(blueprint_library.filter('vehicle.*.*'))
        vehicle_name = vehicle_bp.id

    return vehicle_name


def get_offset_waypoint(waypoint_ego, offset):   #computer offset waypoint
    waypoint = waypoint_ego
    traveled_distance = 0
    distance = offset
    while traveled_distance < distance: 
        waypoint_new = waypoint.next(1.0)[-1]
        traveled_distance += waypoint_new.transform.location.distance(waypoint.transform.location)
        waypoint = waypoint_new
    return waypoint


def carla2pyxosc(spawn):   #convert carla location to pyxosc

    x = spawn.location.x
    y = spawn.location.y *(-1)  #multiply for -1 because of carla bug
    z = spawn.location.z
    h = math.radians(spawn.rotation.yaw) *(-1)   #multiply for -1 because of carla bug

    return pyoscx.TeleportAction(pyoscx.WorldPosition(x, y, z, h))


def get_random_npc_spawn(current_map, ego_spawn,radius, offset, check_lane):

    npc_spawns = []

    radius1 = radius
    radius3 = offset

    c_x = ego_spawn.location.x
    c_y = ego_spawn.location.y

    ego_waypoint = current_map.get_waypoint(ego_spawn.location)
    ego_lane_id = ego_waypoint.lane_id

    if (check_lane == "left" and ego_waypoint.get_left_lane() != None):
        lane_change_id = ego_waypoint.get_left_lane().lane_id
    elif(check_lane == "right" and ego_waypoint.get_right_lane() != None):
        lane_change_id = ego_waypoint.get_right_lane().lane_id
    else:
        lane_change_id = 999

    spawn_transforms = current_map.get_spawn_points()
    for spawn in spawn_transforms:
        random_waypoint = current_map.get_waypoint(spawn.location)
        random_lane_id = random_waypoint.lane_id
        if(spawn != ego_spawn):
            if (c_x-spawn.location.x)**2 + (c_y-spawn.location.y)**2 <= radius1**2:
                if ((random_lane_id != lane_change_id) and (random_lane_id != ego_lane_id)):
                    npc_spawns.append(carla2pyxosc(spawn))
                elif(c_x-spawn.location.x)**2 + (c_y-spawn.location.y)**2 >= (radius3 + 10)**2:

                    npc_spawns.append(carla2pyxosc(spawn))
    
    return npc_spawns
