__author__ = 'ivana'
import datetime
import network_generators as network_generators
import tests_library as tests_library
from interdependent_network_library import *


def run_test(x_coordinate, y_coordinate, exp, n_inter, n_logic_suppliers,
             version, n_logic, n_phys, iter_number, READ_flag=False, attack_types=[], model=[], logic_flag=False,
             physical_flag=False, phys_iteration=0, strategy='', process_name="", localized_attack_data=[],
             seismic_data=[], legacy=False, debug=False, logic_file_name=None, interlink_type=None,
             interlink_version=1):

    fix_bridge_nodes_interlinks = False

    attack_logic = 'logic' in attack_types
    attack_phys = 'physical' in attack_types
    attack_both = 'both' in attack_types
    attack_localized = 'localized' in attack_types
    #
    attack_seismic = 'seismic' in attack_types

    if READ_flag:
        print("{} -- start {}".format(process_name, datetime.datetime.now()))
        interlink_type_names = {"provider_priority": "pp", "full_random": "fr", "semi_random":"sr"}
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
            interlink_title = "legacy_{}".format(csv_title_generator("dependence",  "20", "500", exp, n_inter, 6,
                                                                     version=1))
            providers_title = "legacy_{}".format(csv_title_generator("providers",  "20", "500", exp, n_inter, 6,
                                                                     version=1))
        else:
            if logic_file_name:
                logic_title = logic_file_name
            else:
                logic_title = "legacy_{}".format(csv_title_generator("logic", "20", "500", exp, version=1))
            interlink_title = csv_title_generator("dependence",  "", "", "", n_inter, 6, version=interlink_version)
            providers_title = csv_title_generator("providers",  "", "", "", n_inter, 6, version=interlink_version)

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
        sub_dir = 'simple_graphs'

        if strategy != '':
            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, "networks", "physical_networks", "extra_edges", strategy,
                                csv_title_generator("candidates", x_coordinate, y_coordinate, exp,
                                                    version=version, model=model))

            edges_to_add = get_list_of_tuples_from_csv(path)
            network_system.add_edges_to_physical_network(edges_to_add)
            print("{} -- -> Added edges from: {}".format(process_name, path))
            sub_dir = strategy

        if attack_phys:
            # key = (ppv,ndep, lv)
            fix_interlink_dict = {
                (3, 7, 2): [('p1105', 'l52'), ('p1488', 'l52'), ('p1918', 'l52'), ('p1058', 'l52'), ('p915', 'l52'),
                            ('p1277', 'l52'), ('p219', 'l294'), ('p1965', 'l294'), ('p1418', 'l294'), ('p1426', 'l294'),
                            ('p744', 'l294')],
                (1, 7, 2): [('p1285', 'l52')],
                (3, 7, 3): [('p679', 'l251'), ('p665', 'l251'), ('p673', 'l251'), ('p1452', 'l251')],
                (1, 7, 3): [],
                (3, 7, 4): [('p1261', 'l279'), ('p502', 'l279'), ('p1477', 'l279'), ('p1731', 'l279'),
                            ('p355', 'l279')],
                (1, 7, 4): [('p1566', 'l279'), ('p303', 'l279'), ('p1983', 'l279'), ('p842', 'l279'), ('p951', 'l279'),
                            ('p1447', 'l279')],
                (3, 7, 5): [('p1461', 'l138'), ('p59', 'l138'), ('p1629', 'l138'), ('p257', 'l138')],
                (1, 7, 5): [],
                (3, 7, 6): [],
                (1, 7, 6): [('p804', 'l87')],
                (3, 7, 7): [('p1350', 'l2')],
                (1, 7, 7): [('p620', 'l2'), ('p683', 'l2'), ('p286', 'l2'), ('p770', 'l2'), ('p1650', 'l2'),
                            ('p1178', 'l2')],
                (3, 7, 8): [('p1140', 'l88'), ('p261', 'l88'), ('p347', 'l88')],
                (1, 7, 8): [('p1928', 'l88'), ('p22', 'l88'), ('p943', 'l88'), ('p1117', 'l88')],
                (3, 7, 9): [],
                (1, 7, 9): [('p122', 'l179'), ('p643', 'l179')],
                (3, 7, 10): [('p1333', 'l138'), ('p1692', 'l138'), ('p153', 'l138'), ('p270', 'l138')],
                (1, 7, 10): [],
                (3, 3, 2): [('p73', 'l52')],
                (3, 3, 3): [('p1553', 'l192'), ('p462', 'l192'), ('p387', 'l251')],
                (3, 3, 4): [],
                (3, 3, 5): [('p1358', 'l138'), ('p1877', 'l138')],
                (3, 3, 6): [],
                (3, 3, 7): [],
                (3, 3, 8): [('p1758', 'l88'), ('p1173', 'l88')],
                (3, 3, 9): [],
                (3, 3, 10): [('p175', 'l138'), ('p436', 'l138')]
                                  }
            print("{} -- physical test attack {}".format(process_name, datetime.datetime.now()))

            # attack only physical network
            physical_attack_title = csv_title_generator("result", x_coordinate, y_coordinate, exp, n_dependence=n_inter,
                                                        attack_type="physical", version=version, model=model)
            if logic_file_name:
                physical_attack_title = physical_attack_title.replace("result_","")
                lver = (logic_file_name.replace("ogic_exp_2.5_","")).replace(".csv","")
                physical_attack_title = "result_{}_{}".format(lver, physical_attack_title)
            if interlink_type:
                physical_attack_title = physical_attack_title.replace("result_", "")
                inter_name = "{}v{}".format(interlink_type_names[interlink_type], interlink_version)
                physical_attack_title = "result_{}_{}".format(inter_name, physical_attack_title)
            if legacy:
                physical_attack_title = "legacy_{}".format(physical_attack_title)
            if debug:
                print("OK DEBUG")
                physical_attack_title = "debug_{}".format(physical_attack_title)
            ################################################################
            if fix_bridge_nodes_interlinks:
                lv = int((logic_file_name.replace("logic_exp_2.5_v", "")).replace(".csv", ""))
                print(" KEY: {}".format((interlink_version, n_inter, lv)))
                interlinks_to_add = fix_interlink_dict[(interlink_version, n_inter, lv)]
                interlinks = network_system.get_interlinks()
                og_number_of_interlinks = len(interlinks.get_edgelist())
                print(og_number_of_interlinks)
                existing_nodes = interlinks.vs["name"]
                new_nodes_to_add = [edge[0] for edge in interlinks_to_add if edge[0] not in existing_nodes]
                interlinks.add_vertices(new_nodes_to_add)
                interlinks.add_edges(interlinks_to_add)
                new_number_of_interlinks = len(interlinks.get_edgelist())
                print("Links added: {}".format(new_number_of_interlinks-og_number_of_interlinks))
                print("Expected links to add: {}".format(len(fix_interlink_dict[(interlink_version, n_inter, lv)])))
                network_system.set_interlinks(interlinks)
                print(len((network_system.get_interlinks()).get_edgelist()))
                physical_attack_title = "m_{}".format(physical_attack_title)
            else:
                print("RUNNING WITHOUT FIXING INTERLINKS")
            ################################################################

            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, "test_results", sub_dir, "physical_random_attacks", physical_attack_title)
            print("{} -- will save results on: {}".format(process_name, path))
            tests_library.single_network_attack(network_system, "physical", path, iter_number, "NEW",
                                                process_name=process_name)

        if attack_localized:
            print("{} -- localized attack test {}".format(process_name, datetime.datetime.now()))
            # attack physical network using localized attacks
            radius = localized_attack_data["radius"]
            tests_library.localized_attack(iter_number, network_system, x_coordinate, y_coordinate, radius, n_inter,
                                           n_logic_suppliers, version, model, strategy=strategy, legacy=legacy)
            print("{} -- localized attack test {}".format(process_name, datetime.datetime.now()))
        #
        if attack_seismic:
            print("{} -- seismic attack test {}".format(process_name, datetime.datetime.now()))
            # aca la idea es poner una función que lea datos sísmicos de un archivo y llamé a la otra función que hace
            # en serio el ataque
            seismic_data_file = seismic_data["file"]
            tests_library.seismic_attacks(network_system, x_coordinate, y_coordinate, n_inter, version, model,
                                          seismic_data_file)
            print("{} -- seismic attack test {}".format(process_name, datetime.datetime.now()))

        else:
            pass

    elif logic_flag:
        # generate AS network
        as_graph = network_generators.generate_logic_network(n_logic, exponent=exp)
        network_system = InterdependentGraph()
        network_system.set_AS(as_graph)
        network_system.save_logic(exp, version=version)

        print("amount of connected components " + str(len(as_graph.clusters())))
        print("AS ready " + str(datetime.datetime.now()))

    elif physical_flag:
        if phys_iteration == 0:
            x_coord, y_coord = network_generators.generate_coordinates(n_phys, x_axis=x_coordinate, y_axis=y_coordinate)
            save_nodes_to_csv(x_coord, y_coord, x_coordinate, y_coordinate, exp, n_inter, n_logic_suppliers,
                              version=version)
        
        else:
            # generate physical network
            coord_dir = "networks/physical_networks/node_locations/" + \
                        csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version)
            coord_dict = get_list_of_coordinates_from_csv(coord_dir)

            phys_graph = network_generators.generate_physical_network(n_phys, model, coord_dict)
            network_system = InterdependentGraph()
            network_system.set_physical(phys_graph)
            # Save physical
            network_system.save_physical(x_coordinate, y_coordinate, exp, version=phys_iteration, model=model)

        print("phys ready " + str(datetime.datetime.now()))

    else:

        print("start {}".format(datetime.datetime.now()))

        phys_id_list = []
        for i in range(n_phys):
            phys_id_list.append('p{}'.format(i))

        logic_id_list = []
        for i in range(n_logic):
            logic_id_list.append('l{}'.format(i))

        as_suppliers = network_generators.set_logic_suppliers(logic_id_list, n_logic_suppliers)

        print("AS suppliers ready {}".format(datetime.datetime.now()))

        interdep_graph = network_generators.set_interdependencies(phys_id_list, logic_id_list, n_inter, as_suppliers)

        print("interdep ready {}".format(datetime.datetime.now()))

        phys_suppliers = network_generators.set_physical_suppliers(interdep_graph, as_suppliers)

        print("Phys suppliers ready {}".format(datetime.datetime.now()))

        network_system = InterdependentGraph()
        network_system.create_from_empty_logic_physical(logic_id_list, as_suppliers, phys_id_list, phys_suppliers,
                                                        interdep_graph)

        print("system created {}".format(datetime.datetime.now()))

        network_system.save_interlinks_and_providers(x_coordinate, y_coordinate, exp, n_inter, version=version)

        print("system saved {}".format(datetime.datetime.now()))
    print("run test done")


