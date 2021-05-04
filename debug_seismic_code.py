import interdependent_networks.tests_library as tl
from interdependent_networks.runnables import *
import interdependent_networks.map_handler as map
import interdependent_networks.seismic_data.image_process as ip
import numpy as np

def load_network(x_coordinate, y_coordinate, n_inter, version, model, exp=2.5):
    print("start {}".format(datetime.datetime.now()))
    network_system = InterdependentGraph()
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "networks")
    AS_title = os.path.join(path, csv_title_generator("logic", "20", "500", exp, version=1))
    phys_title = os.path.join(path, csv_title_generator("physic", x_coordinate, y_coordinate, exp, version=version,
                                                        model=model))
    interd_title = os.path.join(path, csv_title_generator("dependence", "20", "500", exp, n_inter, 6,
                                                          version=1))
    providers_title = os.path.join(path, csv_title_generator("providers", "20", "500", exp, n_inter,
                                                             6, version=1))
    nodes_title = os.path.join(path, csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=1))
    network_system.create_from_csv(AS_title, phys_title, interd_title, nodes_title, providers_csv=providers_title)
    print("System created {} from:".format(datetime.datetime.now()))
    print(" -> Logical network: {}".format(AS_title))
    print(" -> Inter-links: {}".format(interd_title))
    print(" -> Providers: {}".format(providers_title))
    print(" -> Physical network: {}".format(phys_title))
    print(" -> Node allocation: {}".format(nodes_title))
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
network = load_network("20", "500", 3, 1, "MRN")
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

max_radius = km_to_coordinates_chile(4400)
print(max_radius)
all_gl = []
for i in range(100):
    result = tl.probabilistic_localized_attack(network, x, y, max_radius, tl.seismic_probability_function_chile, param)
    all_gl.append(result['GL'])

print(np.mean(all_gl))
print(np.std(all_gl))

max_radius = km_to_coordinates_chile(400)
print(max_radius)
all_gl = []
for i in range(100):
    result = tl.probabilistic_localized_attack(network,x, y, max_radius, tl.seismic_probability_function_chile, param)
    all_gl.append(result['GL'])

print(np.mean(all_gl))
print(np.std(all_gl))