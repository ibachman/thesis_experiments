import random
import math
import numpy as np
from interdependent_network_library import *
import datetime
__author__ = 'ivana'


def generate_physical_network(n, model, coord_dict, space=(100, 100), recursive=True):
    x = 0
    y = 1
    # establish neighbourhoods
    node_connections = []
    if model == "RNG":
        for i in range(n):
            for j in range(i+1, n):
                # node i data
                node_i_name = "p{}".format(i)
                loc_node_i = (coord_dict[node_i_name][x], coord_dict[node_i_name][y])

                # node j data
                node_j_name = "p{}".format(j)
                loc_node_j = (coord_dict[node_j_name][x], coord_dict[node_j_name][y])

                nodes_distance = get_distance(loc_node_i, loc_node_j)
                can_connect = True
                if nodes_distance > 0:
                    for k in range(n):
                        if k is not i and k is not j:
                            # node k data
                            node_k_name = "p{}".format(k)
                            loc_node_k = (coord_dict[node_k_name][x], coord_dict[node_k_name][y])

                            i_k_distance = get_distance(loc_node_i, loc_node_k)
                            j_k_distance = get_distance(loc_node_k, loc_node_j)

                            if i_k_distance < nodes_distance and j_k_distance < nodes_distance:
                                can_connect = False
                                break
                if can_connect:
                    node_connections.append((node_i_name, node_j_name))

    elif model == "GG":
        for i in range(n):
            for j in range(i + 1, n):
                # node i data
                node_i_name = "p{}".format(i)
                loc_node_i = (coord_dict[node_i_name][x], coord_dict[node_i_name][y])

                # node j data
                node_j_name = "p{}".format(j)
                loc_node_j = (coord_dict[node_j_name][x], coord_dict[node_j_name][y])

                center = ((loc_node_i[x] + loc_node_j[x]) / 2, (loc_node_i[y] + loc_node_j[y]) / 2)

                radius = get_distance(loc_node_i, loc_node_j)/2
                can_connect = True

                # check if there is a node in the circular area defined by 'center' and 'radius'
                for k in range(n):
                    if k != i and k != j:
                        # node k data
                        node_k_name = "p{}".format(k)
                        loc_node_k = (coord_dict[node_k_name][x], coord_dict[node_k_name][y])

                        if get_distance(center, loc_node_k) < radius:
                            can_connect = False
                            break

                if can_connect:
                    node_connections.append((node_i_name, node_j_name))

    elif len(model) == 3 and "NN" in model:
        number_of_neighbors = int(model[0])
        for i in range(n):
            # node i data
            node_i_name = "p{}".format(i)
            loc_node_i = (coord_dict[node_i_name][x], coord_dict[node_i_name][y])

            closest_to_i = []
            for j in range(n):
                if j == i:
                    continue
                # node j data
                node_j_name = "p{}".format(j)
                loc_node_j = (coord_dict[node_j_name][x], coord_dict[node_j_name][y])

                closest_to_i.append((get_distance(loc_node_i, loc_node_j), j))

            closest_to_i.sort(key=lambda tup: tup[0])
            for w in range(number_of_neighbors + 1):
                k = closest_to_i[w][1]
                if i < k:
                    j = k
                else:
                    j = i
                    i = k

                if ("p{}".format(i), "p{}".format(j)) not in node_connections:
                    node_connections.append(("p{}".format(i), "p{}".format(j)))

    elif model == "YAO":
        for i in range(n):
            # node i data
            node_i_name = "p{}".format(i)
            loc_node_i = (coord_dict[node_i_name][x], coord_dict[node_i_name][y])

            area_buckets = {(0, 60): {'distance': np.infty, 'closest_node': -1},
                            (60, 120): {'distance': np.infty, 'closest_node': -1},
                            (120, 180): {'distance': np.infty, 'closest_node': -1},
                            (0, -60): {'distance': np.infty, 'closest_node': -1},
                            (-60, -120): {'distance': np.infty, 'closest_node': -1},
                            (-120, -180): {'distance': np.infty, 'closest_node': -1}}

            for j in range(n):
                if j == i:
                    continue
                # node j data
                node_j_name = "p{}".format(j)
                loc_node_j = (coord_dict[node_j_name][x], coord_dict[node_j_name][y])

                distance = get_distance(loc_node_i, loc_node_j)
                angle = get_angle(loc_node_i, loc_node_j)
                for area in area_buckets.keys():
                    if area[0] == 0 and area[1] == 60:
                        if area[0] <= angle <= area[1]:
                            if distance < area_buckets[area]['distance']:
                                area_buckets[area]['distance'] = distance
                                area_buckets[area]['closest_node'] = node_j_name
                            break
                    else:
                        if area[0] < angle <= area[1]:
                            if distance < area_buckets[area]['distance']:
                                area_buckets[area]['distance'] = distance
                                area_buckets[area]['closest_node'] = node_j_name
                            break

            for area in area_buckets.keys():
                candidate_node = area_buckets[area]['closest_node']
                if candidate_node != -1:
                    cand_node_index = int(candidate_node.replace("p", ""))
                    if i < cand_node_index:
                        new_edge = (node_i_name, candidate_node)
                    else:
                        new_edge = (candidate_node, node_i_name)
                    if new_edge not in node_connections:
                        node_connections.append(new_edge)
    elif model == "GPA":
        m = 50  # edges added in each iteration
        alpha = 0.0002
        t = 0
        radx = space[x] * math.sqrt(math.log10(n)) / math.pow(n, 0.4)  # The value 0.425 can be changed.
        rady = (space[y] / space[x]) * radx
        areaR = math.pi * radx * rady
        # V contains vertices at step t
        V = {}
        # E contains edges at step t
        E = {}
        # deg at step t
        deg = {}
        # G_0 is the empty graph (no edges, all nodes)
        E[0] = []
        V[0] = ["p{}".format(x) for x in list(range(n))]
        deg[0] = {}
        for u in V[0]:
            deg[0][u] = 0

        for i in range(n):
            t += 1

            deg[t] = {}
            node_i_name = "p{}".format(i)
            loc_node_i = (coord_dict[node_i_name][x], coord_dict[node_i_name][y])

            # close_nodes = B_r(x_{t+1})
            close_nodes = []
            # sum_degrees = D_t(x_t)
            sum_degrees = 0
            # node i data

            for j in range(n):
                # node j data
                node_j_name = "p{}".format(j)
                loc_node_j = (coord_dict[node_j_name][x], coord_dict[node_j_name][y])

                # get B_r(x_{t+1})
                if is_within_elliptical_area(loc_node_i, loc_node_j, radx, rady):
                    # close_nodes = B_r(x_{t+1})
                    close_nodes.append(node_j_name)

            # get V_t(x_t) = V_t intersec B_r(x_{t+1})
            V_t_x_t_1 = [x for x in V[t - 1] if x in close_nodes]

            # get D_t(x_t)
            for node_v in V_t_x_t_1:
                # sum_degrees = Dt(xt)
                sum_degrees += deg[t-1][node_v]

            # prob of adding edge (x_t_1, y_i)
            prob_of_connecting_with = {}
            for node_v in V_t_x_t_1:
                if node_v == node_i_name:
                    continue
                # Pr(y_i = v)
                prob = deg[t - 1][node_v] / max(sum_degrees, alpha * m * areaR * t)*1.0
                prob_of_connecting_with[node_v] = prob
            prob_of_connecting_with[node_i_name] = 1 - sum_degrees / max(sum_degrees, alpha * m * areaR * t)*1.0

            # get 'm' edges
            aux_node_list = []
            aux_prob_list = []
            for node_v in V_t_x_t_1:
                aux_node_list.append(node_v)
                aux_prob_list.append(prob_of_connecting_with[node_v])
            y_i_list = random.choices(aux_node_list, aux_prob_list, k=m)
            V[t] = V[t-1]
            for u in V[t]:
                deg[t][u] = deg[t - 1][u]

            E[t] = E[t-1]
            for y_i in y_i_list:
                E[t].append((y_i, node_i_name))
                deg[t][y_i] += deg[t-1][y_i] + 1
                deg[t][node_i_name] += deg[t - 1][node_i_name] + 1

        distinct_edges_dict = {}
        for tuple in E[t]:
            node_i = int(tuple[x].replace("p", ""))
            node_j = int(tuple[y].replace("p", ""))
            if node_i < node_j:
                new_edge = tuple
            elif node_j < node_i:
                new_edge = (tuple[y], tuple[x])
            else:
                continue
            distinct_edges_dict[new_edge] = ""

        keyslist = list(distinct_edges_dict.keys())

        node_connections = keyslist

    elif "ER":
        # in ER networks edges do not depend of the node allocation
        node_connections = []
        for i in range(n):
            node_i_name = 'p{}'.format(i)
            for j in range(i+1, n):
                node_j_name = 'p{}'.format(j)
                rand_val = random.uniform(0, 1)

                if rand_val < (math.log(n) / n):
                    node_connections.append((node_i_name, node_j_name))

    # set nodes ids
    id_list = []
    cord = []
    for i in range(n):
        node_i_name = "p{}".format(i)
        id_list.append(node_i_name)
        loc = (coord_dict[node_i_name][x], coord_dict[node_i_name][y])
        cord.append(loc)

    # generate igraph graph
    graph = igraph.Graph(n)
    graph.vs['name'] = id_list
    graph.vs['loc'] = cord

    graph.add_edges(node_connections)
    if model == "GPA" or model == "ER" and recursive:
        number_of_connected_components = len(graph.clusters())
        if number_of_connected_components > 1:
            while number_of_connected_components > 1:
                graph = generate_physical_network(n, model, coord_dict, space=space, recursive=False)
                number_of_connected_components = len(graph.clusters())
                print(number_of_connected_components)
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


