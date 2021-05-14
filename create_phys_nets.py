from interdependent_network_library import *
import network_generators as network_generators
import igraph
import datetime
import random


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
    graph = igraph.Graph(3)
    graph.vs['name'] = ["p0", "p1", "p2"]
    graph.add_edges([("p0", "p1"), ("p1", "p2")])
    print(graph)
    print(graph.vs[0])
    print(graph.vs[1])
    print(graph.vs[2])
    print(graph.get_edgelist())


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


def create_interdependencies_and_providers(n_logic, n_phys, n_logic_suppliers, n_inter, version, interlink_type):
    print("start {}".format(datetime.datetime.now()))

    phys_id_list = []
    for i in range(n_phys):
        phys_id_list.append('p{}'.format(i))

    logic_id_list = []
    for i in range(n_logic):
        logic_id_list.append('l{}'.format(i))

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

