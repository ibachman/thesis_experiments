import igraph
import csv
import os
import time
import gc

def save_as_csv(path, file_name, content_dict):
    title = os.path.join(path,file_name)
    with open(title, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        first_line = content_dict[0].keys()
        writer.writerow(first_line)
        for row in content_dict:
            line = []
            for column in first_line:
                line.append(row[column])
            writer.writerow(line)


def csv_title_generator(graph_type, x_axis_length, y_axis_length, pg_exponent, n_dependence="", l_providers="",
                        attack_type="", version="", model=""):
    title = str(graph_type)

    if x_axis_length != "" and y_axis_length != "":
        title += "_{}x{}".format(x_axis_length, y_axis_length)
    if pg_exponent != "":
        title += "_exp_{}".format(pg_exponent)
    if n_dependence != "":
        title += "_ndep_{}".format(n_dependence)
    if attack_type != "":
        title = title + "_att_{}".format(attack_type)
    if l_providers != "":
        title += "_lprovnum_{}".format(l_providers)
    if version != "":
        title += "_v{}".format(version)
    if model != "":
        title += "_m_{}".format(model)

    title += ".csv"
    return title


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


def write_graph_with_node_names(graph, title):
    with open(title, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        lst = graph.get_edgelist()
        names = graph.vs["name"]
        for i in range(len(lst)):
            j = lst[i][0]
            k = lst[i][1]
            writer.writerow([names[j], names[k]])


def get_list_of_tuples_from_csv(csv_file):
    list_of_tuples = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            first = row[0]
            second = row[1]
            list_of_tuples.append((first, second))
    return list_of_tuples


def save_nodes_to_csv(x_positions, y_positions, x_coordinates, y_coordinates, pg_exponent, n_dependence, l_providers,
                      attack_type="", version="", model=""):
    title = csv_title_generator("nodes", x_coordinates, y_coordinates, pg_exponent,
                                attack_type="", version=version, model=model)
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_directory = os.path.join(base_path, "networks", "physical_networks", "node_locations", title)

    with open(full_directory, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(x_positions)):
            j = x_positions[i]
            k = y_positions[i]
            name = "p"+str(i)
            writer.writerow([name, j, k])


def get_list_of_coordinates_from_csv(csv_file):
    coord_dict = {}

    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            x = float(row[1])
            y = float(row[2])
            coord_dict[row[0]] = [x, y]

    return coord_dict


# def get_nodes_in_radius(physical_network, x_coordinate, y_coordinate, exp, version):
#    # Read coordinates
#    coord_title = "networks/" + csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version)
#    x_coord, y_coord = get_list_of_coordinates_from_csv(coord_title)
class RandomAttackTimeoutError(Exception):
    pass


class InterdependentGraph(object):

    def __init__(self):
        pass

    def save_physical(self, x_coordinates, y_coordinates, pg_exponent, version="", model=""):
        physical_graph = self.physical_network
        if not os.path.exists('networks'):
            os.makedirs('networks')
        base_path = os.path.dirname(os.path.abspath(__file__))

        # write physical
        physical_file_name = csv_title_generator("physic", x_coordinates, y_coordinates, pg_exponent, version=version,
                                                 model=model)
        physical_dir = os.path.join(base_path, "networks", "physical_networks", "links", physical_file_name)

        print("---- ... writing")
        write_graph_with_node_names(physical_graph, physical_dir)
        print("---- Physical network saved in: {}".format(physical_dir))
    
    def save_logic(self, pg_exponent, version=""):
        base_path = os.path.dirname(os.path.abspath(__file__))
        logic_graph = self.AS_network
        if not os.path.exists('networks'):
            os.makedirs('networks')
        # write logic
        logic_name = csv_title_generator("logic", "", "", pg_exponent, version=version, model="")

        logic_network_path = os.path.join(base_path, "networks", "logical_networks", logic_name)
        write_graph_with_node_names(logic_graph, logic_network_path)

    def save_interlinks_and_providers(self, n_dependence, version="", model="", interlink_mode=None):

        interlink_graph = self.interactions_network
        p_provider = list(self.physical_providers)
        l_providers = list(self.AS_providers)
        len_l_providers = str(len(l_providers))

        if not os.path.exists('networks'):
            os.makedirs('networks')
        base_path = os.path.dirname(os.path.abspath(__file__))

        dependence_name = csv_title_generator("dependence", "", "", "", n_dependence,
                                              len_l_providers, version=version, model=model)

        providers_name = csv_title_generator("providers", "", "", "", n_dependence,
                                             len_l_providers, version=version, model=model)

        # set paths
        if interlink_mode:
            interlink_mode = interlink_mode.replace(" ", "_")
            dependence_path = os.path.join(base_path, "networks", "interdependencies", interlink_mode, dependence_name)
            providers_path = os.path.join(base_path, "networks", "providers", interlink_mode, providers_name)
        else:
            dependence_path = os.path.join(base_path, "networks", "interdependencies", dependence_name)
            providers_path = os.path.join(base_path, "networks", "providers", providers_name)

        # write dependence
        write_graph_with_node_names(interlink_graph, dependence_path)

        # write providers
        with open(providers_path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["logic"])
            for i in range(len(l_providers)):
                writer.writerow([l_providers[i]])
            writer.writerow(["physical"])
            for i in range(len(p_provider)):
                writer.writerow([p_provider[i]])

    def create_from_csv(self, AS_net_csv, physical_net_csv, interactions_csv, nodes_title, providers_csv="",
                        AS_provider_nodes=[],
                        physical_provider_nodes=[]):
        x = 0
        y = 1
        # Create AS graph from csv file
        self.AS_network = set_graph_from_csv(AS_net_csv)

        ##### Create physical graph from csv file
        self.physical_network = set_graph_from_csv(physical_net_csv)
        coord_dict = get_list_of_coordinates_from_csv(nodes_title)
        x_aloc = []
        y_aloc = []
        for i in range(len(self.physical_network.vs)):
            node_name = self.physical_network.vs[i]['name']
            x_aloc.append(coord_dict[node_name][x])
            y_aloc.append(coord_dict[node_name][y])

        self.physical_network.vs['x_coordinate'] = x_aloc
        self.physical_network.vs['y_coordinate'] = y_aloc
        ##### -----------------------------------

        # Create interactions graph from csv file. This contains the nodes of both networks
        self.interactions_network = igraph.Graph()
        self.interactions_network = set_graph_from_csv(interactions_csv)
        # set providers from file
        if providers_csv != "":
            AS_provider_nodes = []
            physical_provider_nodes = []
            with open(providers_csv, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar=',')
                type_of_provider = ""
                for row in reader:
                    if row[0] == "logic":
                        type_of_provider = "logic"
                    elif row[0] == "physical":
                        type_of_provider = "physical"
                    else:
                        if type_of_provider == "logic":
                            AS_provider_nodes.append(str(row[0]))
                        if type_of_provider == "physical":
                            physical_provider_nodes.append(str(row[0]))

        as_net_name_list = self.AS_network.vs['name']
        physical_net_name_list = self.physical_network.vs['name']
        type_list = []
        for node in self.interactions_network.vs:
            if node['name'] in as_net_name_list:
                type_list.append(0)
            elif node['name'] in physical_net_name_list:
                type_list.append(1)
        self.interactions_network.vs['type'] = type_list
        # save provider nodes
        self.AS_providers = AS_provider_nodes
        self.physical_providers = physical_provider_nodes
        # save initial set of functional nodes
        self.initial_number_of_functional_nodes_in_AS_net = \
            len([a for a in self.AS_network.vs if self.AS_network.degree(a.index) > 0])
        return self

    def get_as(self):
        return self.AS_network

    def add_edges_to_physical_network(self, edge_tuple_array):
        (self.physical_network).add_edges(edge_tuple_array)

    def get_as_providers(self):
        return self.AS_providers

    def get_phys(self):
        return self.physical_network

    def get_phys_providers(self):
        return self.physical_providers

    def get_interlinks(self):
        return self.interactions_network
    
    def set_AS(self, AS_graph):
        # save AS graph (create copy from original)
        #self.AS_network = igraph.Graph([e.tuple for e in AS_graph.es])
        self.AS_network = AS_graph
        return self
    
    def set_physical(self, physical_graph):
        #self.physical_network = igraph.Graph([e.tuple for e in physical_graph.es])
        self.physical_network = physical_graph
        return self

    def set_interlinks(self, interlinks_graph):
        self.interactions_network = interlinks_graph
        return self

    def create_from_graph(self, AS_graph, AS_provider_nodes, physical_graph, physical_provider_nodes,
                          interactions_graph):
        # save AS graph (create copy from original)
        self.AS_network = igraph.Graph([e.tuple for e in AS_graph.es])
        self.AS_network.vs["name"] = AS_graph.vs["name"]

        # save physical graph (create copy from original)
        self.physical_network = igraph.Graph([e.tuple for e in physical_graph.es])
        self.physical_network.vs["name"] = physical_graph.vs["name"]
        self.physical_network.vs["x_coordinate"] = physical_graph.vs["x_coordinate"]
        self.physical_network.vs["y_coordinate"] = physical_graph.vs["y_coordinate"]
        # prepare and save interactions graph
        self.interactions_network = igraph.Graph([e.tuple for e in interactions_graph.es])
        self.interactions_network.vs["name"] = interactions_graph.vs["name"]
        as_net_name_list = self.AS_network.vs["name"]
        physical_net_name_list = self.physical_network.vs["name"]
        type_list = []
        for node in self.interactions_network.vs:
            if node['name'] in as_net_name_list:
                type_list.append(0)
            elif node['name'] in physical_net_name_list:
                type_list.append(1)
        self.interactions_network.vs['type'] = type_list
        # save provider nodes
        self.AS_providers = AS_provider_nodes
        self.physical_providers = physical_provider_nodes
        # save initial set of functional nodes
        self.initial_number_of_functional_nodes_in_AS_net = \
            len([a for a in self.AS_network.vs if self.AS_network.degree(a.index) > 0])
        return self
    
    def create_from_empty_logic_physical(self, logic_graph_nodes_ids, logic_provider_nodes, physical_nodes_ids,
                                         physical_provider_nodes, interlink_graph):
        """ # save AS graph (create copy from original)
        self.AS_network = igraph.Graph([e.tuple for e in AS_graph.es])
        self.AS_network.vs["name"] = AS_graph.vs["name"]
         # save physical graph (create copy from original)
        self.physical_network = igraph.Graph([e.tuple for e in physical_graph.es])
        self.physical_network.vs["name"] = physical_graph.vs["name"] """

        # prepare and save interactions graph
        self.interactions_network = igraph.Graph([e.tuple for e in interlink_graph.es])
        self.interactions_network.vs["name"] = interlink_graph.vs["name"]

        type_list = []
        for node in self.interactions_network.vs:
            if node['name'] in logic_graph_nodes_ids:
                type_list.append(0)
            elif node['name'] in physical_nodes_ids:
                type_list.append(1)
        self.interactions_network.vs['type'] = type_list
        # save provider nodes
        self.AS_providers = logic_provider_nodes

        self.physical_providers = physical_provider_nodes
        """ # save initial set of functional nodes
        self.initial_number_of_functional_nodes_in_AS_net = \
            len([a for a in self.AS_network.vs if self.AS_network.degree(a.index) > 0]) """
        return self

    def attack_nodes(self, list_of_nodes_to_delete):
        current_logic_graph = self.AS_network
        current_physical_graph = self.physical_network
        current_interaction_graph = self.interactions_network

        seconds_threshold = 600 # 10 minutes
        time_threshold = seconds_threshold
        start_time = time.time()
        while True:
            current_time = time.time()
            # if there are no more nodes to delete, i.e, the network has stabilized, then stop
            if len(list_of_nodes_to_delete) == 0:
                break
            else:
                if current_time - start_time > time_threshold:
                    raise RandomAttackTimeoutError
            # Delete the nodes to delete on each network, including the interactions network
            nodes_to_delete_in_logic = [node for node in list_of_nodes_to_delete if node in current_logic_graph.vs['name']]
            nodes_to_delete_in_physic = [node for node in list_of_nodes_to_delete if node in current_physical_graph.vs['name']]
            current_logic_graph.delete_vertices(nodes_to_delete_in_logic)
            current_physical_graph.delete_vertices(nodes_to_delete_in_physic)
            current_interaction_graph.delete_vertices(
                [n for n in list_of_nodes_to_delete if n in current_interaction_graph.vs['name']])

            # Determine all nodes that fail because they don't have connection to a provider
            nodes_without_connection_to_provider_in_logic = set(range(len(current_logic_graph.vs)))
            alive_nodes_in_logic = current_logic_graph.vs['name']
            for provider_node in self.AS_providers:
                if provider_node not in alive_nodes_in_logic:
                    continue
                length_to_provider_in_logic_net = current_logic_graph.shortest_paths(provider_node)[0]
                zipped_list_A = zip(length_to_provider_in_logic_net, range(len(current_logic_graph.vs)))
                current_nodes_without_connection_to_provider_in_A = \
                    set([a[1] for a in zipped_list_A if a[0] == float('inf')])
                nodes_without_connection_to_provider_in_logic = \
                    nodes_without_connection_to_provider_in_logic \
                        .intersection(current_nodes_without_connection_to_provider_in_A)

            nodes_without_connection_to_provider_in_B = set(range(len(current_physical_graph.vs)))
            alive_nodes_in_B = current_physical_graph.vs['name']
            for provider_node in self.physical_providers:
                if provider_node not in alive_nodes_in_B:
                    continue
                # print provider_node, "is alive"
                length_to_provider_in_network_B = current_physical_graph.shortest_paths(provider_node)[0]
                zipped_list_B = zip(length_to_provider_in_network_B, range(len(current_physical_graph.vs)))
                current_nodes_without_connection_to_provider_in_B = \
                    set([a[1] for a in zipped_list_B if a[0] == float('inf')])
                nodes_without_connection_to_provider_in_B = \
                    nodes_without_connection_to_provider_in_B \
                        .intersection(current_nodes_without_connection_to_provider_in_B)
            # save the names (unique identifier) of the nodes lost because can't access a provider
            names_of_nodes_lost_in_A = set(current_logic_graph.vs(list(nodes_without_connection_to_provider_in_logic))['name'])
            names_of_nodes_lost_in_B = set(current_physical_graph.vs(list(nodes_without_connection_to_provider_in_B))['name'])
            # Delete all nodes that fail because they don't have connection to a provider on each network including
            # interactions network
            current_logic_graph.delete_vertices(nodes_without_connection_to_provider_in_logic)
            current_physical_graph.delete_vertices(nodes_without_connection_to_provider_in_B)
            nodes_to_delete = list(names_of_nodes_lost_in_A.union(names_of_nodes_lost_in_B))
            current_interaction_graph.delete_vertices(
                [n for n in nodes_to_delete if n in current_interaction_graph.vs['name']])
            # Get the nodes lost because they have lost all support from the other network
            zipped_list_interactions = zip(current_interaction_graph.degree(), current_interaction_graph.vs['name'])
            # Add them to the nodes to delete on the next iteration
            list_of_nodes_to_delete = [a[1] for a in zipped_list_interactions if a[0] < 1]

        return self

    def get_ratio_of_funtional_nodes_in_AS_network(self):
        funct_nodes = [a for a in self.AS_network.vs if self.AS_network.degree(a.index) > 0]
        #print("+++ {}".format(funct_nodes))
        functional_nodes_in_AS_net = len(funct_nodes)
        return (functional_nodes_in_AS_net * 1.0) / (self.initial_number_of_functional_nodes_in_AS_net * 1.0)

    def node_mtfr(self):
        return len((self.interactions_network.maximum_bipartite_matching()).edges())