def add_edges(x_coordinate, y_coordinate, exp, n_inter, n_logic_suppliers, version, n_logic, n_phys, iter_number,
              model=[], phys_iteration=0, strategy='random,degree,distance,external'):
    path = os.path.dirname(os.path.abspath(__file__))

    add_random = 'random' in strategy
    add_degree = 'degree' in strategy
    add_distance = 'distance' in strategy
    add_local_hubs = 'local_hubs' in strategy
    add_external = 'external' in strategy
    # Read current edges
    physical_graph_dir = os.path.join(path, "networks", "physical_networks", "links",
                         csv_title_generator("physic", x_coordinate, y_coordinate, exp, version=version,
                                             model=model))
    print("Making new edges for: {}".format(csv_title_generator("physic", x_coordinate, y_coordinate, exp,
                                                                version=version,  model=model)))
    phys_graph = set_graph_from_csv(physical_graph_dir)

    # Read coordinates

    coord_dir = os.path.join(path, "networks", "physical_networks", "node_locations",
                             csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version))

    print("Getting nodes locations")

    #x_coord, y_coord = get_list_of_coordinates_from_csv(coord_dir)
    coord_dict = get_list_of_coordinates_from_csv(coord_dir)

    print("... done.")

    number_of_edges_to_add = 640

    print("Calculating new edges")
    if add_random:
        new_edges = network_generators.generate_edges_to_add_random(number_of_edges_to_add, phys_graph)
        strategy = "random"
    
    if add_degree:
        percentage = 97
        new_edges = network_generators.generate_edges_to_add_degree(phys_graph, percentage, number_of_edges_to_add)
        strategy = "degree"

    if add_local_hubs:
        percentage = 97
        new_edges = network_generators.generate_edges_to_add_distance_hubs(phys_graph, coord_dict, percentage,
                                                                           number_of_edges_to_add)
        strategy = "local_hubs"

    if add_distance:
        percentage = 97
        new_edges = network_generators.generate_edges_to_add_distance(phys_graph, coord_dict, percentage,
                                                                      number_of_edges_to_add)
        strategy = "distance"

    if add_external:
        dependence_tittle = "networks/" + csv_title_generator("dependence", x_coordinate, y_coordinate, exp, n_inter, 6,
                                                              version=version)
        dep_graph = set_graph_from_csv(dependence_tittle)
        percentage = 10
        new_edges = network_generators.genererate_edges_by_degree(phys_graph, coord_dict, percentage,
                                                                  number_of_edges_to_add, external=True,
                                                                  dependence_graph=dep_graph)
        strategy = "external"

    network_generators.save_edges_to_csv(new_edges, x_coordinate, y_coordinate, exp, version=version,
                                             model=model, strategy=strategy)
    print("Arcos creados")


def distributions(x_coordinate, y_coordinate, exp, model):
    dist = {}
    for i in range(1, 11):
        title = "networks/" + csv_title_generator("physic", x_coordinate, y_coordinate, exp, version=str(i), model=model)
        phys_graph = set_graph_from_csv(title)
        for vertex in phys_graph.vs:
            degree = vertex.degree()
            if degree not in dist:
                dist[degree] = 1
            else:
                dist[degree] += 1
    return dist


