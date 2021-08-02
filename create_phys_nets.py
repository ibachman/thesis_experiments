from interdependent_network_library import *
import network_generators as network_generators
from concurrent_run import parse_task_args
import numpy as np
import math
import igraph
import datetime
import operator
import os


def create_coordinates():
    space_shapes = [[20, 500], [100, 100]]
    n_phys = 2000
    exp = 2.5
    n_inter = 3
    n_logic_suppliers = 6

    for s in space_shapes:
        for version in range(1, 11):
            x_coordinate = s[0]
            y_coordinate = s[1]
            x_coord, y_coord = network_generators.generate_coordinates(n_phys, x_axis=x_coordinate, y_axis=y_coordinate)
            save_nodes_to_csv(x_coord, y_coord, x_coordinate, y_coordinate, exp, n_inter, n_logic_suppliers,
                              version=version)


def single_physical_network(model, space, version):
    n_phys = 2000
    exp = 2.5
    n_inter = 3
    n_logic_suppliers = 6
    x_coordinate = space[0]
    y_coordinate = space[1]
    # generate physical network
    coord_dir = "networks/physical_networks/node_locations/" + \
                csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version)
    coord_dict = get_list_of_coordinates_from_csv(coord_dir)
    print("---- getting coordinates from file: {}".format(coord_dir))
    print("---- Generating network {}. Start time: {}".format(model, datetime.datetime.now()))
    phys_graph = network_generators.generate_physical_network(n_phys, model, coord_dict, space=space)
    print("---- Network {} done. Start time: {}".format(model, datetime.datetime.now()))
    network_system = InterdependentGraph()
    network_system.set_physical(phys_graph)
    # Save physical
    network_system.save_physical(x_coordinate, y_coordinate, exp, version=version, model=model)


def create_physical_network(model, v=None, space_shapes=None):
    if not space_shapes:
        space_shapes = [[20, 500], [100, 100]]

    for s in space_shapes:
        if v:
            single_physical_network(model, s, v)
        else:
            for version in range(1, 11):
                single_physical_network(model, s, version)


def test_igraph():
    graph = igraph.Graph(4)
    graph.vs['name'] = ["p0", "p1", "p2", "p3"]
    graph.add_edges([("p0", "p1"), ("p1", "p2"), ("p1","p3")])
    graph.add_vertices(["p4","p5"])

    graph.add_edge("p4","p5")
    print(graph)


def get_different_nodes(csv_file):
    node_dict = {}
    node_dict_aux = {}
    interlink_flag = False
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            if row[0][0] != row[1][0]:
                interlink_flag = True
            if interlink_flag:
                node_dict[row[0]] = ""
                node_dict_aux[row[1]] = ""
            else:
                node_dict[row[0]] = ""
                node_dict[row[1]] = ""
    node_names = []
    if interlink_flag:
        node_names = list(node_dict.keys()) + list(node_dict_aux.keys())
    else:
        prefix_name = list(node_dict.keys())[0][0]
        for k in range(len(node_dict.keys())):
            node_names.append("{}{}".format(prefix_name, k))
    return node_names


def set_graph_from_csv(csv_file, graph=None):
    if graph is None:
        nodes_names = get_different_nodes(csv_file)
        graph = igraph.Graph(len(nodes_names))
        graph.vs['name'] = nodes_names

    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            first = row[0]
            second = row[1]
            graph.add_edge(first, second)
    return graph


