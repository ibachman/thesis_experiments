# la idea es usar esto para ver si el nuevo "attack nodes" funciona
from interdependent_network_library import *
import random
import datetime
import numpy


def check_paths(paths, minput):
    for path in paths:
        if check_if_path_working(path, minput):
            return True
    return len(paths) == 0


def check_if_path_working(path, minput):
    for node in path:
        if not minput[node]:
            return False
    return True


def get_all_paths_to_providers(graph, providers):
    paths_for_each_node = []
    for i in range(len(graph.vs)):
        current_node_paths = []
        for provider in providers:
            simple_paths = graph.get_all_simple_paths(i, to=provider)
            current_node_paths = current_node_paths + simple_paths
        paths_for_each_node.append(current_node_paths)
    return paths_for_each_node


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


def get_physical_nodes_lost_by_sp(physical_graph, phys_input, providers, phys_roseta):
    physical_graph_copy = physical_graph.copy()
    phys_input_copy = phys_input.copy()
    nodes_to_delete = [i for i in range(len(phys_input)) if not phys_input[i]]

    physical_graph_copy.delete_vertices(nodes_to_delete)

    nodes_without_provider_access = set(range(len(physical_graph_copy.vs)))
    alive_nodes = physical_graph_copy.vs['name']
    for provider_node in providers:
        if provider_node not in alive_nodes:
            continue
        # print provider_node, "is alive"
        shortest_paths_from_provider = physical_graph_copy.shortest_paths(provider_node)[0]
        zipped_path_length_to_node_index = zip(shortest_paths_from_provider, range(len(physical_graph_copy.vs)))
        unreachable_nodes_from_provider = [a[1] for a in zipped_path_length_to_node_index if a[0] == float('inf')]
        current_nodes_without_provider_access = set(unreachable_nodes_from_provider)
        nodes_without_provider_access = nodes_without_provider_access.intersection(current_nodes_without_provider_access)
    names_of_nodes_lost = set(physical_graph_copy.vs(list(nodes_without_provider_access))['name'])
    new_lost_nodes = list(names_of_nodes_lost)
    for node in new_lost_nodes:
        index = phys_roseta[node]
        phys_input_copy[index] = False
    return phys_input_copy


def network_with_deleted_nodes(network, nodes_to_delete):
    network_copy = network.copy()
    network_copy.delete_vertices(nodes_to_delete)
    return network_copy


def attack_nodes_test(phys_name_by_index, logic_name_by_index, intern_name_by_index, physical_graph, phys_providers,
                      inter_roseta_phys, inter_roseta_logic, phys_nodes_to_delete, physical_roseta, logic_roseta,
                      logic_graph, logic_providers, interlink_graph, inner_inter_roseta, logic_nodes_to_delete=[]):
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
    print("Total loops: {}".format(len(all_loop_time)))
    for i in range(10):
        print("--- Average time in segment {}: {}".format(i+1, numpy.average(all_delta[i])))

    return logic_nodes_to_delete


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


def parse_inner_network(network, providers):
    #node_paths_to_providers = get_all_paths_to_providers(network, providers)
    name_by_index = get_name_by_index(network)
    return name_by_index#, node_paths_to_providers


def get_roseta_from_network(network):
    roseta = {}
    for i in range(len(network.vs)):
        node_name = network.vs[i]['name']
        roseta[node_name] = i
    return roseta


def get_list_of_nodes_to_attack(sample, start, stop):
    full_list = []
    for i in range(start, stop):
        list_of_nodes_to_attack = random.sample(sample, i)
        full_list.append(list_of_nodes_to_attack)
    return full_list


def old_attack_nodes(interdependent_network, iter_number, list_of_nodes_to_attack, process_name="debug",
                     network_to_attack="phys"):
    print("Started at {}".format(datetime.datetime.now()))
    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interlink_graph = interdependent_network.get_interlinks()
    n_phys = len(physical_network.vs)
    n_logic = len(logic_network.vs)
    iteration_results = []

    for j in range(1, n_phys + n_logic):
        iteration_results.append([])
    if network_to_attack == "logic":
        samp = logic_network.vs["name"]
        iteration_range = n_logic
    else:
        samp = physical_network.vs["name"]
        iteration_range = n_phys
    for j in range(iter_number):
        print(" -------> [[{}]] -- {} -- iteration: {}".format(datetime.datetime.now(), process_name, (j + 1)))
        for i in range(1, min(iteration_range, len(list_of_nodes_to_attack)+1)):
            graph_copy = InterdependentGraph()
            graph_copy.create_from_graph(logic_network, logic_suppliers, physical_network, phys_suppliers,
                                         interlink_graph)

            while True:
                try:
                    graph_copy.attack_nodes(list_of_nodes_to_attack[i-1])
                    break
                except RandomAttackTimeoutError:
                    print("*** TIMEOUT FOR ITERATION {} - {} *** [[{}]]".format(((j + 1), i), process_name,
                                                                                datetime.datetime.now()))
                    print("*** {} ***".format(list_of_nodes_to_attack))
                    pass
                except Exception as e:
                    print("*** ERROR IN ATTACK NODES {} ***".format(e.__class__))
                    pass

            iteration_results[(i - 1)].append(graph_copy.get_ratio_of_funtional_nodes_in_AS_network())

    print("Ended at {}".format(datetime.datetime.now()))
    return iteration_results


def new_attack_nodes(interdependent_network, iter_number, list_of_nodes_to_attack, network_to_attack="phys",
                     process_name="debug"):
    print("Started at {}".format(datetime.datetime.now()))
    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interlink_graph = interdependent_network.get_interlinks()

    print("Collecting data")
    logic_name_by_index = get_name_by_index(logic_network)
    print("... 1 ")
    physical_roseta = get_roseta_from_network(physical_network)
    logical_roseta = get_roseta_from_network(logic_network)
    inner_inter_roseta = get_roseta_from_network(interlink_graph)
    print("... 2 ")
    phys_name_by_index = get_name_by_index(physical_network)
    print("... 3 ")
    intern_name_by_index, inter_roseta_phys, inter_roseta_logic = parse_interlink_network(interlink_graph,
                                                                                          phys_name_by_index,
                                                                                          logic_name_by_index)
    print("... End collection ")

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
        for i in range(1, min(iteration_range, len(list_of_nodes_to_attack)+1)):
            #print("({}) -- {}".format(i, datetime.datetime.now()))
            logic_nodes_deleted = attack_nodes_test(phys_name_by_index, logic_name_by_index, intern_name_by_index,
                                                    physical_network, phys_suppliers, inter_roseta_phys,
                                                    inter_roseta_logic, list_of_nodes_to_attack[i - 1], physical_roseta,
                                                    logical_roseta, logic_network, logic_suppliers, interlink_graph,
                                                    inner_inter_roseta)
            iteration_results[(i - 1)].append((n_logic - len(logic_nodes_deleted))/n_logic)

            net = network_with_deleted_nodes(logic_network, logic_nodes_deleted)
            functional_nodes = [a for a in net.vs if net.degree(a.index) > 0]
            functional_nodes_in_AS_net = len(functional_nodes)
            print((functional_nodes_in_AS_net * 1.0) / (n_logic * 1.0))
            print("*** {}".format(functional_nodes))

    print("Ended at {}".format(datetime.datetime.now()))
    return iteration_results

