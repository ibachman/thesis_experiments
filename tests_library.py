__author__ = 'ivana'
import random
import seismic_data.seismic_data_processor as sdp
from interdependent_network_library import *
import seismic_data.image_process as ip
import map_handler as mp
import numpy
import datetime
import gc


def single_network_attack(interdependent_network, network_to_attack, file_name, iter_number, mode, process_name=""):
    if mode == "OLD":
        single_network_attack_old(interdependent_network, network_to_attack, file_name, iter_number,
                                  process_name=process_name)
    elif mode == "NEW":
        single_network_attack_new(interdependent_network, network_to_attack, file_name, iter_number,
                                  process_name=process_name)
    else:
        return None


def single_network_attack_new(interdependent_network, network_to_attack, file_name, iter_number, process_name=""):
    print(" -> {} -- Results path: {}".format(process_name, file_name))
    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interlink_graph = interdependent_network.get_interd()

    logic_name_by_index = get_name_by_index(logic_network)

    physical_roseta = get_roseta_from_network(physical_network)
    logical_roseta = get_roseta_from_network(logic_network)
    inner_inter_roseta = get_roseta_from_network(interlink_graph)

    phys_name_by_index = get_name_by_index(physical_network)

    intern_name_by_index, inter_roseta_phys, inter_roseta_logic = parse_interlink_network(interlink_graph,
                                                                                          phys_name_by_index,
                                                                                          logic_name_by_index)

    n_phys = len(physical_network.vs)
    n_logic = len(logic_network.vs)
    iteration_results = []

    if network_to_attack == "logic":
        samp = logic_network.vs["name"]
        iteration_range = n_logic
    else:
        samp = physical_network.vs["name"]
        iteration_range = n_phys
    for j in range(1, iteration_range):
        iteration_results.append([])

    for j in range(iter_number):
        print(" -------> [[{}]] -- {} -- iteration: {}".format(datetime.datetime.now(), process_name, (j + 1)))
        for i in range(1, iteration_range):
            # print("({}) -- {}".format(i, datetime.datetime.now()))
            list_of_nodes_to_attack = random.sample(samp, i)
            logic_nodes_deleted = attack_nodes_test(phys_name_by_index, logic_name_by_index, intern_name_by_index,
                                                    physical_network, phys_suppliers, inter_roseta_phys,
                                                    inter_roseta_logic, list_of_nodes_to_attack, physical_roseta,
                                                    logical_roseta, logic_network, logic_suppliers, interlink_graph,
                                                    inner_inter_roseta)
            iteration_results[(i - 1)].append((n_logic - len(logic_nodes_deleted)) / n_logic)

            net = network_with_deleted_nodes(logic_network, logic_nodes_deleted)
            functional_nodes = [a for a in net.vs if net.degree(a.index) > 0]
            functional_nodes_in_AS_net = len(functional_nodes)
            #print((functional_nodes_in_AS_net * 1.0) / (n_logic * 1.0))
            #print("*** {}".format(functional_nodes))

    print("Ended at {}".format(datetime.datetime.now()))
    print("Starting to write results -- {} -- [[{}]]".format(process_name, datetime.datetime.now()))

    with open(file_name, 'w') as csvfile:
        print(" -> {} -- Writing results on: {}".format(process_name, file_name))
        fieldnames = ["1-p", "mean", "std"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(iteration_range - 1):
            writer.writerow({'1-p': ((i + 1) * 1.0) / iteration_range,
                             'mean': numpy.mean(iteration_results[i]),
                             'std': numpy.std(iteration_results[i])})


def single_network_attack_old(interdependent_network, network_to_attack, file_name, iter_number, process_name=""):
    print(" -> {} -- Results path: {}".format(process_name, file_name))
    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interlink_graph = interdependent_network.get_interd()

    if not network_to_attack == "logic" and not network_to_attack == "physical":
        print("Choose a valid network to attack")
        return
    n_phys = len(physical_network.vs)
    n_logic = len(logic_network.vs)
    if network_to_attack == "logic":
        samp = logic_network.vs["name"]
        iteration_range = n_logic
    else:
        samp = physical_network.vs["name"]
        iteration_range = n_phys

    iteration_results = []
    list_of_nodes_to_attack = []

    for j in range(1, n_phys + n_logic):
        iteration_results.append([])
    for j in range(iter_number):
        print(" -------> [[{}]] -- {} -- iteration: {}".format(datetime.datetime.now(), process_name, (j+1)))
        for i in range(1, iteration_range):
            graph_copy = InterdependentGraph()
            graph_copy.create_from_graph(logic_network, logic_suppliers, physical_network, phys_suppliers,
                                         interlink_graph)

            while True:
                try:
                    list_of_nodes_to_attack = random.sample(samp, i)
                    graph_copy.attack_nodes(list_of_nodes_to_attack)
                    break
                except RandomAttackTimeoutError:
                    print("*** TIMEOUT FOR ITERATION {} - {} *** [[{}]]".format(((j+1), i), process_name,
                                                                                datetime.datetime.now()))
                    print("*** {} ***".format(list_of_nodes_to_attack))
                    pass
                except Exception as e:
                    print("*** ERROR IN ATTACK NODES {} ***".format(e.__class__))
                    pass

            iteration_results[(i-1)].append(graph_copy.get_ratio_of_funtional_nodes_in_AS_network())
            del graph_copy
            del list_of_nodes_to_attack
            gc.collect()

    print("Starting to write results -- {} -- [[{}]]".format(process_name, datetime.datetime.now()))

    with open(file_name, 'w') as csvfile:
        print(" -> {} -- Writing results on: {}".format(process_name, file_name))
        fieldnames = ["1-p", "mean", "std"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for i in range(iteration_range-1):
            writer.writerow({'1-p': ((i+1)*1.0)/iteration_range,
                             'mean': numpy.mean(iteration_results[i]),
                             'std': numpy.std(iteration_results[i])})


# this method calculates 100 iteration of attacks over the whole system
def whole_system_attack(interdependent_network, file_name, iter_number):
    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interdep_graph = interdependent_network.get_interd()
    n_phys = len(physical_network.vs)
    n_logic = len(logic_network.vs)
    iteration_results = []
    for j in range(1,n_phys+n_logic):
        iteration_results.append([])
    for j in range(iter_number):
        for i in range(1,n_phys+n_logic):
            graph_copy = InterdependentGraph()
            graph_copy.create_from_graph(logic_network,logic_suppliers,physical_network,phys_suppliers,interdep_graph)
            list_of_nodes_to_attack = random.sample(physical_network.vs["name"]+logic_network.vs["name"], i)
            graph_copy.attack_nodes(list_of_nodes_to_attack)
            iteration_results[(i-1)].append(graph_copy.get_ratio_of_funtional_nodes_in_AS_network())
    with open(file_name,'w') as csvfile:
        fieldnames = ["1-p","mean","std"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for i in range(n_phys+n_logic-1):
            writer.writerow({'1-p':(i+1)*1.0/(n_logic+n_phys),'mean':numpy.mean(iteration_results[i]),'std':numpy.std(iteration_results[i])})


def mtfr_mean_and_std(graph_list, file_name):
    mtfr_list = []
    for interdependent_system in graph_list:
        mtfr_list.append(interdependent_system.node_mtfr())
    with open(file_name,'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=mtfr_list)
        writer.writeheader()


def single_localized_attack(interdependent_network, x_coordinate,
                     y_coordinate, x_center=-1, y_center=-1, radius=-1,
                     max_radius=-1, center_function=None, radius_function=None, exp="2.5", version="0", file=None):
    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interdep_graph = interdependent_network.get_interd()

    if center_function:
        x_center, y_center = center_function(physical_network, max_radius, x_coordinate, y_coordinate)
    if radius_function:
        radius = radius_function(physical_network, max_radius, x_coordinate, y_coordinate)
    if x_center < 0 or y_center < 0 or radius < 0:
        exit("Localized attacks: negative center and/or raidus")

    # Create copy from original - why tho?
    graph_copy = InterdependentGraph()
    graph_copy.create_from_graph(logic_network, logic_suppliers, physical_network, phys_suppliers, interdep_graph)

    # Get nodes to attack
    nodes_to_attack = []  # name list
    for vertex in physical_network.vs:
        x = vertex["x_coordinate"]
        y = vertex["y_coordinate"]
        if ((x - x_center) ** 2) + ((y - y_center) ** 2) <= radius ** 2:
            nodes_to_attack.append(vertex["name"])

    # attack:
    graph_copy.attack_nodes(nodes_to_attack)
    g_l = graph_copy.get_ratio_of_funtional_nodes_in_AS_network()
    aux_str = "["
    for n in nodes_to_attack:
        aux_str += "{}.".format(n)
    aux_str = aux_str[0:(len(aux_str)-1)] + "]"

    result_dict = {"x_center": x_center,
                   "y_center": y_center,
                   "nodes_removed": aux_str,
                   "GL": g_l,
                   "radius": radius}
    return result_dict


def localized_attack(iterations, interdependent_network, x_coordinate,
                     y_coordinate, radius, ndep, providers, version, model, strategy='', center_file=None, centers=None,
                     max_radius=-1, center_function=None, radius_function=None, exp="2.5", file=None, legacy=False):

    if not centers:
        centers = []
        if center_file:
            # get centers from file
            with open(center_file, "r") as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar=',')
                for row in reader:
                    centers.append({"x": row[0], "y": row[1]})
        else:
            x_coordinate = int(x_coordinate)
            y_coordinate = int(y_coordinate)
            centers = uniform_centers_for_geography(x_coordinate, y_coordinate, 100)

    contents = []
    for position in centers:
        for r in radius:
            contents.append(single_localized_attack(interdependent_network, x_coordinate, y_coordinate, x_center=position["x"],
                                    y_center=position["y"], radius=r))
    file_name = csv_title_generator("result", x_coordinate, y_coordinate, exp, n_dependence=ndep,
                                    attack_type="localized", version=version, model=model)
    if legacy:
        file_name = "legacy_{}".format(file_name)

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "test_results")
    if strategy != '':
        path = os.path.join(path, strategy)
    else:
        path = os.path.join(path, "simple_graphs")
    path = os.path.join(path, "localized_attacks")

    save_as_csv(path, file_name, contents)


def simple_radius(graph, radius, length, width):
    return radius


def random_center(graph, max_radius, x_coordinate, y_coordinate):
    x_center = numpy.random.uniform(0, max_radius)
    y_center = numpy.random.uniform(0, max_radius)
    return x_center, y_center


def uniform_centers_for_geography(width, length, amount):
    area = width*length
    square_side = int(numpy.sqrt(area/amount))
    width_cells = int(width/square_side)
    length_cells = int(length/square_side)
    centers = []
    p = 1
    for i in range(width_cells):
        x_center = (i + 0.5)*square_side
        for j in range(length_cells):
            y_center = (j+0.5)*square_side
            centers.append({"x": x_center, "y": y_center})
    return centers


def soil_value(vs30):
    return 0.322


def seismic_attacks(interdependent_network, x_coordinate, y_coordinate, ndep, version, model, seismic_data_file,
                    max_radius_km=400, centers=None, exp=2.5):

    # get physical network
    physical_net = interdependent_network.get_phys()
    # get vss30
    vs30_matrix = ip.create_values_matrix('seismic_data/m_full_map.png', 'seismic_data/map_scale2.png', 2200, 0)
    # make map
    map_obj = mp.SoilMap(vs30_matrix, soil_value, (x_coordinate, y_coordinate))
    # set soil things onto physical network
    physical_net = map_obj.assign_soil_to_points(physical_net)
    # re-set modified physical network
    interdependent_network.set_physical(physical_net)

    max_radius = km_to_coordinates_chile(max_radius_km)
    seismic_data = load_seismic_data_from_file(seismic_data_file)

    if not centers:
        x_coordinate = int(x_coordinate)
        y_coordinate = int(y_coordinate)
        centers = uniform_centers_for_geography(x_coordinate, y_coordinate, 100)

    contents = []
    for seismic_event in seismic_data:
        print("SEISMIC EVENT: {}".format(seismic_event['id']))
        for center in centers:
            x = center["x"]
            y = center["y"]
            result_dict = probabilistic_localized_attack(interdependent_network, x, y, max_radius,
                                           seismic_probability_function_chile,
                                           seismic_event)
            contents.append(result_dict)

    file_name = csv_title_generator("result", x_coordinate, y_coordinate, exp, n_dependence=ndep,
                                    attack_type="seismic", version=version, model=model)
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "test_results")
    path = os.path.join(path, "seismic")
    save_as_csv(path, file_name, contents)


def load_seismic_data_from_file(seismic_data_file):
    data_dict = sdp.load_from_csv(seismic_data_file)
    seismic_data_list = []
    for event_id in data_dict.keys():
        event = data_dict[event_id][0]
        seismic_event = {"magnitude": event['Magnitude'],
                         "depth": event['Depth'],
                         "event_type": event['Fault Type'],
                         "id": event_id}
        seismic_data_list.append(seismic_event)
    return seismic_data_list


def probabilistic_localized_attack(interdependent_network, x_center, y_center, max_radius, probability_function, param):
    # probability function determines whether a node is removed or not given the conditions
    # param contains other necessary info for the probability_function to work
    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interdep_graph = interdependent_network.get_interd()
    param["epicenter"] = {"x": x_center, "y": y_center}

    # Get nodes to attack
    nodes_to_attack = []  # name list

    for vertex in physical_network.vs:
        x = vertex["x_coordinate"]
        y = vertex["y_coordinate"]

        # if within maximum radius
        if ((x - x_center) ** 2) + ((y - y_center) ** 2) <= max_radius ** 2:
            # call probability function to know whether to remove the node or not
            if probability_function(vertex, param):
                nodes_to_attack.append(vertex["name"])
    # Create copy from original - why tho?
    graph_copy = InterdependentGraph()
    graph_copy.create_from_graph(logic_network, logic_suppliers, physical_network, phys_suppliers, interdep_graph)

    # attack:
    graph_copy.attack_nodes(nodes_to_attack)
    g_l = graph_copy.get_ratio_of_funtional_nodes_in_AS_network()
    aux_str = "["
    for n in nodes_to_attack:
        aux_str += "{}.".format(n)
    aux_str = aux_str[0:(len(aux_str) - 1)] + "]"

    result_dict = {"x_center": x_center,
                   "y_center": y_center,
                   "GL": g_l,
                   "radius": max_radius,
                   "magnitude": param["magnitude"],
                   "depth": param["depth"],
                   "event_type": param["event_type"],
                   "nodes_removed": aux_str}
    return result_dict


def seismic_probability_function_chile(vertex, params):
    vertex_x = vertex["x_coordinate"]
    vertex_y = vertex["y_coordinate"]
    epicenter_x = params["epicenter"]["x"]
    epicenter_y = params["epicenter"]["y"]
    R_c = numpy.sqrt(((vertex_x - epicenter_x) ** 2) + ((vertex_y - epicenter_y) ** 2))
    R = coordinates_to_km_chile(R_c)
    St_t = vertex["soil"]
    Vs30 = vertex["vs30"]
    Mw = params["magnitude"]
    H = params["depth"]
    Feve = params["event_type"]


    pga_value = get_chile_pga(Mw,H,Feve, R, St_t, Vs30) #(Mw, H, Feve, R, St_t, Vs30)

    # Usar SHINDO scale para las probabilidades
    # notar que la escala no va a ser lineal
    failure_probability = shindo_scale_probability(pga_value)

    return random.uniform(0, 1) <= failure_probability


def shindo_scale_probability(pga):
    gravity_acceleration = 9.8
    ms_pga = pga * gravity_acceleration
    tiers = {#"0": (0, 0.008),
             #"1": (0.008, 0.025),
             #"2": (0.025, 0.08),
             #"3": (0.08,0.25),
             "4": [(0.025, 0.80), (0.01, 0.1)], # delta = 0.55 -> 0.8 m/s => 10% damage probability
             "5-": [(0.8, 1.4),(0.1,0.2)], # delta = 0.6 -> 1.4 m/s => 20% damage probability
             "5+": [(1.4, 2.5),(0.2,0.5)], # delta = 1.1 -> 2.5 m/s => 50% damage probability
             "6-": [(2.5, 3.15),(0.5,0.85)], # delta = 0.65 -> 3.15 m/s => 85% damage probability
             "6+": [(3.15, 4),(0.85,1)], #delta = 0.85 -> 4 m/s => 100% damage probability
             "7": [(4, float('inf')),(1,1)]}

    for tier_number in tiers:
        if tiers[tier_number][0][0] <= ms_pga < tiers[tier_number][0][1]:
            point_1 = (tiers[tier_number][0][0],tiers[tier_number][1][0])
            point_2 = (tiers[tier_number][0][1],tiers[tier_number][1][1])
            prob_value = two_point_line_eq(ms_pga, point_1, point_2)
            return prob_value
    return 0


def two_point_line_eq(x, point_1, point_2):
    x1 = point_1[0]
    y1 = point_1[1]
    x2 = point_2[0]
    y2 = point_2[1]
    return (y2 - y1) * ((x - x1)/(x2 - x1)) + y1


def get_chile_pga(Mw, H, Feve, R, St_t, Vs30):
    c1 = -2.8548
    c2 = 0.7741
    c3 = -0.97558
    c4 = 0.1
    c5 = -0.00174
    c6 = 5
    c7 = 0.35
    c8 = 0.00586
    c9 = -0.03958
    delta_c1 = 2.5699
    delta_c2 = -0.4761
    delta_c3 = -0.52745
    h0 = 50  # 50 km
    Mr = 5
    Vref = 1530  # 1530 m/s

    if Feve == 0:
        delta_fm = c9 * (Mw ** 2)
    else:
        delta_fm = delta_c1 + delta_c2 * Mw

    Ff = c1 + c2*Mw + c8*(H - h0)*Feve + delta_fm

    g = (c3 + c4*(Mw - Mr) + delta_c3*Feve)
    R0 = ((1 - Feve)*c6 * 10**(c7*(Mw - Mr)))

    Fd = g*numpy.log10(R + R0) + c5*R

    Fs = St_t*numpy.log10((Vs30+0.00000000000001)/Vref)

    log10_pga = Ff + Fd + Fs

    pga = 10 ** log10_pga
    return pga


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

def parse_interlink_network(interlinks_graph, phys_name_by_index, logic_name_by_index):
    name_by_index = []
    roseta_phys = {}
    roseta_logic = {}
    for i in range(len(interlinks_graph.vs)):
        node_name = interlinks_graph.vs[i]['name']
        name_by_index.append(node_name)
        if is_logical_node(node_name):
            roseta_logic[node_name] = logic_name_by_index.index(node_name)
        else:
            roseta_phys[node_name] = phys_name_by_index.index(node_name)

    #paths_for_each_node = []
    #for i in range(len(interlinks_graph.vs)):
    #    current_node_paths = interlinks_graph.get_all_simple_paths(i, cutoff=1)
    #    paths_for_each_node.append(current_node_paths)

    return name_by_index, roseta_phys, roseta_logic#, paths_for_each_node


def is_logical_node(node_name):
    return node_name[0] == 'l'


def get_name_by_index(network):
    name_by_index = []
    for i in range(len(network.vs)):
        name_by_index.append(network.vs[i]['name'])
    return name_by_index


def get_roseta_from_network(network):
    roseta = {}
    for i in range(len(network.vs)):
        node_name = network.vs[i]['name']
        roseta[node_name] = i
    return roseta


def network_with_deleted_nodes(network, nodes_to_delete):
    network_copy = network.copy()
    network_copy.delete_vertices(nodes_to_delete)
    return network_copy


def attack_nodes_test(phys_name_by_index, logic_name_by_index, intern_name_by_index, physical_graph, phys_providers,
                      inter_roseta_phys, inter_roseta_logic, phys_nodes_to_delete, physical_roseta, logic_roseta,
                      logic_graph, logic_providers, interlink_graph, inner_inter_roseta, logic_nodes_to_delete=[],
                      verbose=False):
    n_phys_nodes = len(phys_name_by_index)
    n_logic_nodes = len(logic_name_by_index)
    n_inter_nodes = len(intern_name_by_index)

    phys_input = [True for i in range(n_phys_nodes)]
    logic_input = [True for i in range(n_logic_nodes)]
    inter_input = [True for i in range(n_inter_nodes)]
    current_phys_nodes_to_delete = []
    current_logic_nodes_to_delete = []

    for pnode in phys_nodes_to_delete:
        phys_input[physical_roseta[pnode]] = False

    for lnode in logic_nodes_to_delete:
        logic_input[lnode] = False

    all_delta = [[], [], [], [], [], [], [], [], [], []]
    all_loop_time = []

    amp = 10000000
    while True:
        # if there are no more nodes to delete, i.e, the network has stabilized, then stop
        if phys_nodes_to_delete == current_phys_nodes_to_delete and\
                logic_nodes_to_delete == current_logic_nodes_to_delete:
            break
        timestamp_1 = time.time()
        phys_nodes_to_delete = current_phys_nodes_to_delete.copy()
        logic_nodes_to_delete = current_logic_nodes_to_delete.copy()
        timestamp_2 = time.time()
        delta_1 = (timestamp_2 - timestamp_1) * amp
        all_delta[0].append(delta_1)

        # Delete the nodes to delete on each network, including the interactions network

        for pnode in phys_nodes_to_delete:
            phys_input[pnode] = False

        for lnode in logic_nodes_to_delete:
            logic_input[lnode] = False
        timestamp_3 = time.time()
        delta_2 = (timestamp_3 - timestamp_2) * amp
        all_delta[1].append(delta_2)
        # Delete all nodes that fail because they don't have connection to a provider on each network including
        # interactions network
        for inode in range(n_inter_nodes):
            inode_name = intern_name_by_index[inode]
            if inode_name in inter_roseta_logic.keys():
                l_index = inter_roseta_logic[inode_name]
                inter_input[inode] = logic_input[l_index]
            else:
                p_index = inter_roseta_phys[inode_name]
                inter_input[inode] = phys_input[p_index]
        timestamp_4 = time.time()
        delta_3 = (timestamp_4 - timestamp_3) * amp
        all_delta[2].append(delta_3)

        # Determine all nodes that fail because they don't have connection to a provider
        # physical
        while True:
            phys_input_old = phys_input.copy()
            phys_input = get_physical_nodes_lost_by_cc(physical_graph, phys_input,  phys_providers, physical_roseta)
            if phys_input_old == phys_input:
                break
        timestamp_5 = time.time()
        delta_4 = (timestamp_5 - timestamp_4) * amp
        all_delta[3].append(delta_4)

        # logical
        while True:
            logic_input_old = logic_input.copy()
            logic_input = get_physical_nodes_lost_by_cc(logic_graph, logic_input, logic_providers, logic_roseta)
            if logic_input == logic_input_old:
                break
        timestamp_6 = time.time()
        delta_5 = (timestamp_6 - timestamp_5) * amp
        all_delta[4].append(delta_5)
        # interlink
        while True:
            inter_input_old = inter_input.copy()
            inter_input = remove_isolated_nodes_from_inter(interlink_graph, inter_input, inner_inter_roseta)
            if inter_input == inter_input_old:
                break

        timestamp_7 = time.time()
        delta_6 = (timestamp_7 - timestamp_6)*amp
        all_delta[5].append(delta_6)
        # update lists of nodes lost
        # Add them to the nodes to delete on the next iteration
        current_phys_nodes_to_delete_dict = set()
        current_logic_nodes_to_delete_dict = set()
        for pnode in range(n_phys_nodes):
            if not phys_input[pnode]:
                current_phys_nodes_to_delete_dict.add(pnode)
        timestamp_8 = time.time()
        delta_7 = (timestamp_8 - timestamp_7)*amp
        all_delta[6].append(delta_7)
        for lnode in range(n_logic_nodes):
            if not logic_input[lnode]:
                current_logic_nodes_to_delete_dict.add(lnode)
        timestamp_9 = time.time()
        delta_8 = (timestamp_9 - timestamp_8)*amp
        all_delta[7].append(delta_8)
        for inode in range(n_inter_nodes):
            if not inter_input[inode]:
                inode_name = intern_name_by_index[inode]
                if inode_name in inter_roseta_logic.keys():
                    l_index = inter_roseta_logic[inode_name]
                    current_logic_nodes_to_delete_dict.add(l_index)
                else:
                    p_index = inter_roseta_phys[inode_name]
                    current_phys_nodes_to_delete_dict.add(p_index)
        timestamp_10 = time.time()
        delta_9 = (timestamp_10 - timestamp_9)*amp
        all_delta[8].append(delta_9)
        current_phys_nodes_to_delete = list(current_phys_nodes_to_delete_dict)
        current_logic_nodes_to_delete = list(current_logic_nodes_to_delete_dict)
        timestamp_11 = time.time()
        delta_10 = (timestamp_11 - timestamp_10)*amp
        all_delta[9].append(delta_10)

        delta_loop = (timestamp_11 - timestamp_1)*amp
        all_loop_time.append(delta_loop)
    if verbose:
        print("Total loops: {}".format(len(all_loop_time)))
        for i in range(10):
            print("--- Average time in segment {}: {}".format(i+1, numpy.average(all_delta[i])))

    return logic_nodes_to_delete


def get_physical_nodes_lost_by_cc(physical_graph, phys_input, providers, phys_roseta):
    new_lost_nodes = []
    physical_graph_copy = physical_graph.copy()
    phys_input_copy = phys_input.copy()
    nodes_to_delete = [i for i in range(len(phys_input)) if not phys_input[i]]

    physical_graph_copy.delete_vertices(nodes_to_delete)
    clusters = physical_graph_copy.clusters()
    for c in clusters:
        is_alive = False
        name_c = physical_graph_copy.vs[c]['name']
        if len(name_c) > len(providers):
            for sup in providers:
                if sup in name_c:
                    is_alive = True
                    break
        elif len(name_c) > 1:
            for node in name_c:
                if node in providers:
                    is_alive = True
                    break
        else:
            is_alive = False
        if not is_alive:
            new_lost_nodes = new_lost_nodes + name_c
    for node in new_lost_nodes:
        index = phys_roseta[node]
        phys_input_copy[index] = False
    return phys_input_copy


def remove_isolated_nodes_from_inter(inter_graph, inter_input, inter_roseta):
    new_lost_nodes = []
    inter_graph_copy = inter_graph.copy()
    inter_input_copy = inter_input.copy()
    nodes_to_delete = [i for i in range(len(inter_input)) if not inter_input[i]]

    inter_graph_copy.delete_vertices(nodes_to_delete)
    clusters = inter_graph_copy.clusters()
    for c in clusters:
        named_c = inter_graph_copy.vs[c]['name']
        if len(named_c) < 2:
            new_lost_nodes = new_lost_nodes + named_c
    for node in new_lost_nodes:
        index = inter_roseta[node]
        inter_input_copy[index] = False
    return inter_input_copy