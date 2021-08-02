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
    #########################
    fix_bridge_nodes_interlinks = False
    #########################
    title_mod = ""
    #########################
    capped_random = "distance"
    #########################

    attack_logic = 'logic' in attack_types
    attack_phys = 'physical' in attack_types
    attack_both = 'both' in attack_types
    attack_localized = 'localized' in attack_types
    #
    attack_seismic = 'seismic' in attack_types

    if READ_flag:
        print("{} -- start {}".format(process_name, datetime.datetime.now()))
        interlink_type_names = {"provider_priority": "pp", "full_random": "fr", "semi_random": "sr"}
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
            start_title = "candidates"

            if len(title_mod) > 0:
                start_title = "{}_{}".format(start_title, title_mod)
            title = csv_title_generator(start_title, x_coordinate, y_coordinate, exp, version=version, model=model)
            if len(capped_random) > 0 and strategy == "random":
                title = title.replace("candidates_", "candidates_cl_{}_".format(capped_random))
            path = os.path.join(path, "networks", "physical_networks", "extra_edges", strategy, title)

            edges_to_add = get_list_of_tuples_from_csv(path)
            network_system.add_edges_to_physical_network(edges_to_add)
            print("{} -- -> Added edges from: {}".format(process_name, path))
            sub_dir = strategy

        if attack_phys:
            # key = (ppv,ndep, lv)
            fix_interlink_dict = {

                (1, 7, 2): [('p1285', 'l52')],
                (1, 7, 3): [],
                (1, 7, 4): [('p1566', 'l279'), ('p303', 'l279'), ('p1983', 'l279'), ('p842', 'l279'), ('p951', 'l279'), ('p1447', 'l279')],
                (1, 7, 5): [],
                (1, 7, 6): [('p804', 'l87')],
                (1, 7, 7): [('p620', 'l2'), ('p683', 'l2'), ('p286', 'l2'), ('p770', 'l2'), ('p1650', 'l2'), ('p1178', 'l2')],
                (1, 7, 8): [('p1928', 'l88'), ('p22', 'l88'), ('p943', 'l88'), ('p1117', 'l88')],
                (1, 7, 9): [('p122', 'l179'), ('p643', 'l179')],
                (1, 7, 10): [],

                (3, 1, 1): [],
                (3, 2, 1): [('p353', 'l50')],
                (3, 3, 1): [('p1403', 'l50'), ('p1084', 'l50')],
                (3, 4, 1): [('p26', 'l50'), ('p154', 'l50')],
                (3, 5, 1): [('p1409', 'l50'), ('p506', 'l50')],
                (3, 6, 1): [('p202', 'l50')],
                (3, 7, 1): [('p830', 'l50'), ('p1666', 'l50'), ('p1573', 'l50'), ('p832', 'l50')],
                (3, 8, 1): [('p662', 'l50'), ('p171', 'l50'), ('p747', 'l50')],
                (3, 9, 1): [('p1752', 'l50'), ('p1041', 'l50'), ('p763', 'l50'), ('p526', 'l50'), ('p1242', 'l50'), ('p1498', 'l50'), ('p256', 'l50')],
                (3, 10, 1): [('p748', 'l50'), ('p266', 'l50'), ('p392', 'l50'), ('p1518', 'l50'), ('p1792', 'l50'), ('p322', 'l50'), ('p1566', 'l50')],

                (3, 1, 2): [],
                (3, 2, 2): [('p430', 'l52')],
                (3, 3, 2): [('p73', 'l52')],
                (3, 4, 2): [('p383', 'l52'), ('p1721', 'l52'), ('p1478', 'l52'), ('p1253', 'l294'), ('p1247', 'l294'), ('p388', 'l294')],
                (3, 5, 2): [('p1808', 'l52'), ('p209', 'l52'), ('p1071', 'l52')],
                (3, 6, 2): [('p1840', 'l52'), ('p1324', 'l52'), ('p842', 'l52')],
                (3, 7, 2): [('p1105', 'l52'), ('p1488', 'l52'), ('p1918', 'l52'), ('p1058', 'l52'), ('p915', 'l52'), ('p1277', 'l52'), ('p219', 'l294'), ('p1965', 'l294'), ('p1418', 'l294'),
                            ('p1426', 'l294'), ('p744', 'l294')],
                (3, 8, 2): [('p506', 'l294'), ('p1706', 'l294'), ('p1852', 'l294')],
                (3, 9, 2): [('p1373', 'l52'), ('p493', 'l52'), ('p592', 'l52'), ('p35', 'l52'), ('p1039', 'l52'), ('p716', 'l52'), ('p518', 'l52'), ('p1283', 'l294'), ('p1376', 'l294'),
                            ('p625', 'l294')],
                (3, 10, 2): [('p190', 'l52'), ('p791', 'l52'), ('p1696', 'l52'), ('p1482', 'l52'), ('p1855', 'l294'), ('p998', 'l294'), ('p250', 'l294'), ('p518', 'l294'), ('p1056', 'l294'),
                             ('p1590', 'l294')],

                (3, 1, 3): [],
                (3, 2, 3): [('p78', 'l192')],
                (3, 3, 3): [('p1553', 'l192'), ('p462', 'l192'), ('p387', 'l251')],
                (3, 4, 3): [('p1152', 'l192'), ('p131', 'l192'), ('p1498', 'l192'), ('p1468', 'l251'), ('p1369', 'l251')],
                (3, 5, 3): [('p1015', 'l251'), ('p885', 'l251'), ('p718', 'l251')],
                (3, 6, 3): [('p1684', 'l192'), ('p1527', 'l192')],
                (3, 7, 3): [('p679', 'l251'), ('p665', 'l251'), ('p673', 'l251'), ('p1452', 'l251')],
                (3, 8, 3): [('p789', 'l192'), ('p864', 'l192'), ('p1849', 'l192'), ('p1', 'l192'), ('p428', 'l192'), ('p841', 'l192'), ('p1377', 'l192'), ('p914', 'l251'), ('p287', 'l251'),
                            ('p139', 'l251'), ('p1225', 'l251'), ('p1058', 'l251'), ('p305', 'l251'), ('p351', 'l251')],
                (3, 9, 3): [('p1140', 'l192'), ('p508', 'l192'), ('p1679', 'l192'), ('p1381', 'l251'), ('p1077', 'l251'), ('p1576', 'l251'), ('p1774', 'l251'), ('p1091', 'l251')],
                (3, 10, 3): [('p473', 'l192'), ('p1364', 'l192'), ('p1379', 'l192'), ('p744', 'l192'), ('p1037', 'l192'), ('p1400', 'l192'), ('p598', 'l192'), ('p1569', 'l192'), ('p1486', 'l251')],

                (3, 1, 4): [],
                (3, 2, 4): [('p1957', 'l279')],
                (3, 3, 4): [],
                (3, 4, 4): [('p1814', 'l279'), ('p104', 'l279'), ('p1979', 'l279')],
                (3, 5, 4): [('p1002', 'l279'), ('p1034', 'l279')],
                (3, 6, 4): [('p124', 'l279')],
                (3, 7, 4): [('p1261', 'l279'), ('p502', 'l279'), ('p1477', 'l279'), ('p1731', 'l279'), ('p355', 'l279')],
                (3, 8, 4): [('p1206', 'l279')],
                (3, 9, 4): [('p567', 'l279'), ('p814', 'l279'), ('p112', 'l279'), ('p730', 'l279'), ('p960', 'l279'), ('p563', 'l279'), ('p746', 'l279'), ('p1888', 'l279')],
                (3, 10, 4): [('p944', 'l279'), ('p999', 'l279'), ('p393', 'l279')],

                (3, 1, 5): [],
                (3, 2, 5): [('p15', 'l138')],
                (3, 3, 5): [('p1358', 'l138'), ('p1877', 'l138')],
                (3, 4, 5): [('p1689', 'l138'), ('p293', 'l138')],
                (3, 5, 5): [('p1070', 'l138'), ('p1142', 'l138'), ('p178', 'l138')],
                (3, 6, 5): [],
                (3, 7, 5): [('p1461', 'l138'), ('p59', 'l138'), ('p1629', 'l138'), ('p257', 'l138')],
                (3, 8, 5): [('p837', 'l138'), ('p428', 'l138'), ('p1093', 'l138')],
                (3, 9, 5): [],
                (3, 10, 5): [],

                (3, 1, 6): [],
                (3, 2, 6): [('p388', 'l87')],
                (3, 3, 6): [],
                (3, 4, 6): [('p198', 'l87'), ('p1095', 'l87'), ('p650', 'l87')],
                (3, 5, 6): [('p393', 'l87'), ('p1972', 'l87')],
                (3, 6, 6): [('p1550', 'l87'), ('p1445', 'l87'), ('p688', 'l87'), ('p104', 'l87')],
                (3, 7, 6): [],
                (3, 8, 6): [('p205', 'l87'), ('p782', 'l87'), ('p1159', 'l87'), ('p570', 'l87'), ('p351', 'l87'), ('p1510', 'l87'), ('p646', 'l87')],
                (3, 9, 6): [('p571', 'l87'), ('p354', 'l87'), ('p522', 'l87')],
                (3, 10, 6): [('p1946', 'l87'), ('p1626', 'l87'), ('p774', 'l87'), ('p107', 'l87'), ('p466', 'l87')],

                (3, 1, 7): [],
                (3, 2, 7): [('p1187', 'l2')],
                (3, 3, 7): [],
                (3, 4, 7): [('p857', 'l2'), ('p1803', 'l2')],
                (3, 5, 7): [('p1335', 'l2'), ('p1742', 'l2'), ('p242', 'l2'), ('p1078', 'l2')],
                (3, 6, 7): [('p1907', 'l2'), ('p264', 'l2'), ('p964', 'l2'), ('p630', 'l2')],
                (3, 7, 7): [('p1350', 'l2')],
                (3, 8, 7): [],
                (3, 9, 7): [('p1170', 'l2'), ('p1250', 'l2'), ('p501', 'l2'), ('p214', 'l2'), ('p858', 'l2'), ('p1525', 'l2')],
                (3, 10, 7): [('p1263', 'l2'), ('p1012', 'l2')],

                (3, 1, 8): [],
                (3, 2, 8): [],
                (3, 3, 8): [('p1758', 'l88'), ('p1173', 'l88')],
                (3, 4, 8): [('p1152', 'l88'), ('p1790', 'l88'), ('p793', 'l88')],
                (3, 5, 8): [],
                (3, 6, 8): [],
                (3, 7, 8): [('p1140', 'l88'), ('p261', 'l88'), ('p347', 'l88')],
                (3, 8, 8): [('p187', 'l88'), ('p423', 'l88')],
                (3, 9, 8): [('p1235', 'l88'), ('p1662', 'l88'), ('p1402', 'l88'), ('p1646', 'l88')],
                (3, 10, 8): [('p515', 'l88'), ('p1154', 'l88')],

                (3, 1, 9): [],
                (3, 2, 9): [('p54', 'l179')],
                (3, 3, 9): [],
                (3, 4, 9): [('p322', 'l179'), ('p1973', 'l179'), ('p1046', 'l179')],
                (3, 5, 9): [('p1554', 'l179'), ('p634', 'l179'), ('p54', 'l179')],
                (3, 6, 9): [('p1469', 'l179')],
                (3, 7, 9): [],
                (3, 8, 9): [('p770', 'l179'), ('p1053', 'l179'), ('p1581', 'l179'), ('p906', 'l179'), ('p1339', 'l179'), ('p1047', 'l179'), ('p126', 'l179')],
                (3, 9, 9): [('p1373', 'l179'), ('p537', 'l179'), ('p1197', 'l179'), ('p1006', 'l179'), ('p735', 'l179')],
                (3, 10, 9): [('p890', 'l179'), ('p1387', 'l179'), ('p1551', 'l179'), ('p494', 'l179'), ('p1004', 'l179'), ('p46', 'l179'), ('p1890', 'l179'), ('p1096', 'l179')],

                (3, 1, 10): [],
                (3, 2, 10): [('p313', 'l138')],
                (3, 3, 10): [('p175', 'l138'), ('p436', 'l138')],
                (3, 4, 10): [('p1553', 'l138'), ('p1119', 'l138')],
                (3, 5, 10): [('p90', 'l138'), ('p780', 'l138'), ('p35', 'l138')],
                (3, 6, 10): [],
                (3, 7, 10): [('p1333', 'l138'), ('p1692', 'l138'), ('p153', 'l138'), ('p270', 'l138')],
                (3, 8, 10): [('p174', 'l138'), ('p1304', 'l138'), ('p1172', 'l138')],
                (3, 9, 10): [],
                (3, 10, 10): []

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
            if len(title_mod) > 0:
                physical_attack_title = "d{}_{}".format(title_mod, physical_attack_title)
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

            if len(capped_random) > 0 and strategy == "random":
                path = os.path.join(path, "test_results", sub_dir, "physical_random_attacks", capped_random, physical_attack_title)
            else:
                path = os.path.join(path, "test_results", sub_dir, "physical_random_attacks", physical_attack_title)
            print("{} -- will save results on: {}".format(process_name, path))
            tests_library.single_network_attack(network_system, "physical", path, iter_number, "NEW",
                                                process_name=process_name)

        if attack_localized:

            # attack only physical network
            localized_attack_title = csv_title_generator("result", x_coordinate, y_coordinate, exp, n_dependence=n_inter, attack_type="localized", version=version, model=model)
            if logic_file_name:
                localized_attack_title = localized_attack_title.replace("result_", "")
                lver = (logic_file_name.replace("ogic_exp_2.5_", "")).replace(".csv", "")
                localized_attack_title = "result_{}_{}".format(lver, localized_attack_title)
            if interlink_type:
                localized_attack_title = localized_attack_title.replace("result_", "")
                inter_name = "{}v{}".format(interlink_type_names[interlink_type], interlink_version)
                localized_attack_title = "result_{}_{}".format(inter_name, localized_attack_title)
            if legacy:
                localized_attack_title = "legacy_{}".format(localized_attack_title)
            if debug:
                print("OK DEBUG")
                localized_attack_title = "debug_{}".format(localized_attack_title)
            if len(title_mod) > 0:
                localized_attack_title = "d{}_{}".format(title_mod, localized_attack_title)

            print("{} -- will save results on: {}".format(process_name, localized_attack_title))

            print("{} -- localized attack test {}".format(process_name, datetime.datetime.now()))
            # attack physical network using localized attacks
            radius = localized_attack_data["radius"]
            tests_library.localized_attack(iter_number, network_system, x_coordinate, y_coordinate, radius, n_inter,
                                           n_logic_suppliers, version, model, strategy=strategy, legacy=legacy, f_name=localized_attack_title)
            print("{} -- localized attack test {}".format(process_name, datetime.datetime.now()))
        #
        if attack_seismic:
            # attack only physical network
            seismic_attack_title = csv_title_generator("result", x_coordinate, y_coordinate, exp, n_dependence=n_inter, attack_type="seismic", version=version, model=model)
            if logic_file_name:
                seismic_attack_title = seismic_attack_title.replace("result_", "")
                lver = (logic_file_name.replace("ogic_exp_2.5_", "")).replace(".csv", "")
                seismic_attack_title = "result_{}_{}".format(lver, seismic_attack_title)
            if interlink_type:
                seismic_attack_title = seismic_attack_title.replace("result_", "")
                inter_name = "{}v{}".format(interlink_type_names[interlink_type], interlink_version)
                seismic_attack_title = "result_{}_{}".format(inter_name, seismic_attack_title)
            if legacy:
                seismic_attack_title = "legacy_{}".format(seismic_attack_title)
            if debug:
                print("OK DEBUG")
                seismic_attack_title = "debug_{}".format(seismic_attack_title)
            if len(title_mod) > 0:
                seismic_attack_title = "d{}_{}".format(title_mod, seismic_attack_title)

            print("{} -- will save results on: {}".format(process_name, seismic_attack_title))

            print("{} -- seismic attack test {}".format(process_name, datetime.datetime.now()))
            # aca la idea es poner una función que lea datos sísmicos de un archivo y llamé a la otra función que hace
            # en serio el ataque
            seismic_data_file = seismic_data["file"]

            tests_library.seismic_attacks(network_system, x_coordinate, y_coordinate, n_inter, version, model, seismic_data_file, save_in=seismic_attack_title)
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