def set_logic_suppliers(logic_network_nodes_ids, n_logic_suppliers):

    return random.sample(logic_network_nodes_ids, n_logic_suppliers)


def generate_logic_network(n, exponent=2.5):
    graph = generate_power_law_graph(n, exponent, 1.0)
    id_list = []
    for i in range(n):
        id_list.append('l'.format(i))
    graph.vs['name'] = id_list
    return graph


def set_physical_suppliers(interlink_network, logic_suppliers):
    interlink_network_ids = interlink_network.vs['name']
    supplier_list = []
    for name in logic_suppliers:
        nodes_name_neighbors = interlink_network.neighbors(name)
        for i in nodes_name_neighbors:
            supplier_list.append(interlink_network_ids[i])
    return supplier_list


def set_interdependencies(physical_network_nodes_ids, logic_network_nodes_ids, max_number_of_interdependencies,
                          as_suppliers, mode="semi random"):
    connections = []
    physical_nodes_included = {}
    all_supplier_counterparts = {}
    non_supplier_logic_nodes = [x for x in logic_network_nodes_ids if x not in as_suppliers]
    inter_degree_list = []
    if mode == "semi random":
        # get a list of "interdegrees" try to give the highest degrees to the supliers and then random
        for p in range(len(logic_network_nodes_ids)):
            inter_degree_list.append(random.randint(1, max_number_of_interdependencies))
        print("len interdegree list: {}".format(len(inter_degree_list)))
        # count amount of nodes with max(interdegree)
        number_of_logic_nodes_with_max_interd = inter_degree_list.count(max_number_of_interdependencies)

        print("number_of_logic_nodes_with_max_interd = {}".format(number_of_logic_nodes_with_max_interd))
        # make suppliers have the maximum amount of interlinks possible
        k = -1
        current_max_inter_degree = max_number_of_interdependencies

        while k != (len(as_suppliers) - 1):

            for k in range(k+1, min(number_of_logic_nodes_with_max_interd, len(as_suppliers))):

                # attach logic nodes to counterparts
                logic_node = as_suppliers[k]
                # assign max interdegree
                amount_of_neighbours = current_max_inter_degree
                # remove max deg occurence
                inter_degree_list.remove(current_max_inter_degree)
                # get physical counterparts
                physical_neighbors = random.sample(physical_network_nodes_ids, amount_of_neighbours)
                for physical_node in physical_neighbors:
                    # set the connections in the connection list by id
                    connections.append((logic_node, physical_node))
                    # only include non-isolated nodes from the physical network
                    physical_nodes_included[physical_node] = physical_node
                    all_supplier_counterparts[physical_node] = ""

            if current_max_inter_degree > 1:
                current_max_inter_degree -= 1
                number_of_logic_nodes_with_max_interd = inter_degree_list.count(current_max_inter_degree)

        print("len phys suppliers: {}".format(len(list(all_supplier_counterparts.keys()))))
        # add rest of interlinks

    if mode == "provider priority":
        used_physical_nodes = []
        physical_nodes_left = [x for x in physical_network_nodes_ids if x not in used_physical_nodes]
        for logic_supplier in as_suppliers:

            physical_neighbors = random.sample(physical_nodes_left, max_number_of_interdependencies)
            used_physical_nodes += physical_neighbors
            for physical_node in physical_neighbors:
                # set the connections in the connection list by id
                connections.append((logic_supplier, physical_node))
                # only include non-isolated nodes from the physical network
                physical_nodes_included[physical_node] = physical_node
                all_supplier_counterparts[physical_node] = ""
            physical_nodes_left = [x for x in physical_network_nodes_ids if x not in used_physical_nodes]

        print("len phys suppliers: {}".format(len(list(all_supplier_counterparts.keys()))))
        print("physical nodes left: {}".format(len(physical_nodes_left)))

        for p in range(len(physical_nodes_left)):
            inter_degree_list.append(random.randint(1, max_number_of_interdependencies))

    if mode == "full random":
        non_supplier_logic_nodes = logic_network_nodes_ids
        for p in range(len(logic_network_nodes_ids)):
            inter_degree_list.append(random.randint(1, max_number_of_interdependencies))

    print("len(non_supplier_logic_nodes) = {}".format(len(non_supplier_logic_nodes)))
    # for each logic node select an x between 1 and max_number_of_interdependencies
    for index in range(len(non_supplier_logic_nodes)):
        amount_of_neighbours = inter_degree_list[index]
        logic_node = non_supplier_logic_nodes[index]

        # select x nodes from the physical network at random
        for i in range(amount_of_neighbours):
            physical_node_index = random.randint(0, len(physical_network_nodes_ids) - 1)
            physical_node = physical_network_nodes_ids[physical_node_index]

            # set the connections in the connection list by id
            connections.append((logic_node, physical_node))

            # only include non-isolated nodes from the physical network
            physical_nodes_included[physical_node] = physical_node

            if logic_node in as_suppliers:
                all_supplier_counterparts[physical_node] = ""
    if mode == "full random":
        print("len phys suppliers: {}".format(len(list(all_supplier_counterparts.keys()))))

    # create the graph
    graph = igraph.Graph(len(logic_network_nodes_ids) + len(physical_nodes_included.values()))
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


def get_distance(point_1, point_2):
    x = 0
    y = 1
    x1 = point_1[x]
    x2 = point_2[x]
    y1 = point_1[y]
    y2 = point_2[y]
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))


def get_angle(point_1, point_2):
    x = 0
    y = 1
    x1 = point_1[x]
    x2 = point_2[x]
    y1 = point_1[y]
    y2 = point_2[y]
    oc = (y2-y1)
    ac = (x2-x1)
    return math.atan2(oc, ac)*180/math.pi


def is_within_elliptical_area(point_1, point_2, radius_x, radius_y):
    x = 0
    y = 1
    dif_x = point_1[x] - point_2[x]
    dif_y = point_1[y] - point_2[y]
    return ((dif_x * dif_x) / (radius_x * radius_x) + (dif_y * dif_y) / (radius_y * radius_y)) <= 1

