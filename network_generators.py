import random
import math
import numpy as np
from interdependent_network_library import *
import datetime
__author__ = 'ivana'


def generate_physical_network(n, model, coord_dict):

    # establish neighbourhoods
    node_connections = []
    if model == "RNG":
        print()
        for i in range(n):
            for j in range(i+1, n):
                # node i data
                node_i_name = "p{}".format(i)
                node_i_x = coord_dict[node_i_name][0]
                node_i_y = coord_dict[node_i_name][1]
                # node j data
                node_j_name = "p{}".format(j)
                node_j_x = coord_dict[node_j_name][0]
                node_j_y = coord_dict[node_j_name][1]

                nodes_distance = distance(node_i_x, node_i_y, node_j_x, node_j_y)
                can_connect = True
                if nodes_distance is not 0:
                    for k in range(n):
                        if k is not i and k is not j:
                            # node k data
                            node_k_name = "p{}".format(k)
                            node_k_x = coord_dict[node_k_name][0]
                            node_k_y = coord_dict[node_k_name][1]

                            i_k_distance = distance(node_i_x, node_i_y, node_k_x,
                                                    node_k_y)
                            j_k_distance = distance(node_k_x, node_k_y, node_j_x,
                                                    node_j_y)
                            if i_k_distance < nodes_distance and j_k_distance < nodes_distance:
                                can_connect = False
                if can_connect:
                    node_connections.append((node_i_name, node_j_name))


    elif model == "GG":
        for i in range(n):
            for j in range(i + 1, n):
                # node i data
                node_i_name = "p{}".format(i)
                node_i_x = coord_dict[node_i_name][0]
                node_i_y = coord_dict[node_i_name][1]
                # node j data
                node_j_name = "p{}".format(j)
                node_j_x = coord_dict[node_j_name][0]
                node_j_y = coord_dict[node_j_name][1]

                center_x = (node_i_x +node_j_x) / 2
                center_y = (node_i_y + node_j_y) / 2
                distance_from_center = distance(center_x, center_y, node_j_x, node_j_y)
                diameter = distance(node_i_x, node_i_y, node_j_x, node_j_y)
                can_connect = True
                if distance_from_center == 0:
                    pass
                    #print "distancia es cero entre", i, j
                if distance_from_center is not 0:
                    min_center_k_distance = 10000000000000
                    for k in range(n):
                        if k is not i and k is not j:
                            # node k data
                            node_k_name = "p{}".format(k)
                            node_k_x = coord_dict[node_k_name][0]
                            node_k_y = coord_dict[node_k_name][1]
                            diameter_1 = distance(node_i_x, node_i_y, node_k_x,
                                                  node_k_y)
                            diameter_2 = distance(node_j_x, node_j_y, node_k_x,
                                                  node_k_y)
                            if math.pow(diameter_1, 2) + math.pow(diameter_2, 2) < math.pow(diameter, 2):
                                can_connect = False
                if can_connect:
                    node_connections.append((node_i_name, node_j_name))

    elif model == "5NN":
        for i in range(n):
            # node i data
            node_i_name = "p{}".format(i)
            node_i_x = coord_dict[node_i_name][0]
            node_i_y = coord_dict[node_i_name][1]

            closest_to_i = []
            for j in range(n):
                # node j data
                node_j_name = "p{}".format(j)
                node_j_x = coord_dict[node_j_name][0]
                node_j_y = coord_dict[node_j_name][1]

                closest_to_i.append((distance(node_i_x, node_i_y, node_j_x, node_j_y), j))

            closest_to_i.sort(key=lambda tup: tup[0])
            for w in range(1, 5):
                j = closest_to_i[w][1]
                k = min(i, j)
                j = max(i, j)
                i = k
                if ("p{}".format(i), "p{}".format(j)) not in node_connections:
                    node_connections.append(("p{}".format(i), "p{}".format(j)))
    else:
        print("ERROR")

        # set nodes ids
    id_list = []
    for i in range(n):
        id_list.append("p{}".format(i))
    # generate igraph graph
    graph = igraph.Graph(n)
    graph.vs['name'] = id_list
    graph.add_edges(node_connections)

    return graph


def generate_coordinates(n, x_axis=1000, y_axis=1000):
    # establish space boundaries
    x_axis_max_value = x_axis
    y_axis_max_value = y_axis
    # randomly assign n nodes into this space
    x_coordinates = []
    y_coordinates = []
    for i in range(n):
        x_coordinates.append(random.uniform(0, x_axis_max_value))
        y_coordinates.append(random.uniform(0, y_axis_max_value))
    
    return x_coordinates, y_coordinates