def net_and_extra_links(model, version, strategy=None):
    x_coordinate = 20
    y_coordinate = 500
    exp = 2.5
    n_inter = 3
    network_system = InterdependentGraph()
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "networks")

    logic_dir = os.path.join(path, "logical_networks")
    AS_title = os.path.join(logic_dir, csv_title_generator("logic", "20", "500", exp, version=1))

    physical_dir = os.path.join(path, "physical_networks", "links")
    phys_title = os.path.join(physical_dir, csv_title_generator("physic", x_coordinate, y_coordinate, exp,
                                                                version=version, model=model))

    interlink_dir = os.path.join(path, "interdependencies", "full_random")
    interd_title = os.path.join(interlink_dir, csv_title_generator("dependence", "20", "500", exp, n_inter, 6,
                                                                   version=1))
    providers_dir = os.path.join(path, "providers")
    providers_title = os.path.join(providers_dir, csv_title_generator("providers", "20", "500", exp, n_inter,
                                                                      6, version=1))

    node_loc_dir = os.path.join(path, "physical_networks", "node_locations")
    nodes_title = os.path.join(node_loc_dir,
                               csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version))

    network_system.create_from_csv(AS_title, phys_title, interd_title, nodes_title, providers_csv=providers_title)
    pgraph = network_system.get_phys()
    print(len(pgraph.get_edgelist()))

    if strategy:
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, "networks", "physical_networks", "extra_edges", strategy,
                            csv_title_generator("candidates", x_coordinate, y_coordinate, exp,
                                                version=version, model=model))

        edges_to_add = get_list_of_tuples_from_csv(path)
        network_system.add_edges_to_physical_network(edges_to_add)
        pgraph = network_system.get_phys()
        print(len(pgraph.get_edgelist()))
        print(" -> Added edges from: {}".format(path))


def check_allocations():
    x = 0
    y = 1
    space_shapes = [[20, 500], [100, 100]]
    n_phys = 2000
    exp = 2.5
    n_inter = 3
    n_logic_suppliers = 6
    for version in range(1, 11):
        for s in space_shapes:
            coord_dir = "networks/physical_networks/node_locations/" + \
                        csv_title_generator("nodes", s[x], s[y], exp, version=version)
            coord_dict = get_list_of_coordinates_from_csv(coord_dir)
            aux_dict = {}
            print_flag = False
            for node in list(coord_dict.keys()):

                point = (coord_dict[node][x], coord_dict[node][y])
                if point not in aux_dict.keys():
                    aux_dict[point] = 1
                else:
                    aux_dict[point] += 1
                    print_flag = True
            if print_flag:
                for p in aux_dict.keys():
                    if aux_dict[p] > 1:
                        print("Point {} appears {} times in {}".format(p, aux_dict[p], coord_dir))
            else:
                print("{} OK".format(coord_dir))


def check_edges(model):
    x = 0
    y = 1
    space_shapes = [[20, 500], [100, 100]]
    n_phys = 2000
    exp = 2.5
    n_inter = 3
    n_logic_suppliers = 6
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "networks")

    not_ok_flag= False
    for version in range(1, 11):
        for s in space_shapes:
            physical_dir = os.path.join(path, "physical_networks", "links")
            phys_title = os.path.join(physical_dir, csv_title_generator("physic", s[x], s[y], exp,
                                                                        version=version, model=model))


            print("opening {}".format(phys_title))
            pg = single_physical_network(model, s, version)
            elist = pg.get_edgelist()


            aux_dict = {}
            print_flag = False
            with open(phys_title, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar=',')
                for row in reader:
                    first = row[0]
                    second = row[1]
                    edge = (first, second)

                    edge_aux = (int(first.replace("p", "")), int(second.replace("p", "")))
                    if edge_aux not in elist and (second, first) not in elist:
                        print(edge)
                        not_ok_flag = True

                    if edge not in aux_dict.keys() and (second, first) not in aux_dict.keys():
                        aux_dict[edge] = 1
                    else:
                        aux_dict[edge] += 1
                        print_flag = True
                if print_flag:
                    for p in aux_dict.keys():
                        if aux_dict[p] > 1:
                            print("Edge {} appears {} times in {}".format(p, aux_dict[p], phys_title))
                #else:
                #    print("{} OK".format(phys_title))
                if len(elist) != len(list(aux_dict.keys())):
                    print("{} vs {}".format(len(elist), len(list(aux_dict.keys()))))
                    not_ok_flag = True
    if not_ok_flag:
        print("Model {} has problems".format(model))


