import carla
import argparse

argparser = argparse.ArgumentParser(
    description=__doc__)
argparser.add_argument(
    '--host',
    metavar='H',
    default='127.0.0.1',
    help='IP of the host server (default: 127.0.0.1)')
argparser.add_argument(
    '-p', '--port',
    metavar='P',
    default=2000,
    type=int,
    help='TCP port to listen to (default: 2000)')
argparser.add_argument(
    '-s', '--speed',
    metavar='FACTOR',
    default=1.0,
    type=float,
    help='rate at which the weather changes (default: 1.0)')
args = argparser.parse_args()

speed_factor = args.speed
update_freq = 0.1 / speed_factor

client = carla.Client(args.host, args.port)
world = client.get_world()
blueprint = world.get_blueprint_library().filter('vehicle.mercedes.*')[0]
map = world.get_map()
t_intersection_spawn_waypoint = map.get_waypoint_xodr(52, -1, 75.0)
spawn_location_list = map.get_spawn_points()
print(spawn_location_list[10])
# t_intersection_spawn_waypoint.transform.location.x += 3.0
#t_intersection_spawn_waypoint.transform.location.z += 2.0
# t_intersection_spawn_waypoint.transform.location.y += 3.0
#sworld.debug.draw_point(t_intersection_spawn_waypoint.transform.location, size=0.5)
world.spawn_actor(blueprint, spawn_location_list[10])