def generate_edges_to_add_random(number_of_edges_to_add, graph):

    graph_complement = graph.complementer()
    edge_id_list_remove = []
    for i in range(len(graph.vs)):
        id = graph_complement.get_eid(i, i)
        edge_id_list_remove.append(id)
    graph_complement.delete_edges(edge_id_list_remove)
    new_edges_candidates = graph_complement.get_edgelist()
    index_list = random.sample(range(len(new_edges_candidates) - 1), number_of_edges_to_add)

    final_edge_list = []
    for k in index_list:
        i = new_edges_candidates[k][0]
        j = new_edges_candidates[k][1]
        i_name = graph.vs['name'][i]
        j_name = graph.vs['name'][j]
        final_edge_list.append((i_name, j_name))
    return final_edge_list


def generate_edges_to_add_distance(phys_graph, coord_dict, percentage, n, external=False, dependence_graph=None):
    """
    x_coord: List of x coordinates
    y_coord: List of y coordinates
    percentage: Percentage of nodes with minimum degree to iterate
    n: Number of edges to add
    """
    x = 0
    y = 1

    new_edges = []  
    v = phys_graph.vcount()
    number_of_nodes_to_iterate = int(v * percentage / 100)
    number_of_added_edges = 0
    ranking = []

    if external:
        print("external")
        # Make ranking by external degree
        phys_names = phys_graph.vs["name"]
        dep_degrees = dependence_graph.degree()
        dep_sorted_nodes = np.flip(np.argsort(dep_degrees), axis=0)
        for node in dep_sorted_nodes:
            if dependence_graph.vs["name"][node] in phys_names:
                # Find index in phys graph
                index = phys_names.index(dependence_graph.vs["name"][node])
                ranking.append(index)
        # Add nodes that are not connected to the logic layer
        for node in phys_graph.vs:
            if node.index not in ranking:
                ranking.append(node.index)

    while number_of_added_edges < n:
        if external:
            sorted_nodes = ranking
        else:
            degrees = phys_graph.degree()
            phys_graph.vs["degree"] = degrees
            sorted_nodes = np.flip(np.argsort(degrees), axis=0)

        for i in reversed(range(v - number_of_nodes_to_iterate, v)):
            small_degree_node = phys_graph.vs[sorted_nodes[i]]['name']
            target = float("inf")
            distance = float("inf")

            for j in range(v - number_of_nodes_to_iterate):
                candidate = phys_graph.vs[sorted_nodes[j]]['name']
                x1 = coord_dict[small_degree_node][x]#x_coord[small_degree_node]
                y1 = coord_dict[small_degree_node][y]#y_coord[small_degree_node]
                x2 = coord_dict[candidate][x]
                y2 = coord_dict[candidate][y]

                cand_distance = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

                if small_degree_node != candidate and cand_distance < distance and \
                        not phys_graph.are_connected(small_degree_node, candidate):
                    target = candidate
                    distance = cand_distance
            new_edges.append((small_degree_node, target))
            phys_graph.add_edge(small_degree_node, target)
            number_of_added_edges += 1
            if number_of_added_edges >= n:
                return new_edges 
    return new_edges


def generate_edges_to_add_degree(phys_graph, percentage, number_of_edges_to_add):
    """
    percentage: Percentage of nodes with minimun degree to iterate
    number_of_edges_to_add: Number of edges to add
    add edges from nodes with minimun degree to nodes with maximum degree
    """
    new_edges = []  
    v = phys_graph.vcount()
    number_of_nodes_to_iterate = int(v * percentage / 100)
    number_of_added_edges = 0
    while number_of_added_edges < number_of_edges_to_add:
        degrees = phys_graph.degree()
        sorted_nodes = np.flip(np.argsort(degrees), axis=0)
        
        for i in reversed(range(v - number_of_nodes_to_iterate, v)):
            small_degree_node = sorted_nodes[i]
            for j in range(v - number_of_nodes_to_iterate):
                target = sorted_nodes[j]

                if small_degree_node != target and not phys_graph.are_connected(small_degree_node, target):
                    names = phys_graph.vs['name']
                    new_edges.append((names[small_degree_node], names[target]))
                    phys_graph.add_edge(small_degree_node, target)
                    number_of_added_edges += 1
                    if number_of_added_edges >= number_of_edges_to_add :
                        return new_edges

    return new_edges


def save_edges_to_csv(edge_list, x_coordinates, y_coordinates, pg_exponent, n_dependence="", l_providers="",
                       version="", model="", strategy=""):
    title = csv_title_generator("candidates", x_coordinates, y_coordinates, pg_exponent, n_dependence,
                                l_providers, attack_type="", version=version, model=model)

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "networks", "physical_networks", "extra_edges")

    if "random" in strategy:
        full_directory = os.path.join(path, "random", title)
    elif "distance" in strategy:
        full_directory = os.path.join(path, "distance", title)
    elif "external" in strategy:
        full_directory = os.path.join(path, "external", title)
    elif "degree" in strategy:
        full_directory = os.path.join(path, "degree", title)
    else:
        full_directory = os.path.join(path, title)

    print("Saving new edges in: {}".format(full_directory))
    with open(full_directory, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(edge_list)):
            j = edge_list[i][0]
            k = edge_list[i][1]
            writer.writerow([j, k])