def create_interdependencies_and_providers(n_logic, n_phys, n_logic_suppliers, n_inter, version, interlink_type, legacy=False):
    print("start {}".format(datetime.datetime.now()))

    phys_id_list = []
    for i in range(n_phys):
        phys_id_list.append('p{}'.format(i))

    logic_id_list = []
    for i in range(n_logic):
        logic_id_list.append('l{}'.format(i))

    # for legacy
    as_suppliers_dict = {1: ['l295', 'l50', 'l230', 'l273', 'l176', 'l107'],
                         3: ['l223', 'l70', 'l177', 'l89', 'l141', 'l176'],
                         5: ['l227', 'l60', 'l92', 'l17', 'l122', 'l3'],
                         7: ['l194', 'l90', 'l260', 'l49', 'l259', 'l285'],
                         10: ['l96', 'l220', 'l132', 'l25', 'l24', 'l285']}
    if legacy and n_inter in list(as_suppliers_dict.keys()):
        as_suppliers = as_suppliers_dict[n_inter]
    else:
        as_suppliers = network_generators.set_logic_suppliers(logic_id_list, n_logic_suppliers)

    print("Logic suppliers ready {}".format(datetime.datetime.now()))

    interdep_graph = network_generators.set_interdependencies(phys_id_list, logic_id_list, n_inter, as_suppliers,
                                                              mode=interlink_type)

    print("interdep ready {}".format(datetime.datetime.now()))

    phys_suppliers = network_generators.set_physical_suppliers(interdep_graph, as_suppliers)

    print("Phys suppliers ready {}".format(datetime.datetime.now()))

    network_system = InterdependentGraph()
    network_system.create_from_empty_logic_physical(logic_id_list, as_suppliers, phys_id_list, phys_suppliers,
                                                    interdep_graph)

    print("system created {}".format(datetime.datetime.now()))

    network_system.save_interlinks_and_providers(n_inter, version=version, interlink_mode=interlink_type)

    print("system saved {}".format(datetime.datetime.now()))


