import tests_library as tl
from runnables import *
import map_handler as map
import seismic_data.image_process as ip
import numpy as np


def load_network(x_coordinate, y_coordinate, n_inter, version, model, exp=2.5):
    process_name = "debug_seismic"
    interlink_type = "provider_priority"
    legacy = False
    logic_file_name = "logic_exp_2.5_v1.csv"
    interlink_version = 3
    print("{} -- start {}".format(process_name, datetime.datetime.now()))
    interlink_type_names = {"provider_priority": "pp", "full_random": "fr", "semi_random": "sr"}
    network_system = InterdependentGraph()
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "networks")

    logic_dir = os.path.join(path, "logical_networks")
    physical_dir = os.path.join(path, "physical_networks", "links")
    interlink_dir = os.path.join(path, "interdependencies", "full_random")
    providers_dir = os.path.join(path, "providers")

    if interlink_type == "provider_priority":
        interlink_dir = os.path.join(path, "interdependencies", "provider_priority")
        providers_dir = os.path.join(providers_dir, "provider_priority")
    elif interlink_type == "semi_random":
        interlink_dir = os.path.join(path, "interdependencies", "semi_random")
        providers_dir = os.path.join(providers_dir, "semi_random")
    elif interlink_type == "full_random":
        providers_dir = os.path.join(providers_dir, "full_random")

    node_loc_dir = os.path.join(path, "physical_networks", "node_locations")

    if legacy:
        logic_title = "legacy_{}".format(csv_title_generator("logic", "20", "500", exp, version=1))
        interlink_title = "legacy_{}".format(csv_title_generator("dependence", "20", "500", exp, n_inter, 6,
                                                                 version=1))
        providers_title = "legacy_{}".format(csv_title_generator("providers", "20", "500", exp, n_inter, 6,
                                                                 version=1))
    else:
        if logic_file_name:
            logic_title = logic_file_name
        else:
            logic_title = "legacy_{}".format(csv_title_generator("logic", "20", "500", exp, version=1))
        interlink_title = csv_title_generator("dependence", "", "", "", n_inter, 6, version=interlink_version)
        providers_title = csv_title_generator("providers", "", "", "", n_inter, 6, version=interlink_version)

    nodes_loc_title = csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version)
    physic_title = csv_title_generator("physic", x_coordinate, y_coordinate, exp, version=version, model=model)
    logic_dir = os.path.join(logic_dir, logic_title)
    physical_dir = os.path.join(physical_dir, physic_title)
    interlink_dir = os.path.join(interlink_dir, interlink_title)
    providers_dir = os.path.join(providers_dir, providers_title)
    nodes_loc_dir = os.path.join(node_loc_dir, nodes_loc_title)

    network_system.create_from_csv(logic_dir, physical_dir, interlink_dir, nodes_loc_dir,
                                   providers_csv=providers_dir)

    print("{} -- System created {} from:".format(process_name, datetime.datetime.now()))
    print("{} -- -> Logical network: {}".format(process_name, logic_dir))
    print("{} -- -> Inter-links: {}".format(process_name, interlink_dir))
    print("{} -- -> Providers: {}".format(process_name, providers_dir))
    print("{} -- -> Physical network: {}".format(process_name, physical_dir))
    print("{} -- -> Node allocation: {}".format(process_name, nodes_loc_dir))
    return network_system


def coordinates_to_km_chile(coordinates):
    coordinate = 20
    kms = 175
    factor = kms/coordinate # kms per unit of "coordinate"
    return coordinates*factor


def km_to_coordinates_chile(kms):
    coordinate = 20
    km = 175
    factor = coordinate / km  # "coordinate" per km
    return kms * factor


def soil_value(vs30):
    return 0.322


# create a network
network = load_network("20", "500", 3, 1, "RNG")
# get physical network
physical_net = network.get_phys()
# get vss30
vs30_matrix = ip.create_values_matrix('seismic_data/m_full_map.png', 'seismic_data/map_scale2.png', 2200, 0)
# make map
map_obj = map.SoilMap(vs30_matrix, soil_value, (20, 500))
# set soil things onto physical network
physical_net = map_obj.assign_soil_to_points(physical_net)
# re-set modified physical network
network.set_physical(physical_net)

param = {}
param["magnitude"] = 8.8
param["depth"] = 28.1
param["event_type"] = 0

x = 10
y = 200

max_radius = km_to_coordinates_chile(400)
print("Max radius: {}, cap at {}".format(np.round(max_radius, 4), 4400))
all_gl = []
for i in range(100):
    result = tl.probabilistic_localized_attack(network, x, y, max_radius, tl.seismic_probability_function_chile, param)
    all_gl.append(result['GL'])

print("Average GL: {} ({})".format(round(np.mean(all_gl), 4), round(np.std(all_gl), 4)))
exit(43)
max_radius = km_to_coordinates_chile(400)
print("Max radius: {}, cap at {}".format(np.round(max_radius, 4), 400))
all_gl = []
for i in range(100):
    result = tl.probabilistic_localized_attack(network, x, y, max_radius, tl.seismic_probability_function_chile, param)
    all_gl.append(result['GL'])

print("Average GL: {} ({})".format(round(np.mean(all_gl), 4), round(np.std(all_gl), 4)))