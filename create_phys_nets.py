from interdependent_network_library import *
import network_generators as network_generators
import igraph
import datetime
import connection_manager as cm


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
    phys_graph = network_generators.generate_physical_network(n_phys, model, coord_dict)
    print("---- Network {} done. Start time: {}".format(model, datetime.datetime.now()))
    network_system = InterdependentGraph()
    network_system.set_physical(phys_graph)
    # Save physical
    network_system.save_physical(x_coordinate, y_coordinate, exp, version=version, model=model)


def create_physical_network(model, v=None):
    space_shapes = [[20, 500], [100, 100]]
    for s in space_shapes:
        if s == space_shapes[0] and model == "RNG" and v in [1, 2, 3, 4]:
            continue
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

        print(csv_file)

    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            first = row[0]
            second = row[1]
            graph.add_edge(first, second)
    return graph

def net_and_extra_links(model, version, strategy):
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

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "networks", "physical_networks", "extra_edges", strategy,
                        csv_title_generator("candidates", x_coordinate, y_coordinate, exp,
                                            version=version, model=model))

    edges_to_add = get_list_of_tuples_from_csv(path)
    network_system.add_edges_to_physical_network(edges_to_add)
    pgraph = network_system.get_phys()
    print(len(pgraph.get_edgelist()))
    print(" -> Added edges from: {}".format(path))

#create_physical_network("RNG", v=3)
#create_physical_network("GG")