def create_interlinks_and_provider_from_previous(og_ndep, og_provider_file_name, og_interlink_file_name,
                                                 target_ndep, target_provider_file_name, target_interlink_file_name,
                                                 debug=False):
    inherit_interlinks_from_target = False
    # as initial approach it only works with provider_priority
    # logic providers from the og files are preserved

    # if target_ndep < og_ndep, for og_provider not in target_providers
    # load og_provider_file_name and og_interlink_file_name to get each logic provider counterparts,
    # load target_interlink_file_name and target_provider_file_name
    target_interlinks = []
    target_logic_providers = []
    og_interlinks = []
    og_logic_providers = []

    with open(og_interlink_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            og_interlinks.append((row[0], row[1]))

    with open(og_provider_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            if row[0] == "logic":
                continue
            if row[0] == "physical":
                break
            og_logic_providers.append(row[0])

    with open(target_interlink_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            target_interlinks.append((row[0], row[1]))

    with open(target_provider_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            if row[0] == "logic":
                continue
            if row[0] == "physical":
                break
            target_logic_providers.append(row[0])
    if debug:
        print("Initial state:")
        print(" -- Og providers : {}".format(og_logic_providers))
        print(" -- Target providers: {}".format(target_logic_providers))

    # check if there are repeated providers
    og_logic_providers = [provider for provider in og_logic_providers if provider not in target_logic_providers]
    if debug:
        print(" -- Og providers not in target providers: {}".format(og_logic_providers))

    # get interlinks of og_providers
    # delete (og_ndep - target_ndep) interlinks from each logic provider
    if debug:
        print(" -- Interlinks of og providers in og interlinks:")

    upper_limit = min(og_ndep, target_ndep)
    og_provider_interlinks = {}
    for logic_provider in og_logic_providers:
        og_provider_interlinks[logic_provider] = []
        links_added = 0
        for interlink in og_interlinks:
            if interlink[1] == logic_provider:
                og_provider_interlinks[logic_provider].append(interlink)
                links_added += 1
                if links_added >= upper_limit:
                    break
        if debug:
            print(" -- -- {} : {}".format(logic_provider, og_provider_interlinks[logic_provider]))

    # (a) find number of interlinks in target_interlink_file_name of og_providers
    if debug:
        print(" -- Interlinks of og providers in target interlinks:")
    og_provider_in_target_interlinks = {}
    index = 0
    for logic_provider in og_logic_providers:
        og_provider_in_target_interlinks[index] = []
        for interlink in target_interlinks:
            if interlink[1] == logic_provider:
                og_provider_in_target_interlinks[index].append(interlink)
        if debug:
            print(" -- -- {} : {}".format(logic_provider, og_provider_in_target_interlinks[index]))
        index += 1

    # replace og_provider interlinks in the target_interlink_file_name:
    # 1.- delete interlinks that contain og_providers from target_interlinks
    if inherit_interlinks_from_target:
        if debug:
            print("\nModifying target interlinks. Adding og provider interlinks:")

        target_interlinks_after_removal = target_interlinks.copy()
        for logic_provider in og_logic_providers:
            if debug:
                print(" -- Provider {}:".format(logic_provider))
            for interlink in target_interlinks:
                if interlink[1] == logic_provider:
                    target_interlinks_after_removal.remove(interlink)
                    if debug:
                        print(" -- -- Removed: {}".format(interlink))
            for new_interlink in og_provider_interlinks[logic_provider]:
                target_interlinks_after_removal.append(new_interlink)
                if debug:
                    print(" -- -- Added: {}".format(new_interlink))

        # adjust target_providers interlink number to match (a)
        if debug:
            print("\nModifying target interlinks. Changing target provider interlinks:")
        target_logic_providers = [provider for provider in target_logic_providers if provider not in og_logic_providers]
        index = 0
        for logic_provider in target_logic_providers:
            if debug:
                print(" -- Provider {}:".format(logic_provider))
            for interlink in target_interlinks:
                if interlink[1] == logic_provider:
                    target_interlinks_after_removal.remove(interlink)
                    if debug:
                        print(" -- -- Removed: {}".format(interlink))
                    og_provider = og_logic_providers[index]
                    if target_ndep > og_ndep and len(og_provider_interlinks[og_provider]) < target_ndep:
                        new_interlink = (interlink[0], og_provider)
                        if new_interlink not in og_provider_interlinks[og_provider]:
                            og_provider_interlinks[og_provider].append(new_interlink)
                            target_interlinks_after_removal.append(new_interlink)
                            if debug:
                                print(" -- -- + Added to og provider: {}".format( new_interlink))
                        else:
                            if debug:
                                print(" -- -- ! Already interlink of og provider: {}".format(new_interlink))

            for other_interlink in og_provider_in_target_interlinks[index]:
                new_interlink = (other_interlink[0], logic_provider)
                target_interlinks_after_removal.append(new_interlink)
                if debug:
                    print(" -- -- Added: {}".format(new_interlink))
            index += 1

    else:
        new_interlinks = og_interlinks.copy()
        # get interlinks from target
        target_interlinks_per_node = {}
        for i in range(300):
            logic_node_name = 'l{}'.format(i)
            target_interlinks_per_node[logic_node_name] = []
            for interlink in target_interlinks:
                if interlink[1] == logic_node_name:
                    target_interlinks_per_node[logic_node_name].append(interlink)
        # get interlinks from og
        og_interlinks_per_node = {}
        for i in range(300):
            logic_node_name = 'l{}'.format(i)
            og_interlinks_per_node[logic_node_name] = []
            for interlink in og_interlinks:
                if interlink[1] == logic_node_name:
                    og_interlinks_per_node[logic_node_name].append(interlink)

        if debug:
            print("\nModifying target interlinks. Changing target provider interlinks:")
        target_logic_providers = [provider for provider in target_logic_providers if provider not in og_logic_providers]
        index = 0
        # add interlinks if needed to og providers
        for logic_provider in target_logic_providers:
            og_provider = og_logic_providers[index]
            if debug:
                print(" -- Provider {}:".format(og_provider))
            for interlink in target_interlinks:

                if interlink[1] == logic_provider:

                    if target_ndep > og_ndep and len(og_provider_interlinks[og_provider]) < target_ndep:

                        new_interlink = (interlink[0], og_provider)
                        if new_interlink not in og_provider_interlinks[og_provider]:
                            og_provider_interlinks[og_provider].append(new_interlink)
                            new_interlinks.append(new_interlink)
                            if debug:
                                print(" -- -- + Added to og provider: {}".format(new_interlink))
                        else:
                            if debug:
                                print(" -- -- ! Already interlink of og provider: {}".format(new_interlink))
            index += 1
        # adjust interlinks for target providers
        index = 0
        for logic_provider in og_logic_providers:
            og_number_of_links = len(og_interlinks_per_node[logic_provider])
            target_number_of_links = len(target_interlinks_per_node[logic_provider])
            target_provider = target_logic_providers[index]
            print("********* {} {} -- {}".format(target_provider, len(og_interlinks_per_node[target_provider]),
                                       target_number_of_links))
            if len(og_interlinks_per_node[target_provider]) < target_number_of_links:
                count = len(og_interlinks_per_node[target_provider])
                for interlink in target_interlinks_per_node[logic_provider]:
                    new_interlink = (interlink[0], target_provider)
                    if new_interlink not in new_interlinks:
                        new_interlinks.append(new_interlink)
                        count += 1
                        if debug:
                            print(" -- {} -- adding {}".format(count, new_interlink))
                        if count == target_number_of_links:
                            break
                    else:
                        continue
            else:
                if len(og_interlinks_per_node[target_provider]) > target_number_of_links:
                    count = len(og_interlinks_per_node[target_provider])
                    for interlink in og_interlinks_per_node[target_provider]:
                        new_interlinks.remove(interlink)
                        count -= 1
                        if debug:
                            print(" -- {} -- removing {}".format(count, interlink))
                        if count == target_number_of_links:
                            break

            index += 1

        for node in list(target_interlinks_per_node.keys()):
            if node in og_logic_providers or node in target_logic_providers:
                continue

            og_number_of_links = len(og_interlinks_per_node[node])
            target_number_of_links = len(target_interlinks_per_node[node])

            if og_number_of_links < target_number_of_links:
                if debug:
                    print("+ node {}: has {} og_interlinks, {} target_interlinks".format(node,og_number_of_links
                                                                                       , target_number_of_links))
                count = og_number_of_links
                for interlink in target_interlinks_per_node[node]:
                    if interlink not in og_interlinks_per_node[node]:

                        new_interlinks.append(interlink)
                        count += 1
                        if debug:
                            print(" -- {} -- adding {}".format(count,interlink))
                        if count == target_number_of_links:
                            break
            else:
                if og_number_of_links == target_number_of_links:
                    continue
                count = og_number_of_links
                if debug:
                    print("* node {}: has {} og_interlinks, {} target_interlinks".format(node, og_number_of_links,
                                                                                         target_number_of_links))
                for interlink in og_interlinks_per_node[node]:

                    new_interlinks.remove(interlink)
                    count -= 1

                    if debug:
                        print(" -- {} -- removing {}".format(count, interlink))
                    if count == target_number_of_links:
                        break

        target_interlinks_after_removal = new_interlinks

    if debug:
        print("# interlinks in og: {}".format(len(og_interlinks)))
        print("# interlinks after modification: {}".format(len(list(set(target_interlinks_after_removal)))))
        print("# interlinks in target: {}".format(len(target_interlinks)))

    # save the results (actually just print them)
    print("\n\n")
    new_physical_providers = set()
    for interlink in target_interlinks_after_removal:
        print("{},{}".format(interlink[0], interlink[1]))
        # check for physical providers
        if interlink[1] in og_logic_providers:
            new_physical_providers.add(interlink[0])
    print("\n\n")
    print("logic")
    for logic_provider in og_logic_providers:
        print(logic_provider)
        #pass
    print("physical")
    for physical_provider in list(new_physical_providers):
        print(physical_provider)
        #pass


def create_logic_network(exp, version, n_logic=300):
    # generate AS network
    print("Generating logic network ready {}".format(datetime.datetime.now()))
    as_graph = network_generators.generate_logic_network(n_logic, exponent=exp)
    #print(as_graph.degree_distribution())

    network_system = InterdependentGraph()
    number_of_components = len(as_graph.clusters())
    if number_of_components > 1:
        print("amount of connected components {}".format(number_of_components))
        exit(2)

    network_system.set_AS(as_graph)
    network_system.save_logic(exp, version=version)

    print("Logic network ready {}".format(datetime.datetime.now()))


def get_ordered_nodes_by_degrees(graph):
    list_node_name_degree = []
    for node in graph.vs:
        list_node_name_degree.append((node['name'], graph.degree(node)))
    list_node_name_degree.sort(key=operator.itemgetter(1))
    return list_node_name_degree


def number_of_distinct_edges(edge_list):
    edge_dict = {}
    for edge in edge_list:
        edge_n_0 = int((edge[0]).replace("p", ""))
        edge_n_1 = int((edge[1]).replace("p", ""))
        if edge_n_0 < edge_n_1:
            edge_dict[edge] = ""
        else:
            inv_edge = (edge[1], edge[0])
            edge_dict[inv_edge] = ""
    return len(list(edge_dict.keys()))


def create_extra_edges(model, strategy, number=640, max_length=0, max_length_from="", spaces=[]):
    t_mod = ""
    if number != 640:
        t_mod = str(number)
    if max_length > 0:
        if len(t_mod) > 0:
            t_mod += "_"
        t_mod = "{}cl_{}".format(t_mod, max_length_from)
    if len(spaces) < 1:
        spaces = [[20, 500], [100, 100]]
    graph_dir = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/links/"
    coord_dir = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/node_locations/"
    for s in spaces:
        for v in range(1, 11):
            graph_name = "physic_{}x{}_exp_2.5_v{}_m_{}.csv".format(s[0], s[1], v, model)
            cord_name = "nodes_{}x{}_exp_2.5_v{}.csv".format(s[0], s[1], v)
            coord_dict = get_list_of_coordinates_from_csv(coord_dir+cord_name)

            graph1 = set_graph_from_csv(graph_dir+graph_name)
            if strategy == "distance":
                new_edges = network_generators.generate_edges_to_add_distance(graph1, coord_dict, 97, number)
                network_generators.save_edges_to_csv(new_edges, s[0], s[1], 2.5, version=v, model=model, strategy="distance_aux", title_mod=t_mod)
            elif strategy == "local_hubs":
                new_edges = network_generators.generate_edges_to_add_distance_hubs(graph1, coord_dict, 97, number)
                network_generators.save_edges_to_csv(new_edges, s[0], s[1], 2.5, version=v, model=model, strategy="local_hubs", title_mod=t_mod)
            elif strategy == "random":
                new_edges = network_generators.generate_edges_to_add_random(number, graph1, coord_dict, max_length=max_length)
                network_generators.save_edges_to_csv(new_edges, s[0], s[1], 2.5, version=v, model=model, strategy="random", title_mod=t_mod)
            elif strategy == "degree":
                new_edges = network_generators.generate_edges_to_add_degree(graph1, 97, number)
                network_generators.save_edges_to_csv(new_edges, s[0], s[1], 2.5, version=v, model=model, strategy="degree_aux", title_mod=t_mod)


def get_max_edge_length_for_strategy(strategy, spaces, models):
    #spaces = [[20, 500], [100, 100]]

    coord_dir = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/node_locations/"
    st_dict = {"distance": "distance_aux", "degree": "degree_aux", "local_hubs": "local_hubs", "random": "random"}
    graph_dir = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/extra_edges/{}/".format(st_dict[strategy])

    for model in models:
        for s in spaces:
            maxes = []
            for v in range(1, 11):
                max_extra_edge_length = 0
                min_extra_edge_length = 100000
                extra_edges_file_name = "candidates_{}x{}_exp_2.5_v{}_m_{}.csv".format(s[0], s[1], v, model)
                cord_name = "nodes_{}x{}_exp_2.5_v{}.csv".format(s[0], s[1], v)
                coord_dict = get_list_of_coordinates_from_csv(coord_dir + cord_name)
                base_graph = igraph.Graph(len(coord_dict.keys()))
                base_graph.vs['name'] = list(coord_dict.keys())
                extra_edges_graph = set_graph_from_csv(graph_dir + extra_edges_file_name, graph=base_graph)
                x = 0
                y = 1
                for edge in extra_edges_graph.get_edgelist():
                    node_1 = extra_edges_graph.vs[edge[0]]['name']
                    node_2 = extra_edges_graph.vs[edge[1]]['name']
                    x1 = coord_dict[node_1][x]
                    y1 = coord_dict[node_1][y]
                    x2 = coord_dict[node_2][x]
                    y2 = coord_dict[node_2][y]

                    edge_length = math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
                    if edge_length > max_extra_edge_length:
                        max_extra_edge_length = edge_length
                    if edge_length < min_extra_edge_length:
                        min_extra_edge_length = edge_length
                maxes.append(max_extra_edge_length)
                #print("Max edge length for {} strategy: {}, s={}, v={}, m={}".format(strategy, max_extra_edge_length, s, v, model))
                #print("Min edge length for {} strategy: {}, s={}, v={}, m={}".format(strategy, min_extra_edge_length, s, v, model))
            print("{} {} Average max: {} ({})".format(model, s, np.mean(maxes), np.std(maxes)))
            return np.mean(maxes), np.std(maxes)


def check_if_done(x_coordinate, y_coordinate, exp, strategy, n_inter, version, model, legacy=False):
    physical_attack_title = csv_title_generator("result", x_coordinate, y_coordinate, exp, n_dependence=n_inter,
                                                attack_type="physical", version=version, model=model)
    if legacy:
        physical_attack_title = "legacy_{}".format(physical_attack_title)
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "test_results", strategy, "physical_random_attacks", physical_attack_title)
    return os.path.exists(path)


def check_lines_done(file_path):
    print(file_path)
    done_line_list = []
    todo_line_list = []
    file_lines = []
    file_lines = [int(l) for l in file_lines]
    with open(file_path) as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
        if len(file_lines) > 0:
            lines = [lines[i] for i in file_lines]
    for line in lines:
        task = parse_task_args(line)
        is_done = check_if_done(task['x_coordinate'],
                                task['y_coordinate'],
                                task['exp'],
                                task['strategy'],
                                task['n_inter'],
                                task['version'],
                                task['model'],
                                legacy=task['legacy'])
        if is_done:
            done_line_list.append(line)
        else:
            if "degree" not in line:
                print(line)
                todo_line_list.append(line)

    print("done tasks: {}".format(len(done_line_list)))
    print("to do tasks: {}".format(len(todo_line_list)))


def check_paths(paths, input):
    for path in paths:
        if check_if_path_working(path, input):
            return True
    return len(paths) == 0


def check_if_path_working(path, input):
    for node in path:
        if not input[node]:
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


def attack_nodes_test(phys_name_by_index, logic_name_by_index, intern_name_by_index,
                  physic_node_paths_to_providers,
                  logic_node_paths_to_providers,
                  inter_paths,
                  inter_roseta_phys, inter_roseta_logic,
                  phys_nodes_to_delete,
                  logic_nodes_to_delete=[]):
    n_phys_nodes = len(phys_name_by_index)
    n_logic_nodes = len(logic_name_by_index)
    n_inter_nodes = len(intern_name_by_index)

    phys_input = [True for i in range(n_phys_nodes)]
    logic_input = [True for i in range(n_logic_nodes)]
    inter_input = [True for i in range(n_inter_nodes)]
    current_phys_nodes_to_delete = []
    current_logic_nodes_to_delete = []

    for pnode in phys_nodes_to_delete:
        phys_input[pnode] = False

    for lnode in logic_nodes_to_delete:
        logic_input[lnode] = False

    while True:
        # if there are no more nodes to delete, i.e, the network has stabilized, then stop
        if phys_nodes_to_delete == current_phys_nodes_to_delete and\
                logic_nodes_to_delete == current_logic_nodes_to_delete:
            break
        phys_nodes_to_delete = current_phys_nodes_to_delete.copy()
        logic_nodes_to_delete = current_logic_nodes_to_delete.copy()
        current_phys_nodes_to_delete = []
        current_logic_nodes_to_delete = []

        # Delete the nodes to delete on each network, including the interactions network
        for pnode in phys_nodes_to_delete:
            phys_input[pnode] = False

        for lnode in logic_nodes_to_delete:
            logic_input[lnode] = False

        # Delete all nodes that fail because they don't have connection to a provider on each network including
        # interactions network
        for inode in range(n_inter_nodes):
            # la roseta guarda el indice del nodo inter en su grafo de origen, o sea que
            # p_index = roseta[intern_name_by_index[inode]]
            # inter_input[inode] = phys_input[p_index]
            inode_name = intern_name_by_index[inode]
            if inode_name in inter_roseta_logic.keys():
                l_index = inter_roseta_logic[inode_name]
                inter_input[inode] = logic_input[l_index]
            else:
                p_index = inter_roseta_phys[inode_name]
                inter_input[inode] = phys_input[p_index]

        phys_aux_input = [True for i in range(n_phys_nodes)]
        logic_aux_input = [True for i in range(n_logic_nodes)]
        inter_aux_input = [True for i in range(n_inter_nodes)]

        # Determine all nodes that fail because they don't have connection to a provider
        # physical
        for pnode in range(n_phys_nodes):
            phys_aux_input[pnode] = check_paths(physic_node_paths_to_providers[pnode], phys_input)

        # logical
        for lnode in range(n_phys_nodes):
            logic_aux_input[lnode] = check_paths(logic_node_paths_to_providers[lnode], logic_input)

        # Get the nodes lost because they have lost all support from the other network
        for inode in range(n_inter_nodes):
            inter_aux_input[inode] = check_paths(inter_paths[inode], inter_input)

        # update lists of nodes lost
        # Add them to the nodes to delete on the next iteration
        for pnode in range(n_phys_nodes):
            if not phys_aux_input[pnode]:
                current_phys_nodes_to_delete.append(pnode)

        for lnode in range(n_logic_nodes):
            if not logic_aux_input[lnode]:
                current_logic_nodes_to_delete.append(lnode)

        for inode in range(n_inter_nodes):
            if not inter_aux_input[inode]:
                inode_name = intern_name_by_index[inode]
                if inode_name in inter_roseta_logic.keys():
                    l_index = inter_roseta_logic[inode_name]
                    current_logic_nodes_to_delete.append(logic_input[l_index])
                else:
                    p_index = inter_roseta_phys[inode_name]
                    current_phys_nodes_to_delete.append(phys_input[p_index])


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

    paths_for_each_node = []
    for i in range(len(interlinks_graph.vs)):
        current_node_paths = interlinks_graph.get_all_simple_paths(i, cutoff=1)
        paths_for_each_node.append(current_node_paths)

    return name_by_index, roseta_phys, roseta_logic, paths_for_each_node


def is_logical_node(node_name):
    return node_name[0] == 'l'


def parse_inner_network(network, providers):
    name_by_index = []
    node_paths_to_providers = get_all_paths_to_providers(network, providers)
    for i in range(len(network.vs)):
        name_by_index.append(network.vs[i]['name'])
    return name_by_index, node_paths_to_providers


og_ndep = 3
og_provider_file_name = "networks/providers/provider_priority/providers_ndep_3_lprovnum_6_v3.csv"
og_interlink_file_name = "networks/interdependencies/provider_priority/dependence_ndep_3_lprovnum_6_v3.csv"
target_ndep = 7
target_provider_file_name = "networks/providers/provider_priority/og-providers_ndep_7_lprovnum_6_v3.csv"
target_interlink_file_name = "networks/interdependencies/provider_priority/og-dependence_ndep_7_lprovnum_6_v3.csv"

#create_interlinks_and_provider_from_previous(og_ndep, og_provider_file_name, og_interlink_file_name,
#                                                 target_ndep, target_provider_file_name, target_interlink_file_name,
#                                                 debug=True)


#create_extra_edges('RNG', "distance", number=3000)


#create_extra_edges('RNG', "random", number=640, max_length=1)

def create_extra_edges_cap_random_length(strategy):
    strategies = [strategy]#, "local_hubs", "degree", "random"]
    models = ["RNG", "GG", "5NN"]
    spaces = [[20, 500], [100, 100]]
    for strategy in strategies:
        for model in models:
            for s in spaces:
                print("--------- {}".format(strategy))
                mean, std = get_max_edge_length_for_strategy(strategy, [s], [model])
                create_extra_edges(model, "random", number=640, max_length=np.ceil(mean), spaces=[s], max_length_from=strategy)