def set_logic_suppliers(logic_network_nodes_ids, n, n_inter, interdep_graph):
    # this method will choose logic suppliers within those nodes that are as interconnected as possible
    supplier_list = {}
    candidates_list = []
    for k in range(len(logic_network_nodes_ids)):
        k_neighbors = interdep_graph.neighborhood_size(vertices=['l'+str(k)])
        if k_neighbors == n_inter:
            candidates_list.append(k)
    max_sample = len(candidates_list)

    sample = random.sample(candidates_list, min(max_sample,n))

    for k in sample:
        supplier_list[logic_network_nodes_ids[k]] = logic_network_nodes_ids[k]

    if n > max_sample:
        for i in range(n-max_sample):
            while len(supplier_list.values()) < (i+1) :
                k = random.randint(0,len(logic_network_nodes_ids)-1)
                supplier_list[logic_network_nodes_ids[k]] = logic_network_nodes_ids[k]

    return supplier_list.values()


def generate_logic_network(n, exponent=2.7):
    graph = generate_power_law_graph(n, exponent, 1.0)
    id_list = []
    for i in range(n):
        id_list.append('l'+str(i))
    graph.vs['name'] = id_list
    return graph


def set_physical_suppliers(interdepency_network, logic_suppliers):
    interdepency_network_ids = interdepency_network.vs['name']
    supplier_list = []
    for name in logic_suppliers:
        nodes_name_neighbors = interdepency_network.neighbors(name)
        for i in nodes_name_neighbors:
            supplier_list.append(interdepency_network_ids[i])
    return supplier_list


def set_interdependencies(physical_network_nodes_ids, logic_network_nodes_ids, max_number_of_interdependencies):
    connections = []
    physical_nodes_included = {}
    # for each logic node select an x between 1 and max_number_of_interdependencies
    for logic_node in logic_network_nodes_ids:
        amount_of_neighbours = random.randint(1, max_number_of_interdependencies)
        # select x nodes from the physical network at random
        for i in range(amount_of_neighbours):
            physical_node_index = random.randint(0, len(physical_network_nodes_ids)-1)
            physical_node = physical_network_nodes_ids[physical_node_index]
            # set the connections in the connection list by id
            connections.append((logic_node,physical_node))
            # only include non-isolated nodes from the physical network
            physical_nodes_included[physical_node] = physical_node
    # create the graph
    graph = igraph.Graph(len(physical_network_nodes_ids)+len(physical_nodes_included))
    graph.vs['name'] = list(physical_nodes_included.values()) + logic_network_nodes_ids
    graph.add_edges(connections)

    return graph


def generate_erdos_renyi_graph(n):
    while True:
        try:
            g = igraph.Graph.Erdos_Renyi(n, math.log(n)/n, directed=False, loops=False)
            print("success")
            return g
        except Warning:
            pass


def generate_power_law_graph(n, lamda, epsilon):
    node_degrees = get_degrees_power_law(n, lamda)
    while True:
        try:
            g = igraph.Graph.Degree_Sequence(node_degrees, method="vl")
            print("success")
            return g
        except Exception:
            node_degrees = get_degrees_power_law(n, lamda)
            pass
        except Warning:
            pass

    # results = powerlaw.Fit(node_degrees, discrete=True)
    # alpha = results.power_law.alpha
    # diff = math.fabs(alpha - lamda)
    #
    # while True:
    #     while (diff > epsilon):
    #         node_degrees = get_degrees_power_law(n, lamda)
    #         results = powerlaw.Fit(node_degrees, discrete=True, suppress_output=True)
    #
    #         alpha = results.power_law.alpha
    #         diff = math.fabs(alpha - lamda)
    #     try:
    #         g = Graph.Degree_Sequence(node_degrees, method="vl")
    #         print "------------------------", alpha, lamda, "--------------------------"
    #         return g
    #     except Exception, e:
    #         diff = epsilon + 1
    #         pass


def get_degrees_power_law(n, lamda):
    choices = []
    for i in range(n):
        choices.append(((i + 1), math.pow((i + 1), -1.0 * lamda)))
    node_degrees = []
    for i in range(n):
        node_degrees.append(weighted_choice(choices))
    if sum(node_degrees) % 2 != 0:
        node_degrees[0] += 1
    return node_degrees


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    up_to = 0
    for c, w in choices:
        if up_to + w > r:
            return c
        up_to += w
    assert False, "Shouldn't get here"


def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))


def angle(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return math.atan(m)*180/math.pi
