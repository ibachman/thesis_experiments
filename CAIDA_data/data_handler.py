import csv
import igraph
import re
import matplotlib.pyplot as plt
import os

def parse_ipinfowebpage(web_file):
    with open(web_file, 'r') as asn_file:
        lines = asn_file.readlines()

        # find asn + number
        asn_number_found = False
        asn_number_count = 2
        asn_number = "---"

        # find asn type
        asn_type_found = False
        asn_type_count = 3
        asn_type = "---"

        # find peers
        finding_peers = False
        asn_peers = []

        # find upstreams
        finding_upstreams = False
        asn_upstreams = []

        # find downstrams
        finding_downstreams = False
        asn_downstreams = []

        for line in lines:
            # find asn + number
            if "AS number details" in line:
                asn_number_found = True
            if asn_number_found and asn_number_count > 0:
                asn_number_count -= 1
                continue
            elif asn_number_found and asn_number_count == 0:
                asn_number = ((re.search('>(.*)<', line)).group(1)).replace("AS", "")
                asn_number_found = False

            # find asn type
            if "ASN type" in line:
                asn_type_found = True
            if asn_type_found and asn_type_count > 0:
                asn_type_count -= 1
                continue
            elif asn_type_found and asn_type_count == 0:
                asn_type = (line.replace(" ", "").replace("\n", ""))
                asn_type_found = False

            # find asn peers
            if "<div id=\"block-peers\" class=\"pt-3 pb-1\">" in line:
                finding_peers = True
            if finding_peers:
                if "<div id=\"block-upstreams\" class=\"pt-3 pb-1\">" in line:
                    finding_peers = False
                    finding_upstreams = True
                if ">AS" in line:
                    peer = (re.search('>(.*)<', line)).group(1)
                    asn_peers.append(peer.replace("AS", ""))
            if finding_upstreams:
                if "<div id=\"block-downstreams\" class=\"pt-3 pb-1\">" in line:
                    finding_upstreams = False
                    finding_downstreams = True
                if ">AS" in line:
                    upstream = (re.search('>(.*)<', line)).group(1)
                    asn_upstreams.append(upstream.replace("AS", ""))
            if finding_downstreams:
                if "Related Networks" in line:
                    finding_downstreams = False
                    break
                if ">AS" in line:
                    downstream = (re.search('>(.*)<', line)).group(1)
                    asn_downstreams.append(downstream.replace("AS", ""))

    print("\n##########")
    print("AS{}: {},".format(asn_number, asn_type))
    print("##########\n")
    for peer in asn_peers:
        print("{}|{}|0|ispinfo".format(asn_number, peer))
    for upstream in asn_upstreams:
        print("{}|{}|-1|ispinfo".format(upstream, asn_number))
    for downstream in asn_downstreams:
        print("{}|{}|-1|ispinfo".format(asn_number, downstream))
    print("")


def parse_different_as_from_html(web_file):
    asn_list = []
    with open(web_file, 'r') as asn_file:
        lines = asn_file.readlines()
        for line in lines:
            if "<td class=\"p-3\"><a href=\"/AS" in line:
                asn = (re.search('\">(.*)</a></td>', line)).group(1)
                asn = asn.split(">")[1]
                asn_list.append(asn.replace("AS", ""))
    return list(set(asn_list))


# returns dictionary with ASN as key and name of the AS as value
def get_chile_asn(avoid_inactive=True):
    path = os.path.dirname(os.path.abspath(__file__))

    file_name = "chile_ASN.csv"

    all_asn = {}
    with open(os.path.join(path, file_name), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            if row[2] == "Inactive" and avoid_inactive:
                continue
            as_number = row[0].replace("AS", "")
            all_asn[as_number] = row[1]
    return all_asn


def get_chile_provider_candidates():
    asn_dict = get_chile_asn()
    provider_name_must_contain = ['ctc', 'ctr', 'telefónica', 'telefonica', 'vtr', 'gtd', 'entel', 'telmex', 'claro', 'zgh', 'powerhost', 'pacifico',
                                  'orbyta']
    provider_candidates = []
    for asn in asn_dict.keys():
        as_name = asn_dict[asn].lower()
        for provider_name_key in provider_name_must_contain:
            if provider_name_key in as_name:
                provider_candidates.append(asn)
    return list(set(provider_candidates))


def get_chile_providers_using_isp_marker(use_international_connection=None, avoid_inactive=True, get_international_connection_only=False):
    if use_international_connection != None:
        has_international_connection_dict = has_international_connection(use_international_connection)
    international_connection_only = []
    path = os.path.dirname(os.path.abspath(__file__))
    file_name = "chile_ASN.csv"
    asn_with_isp_mark = []
    with open(os.path.join(path, file_name), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            if row[2] == "Inactive" and avoid_inactive:
                continue
            as_number = row[0].replace("AS", "")
            if row[2] == "ISP":
                asn_with_isp_mark.append(as_number)
            elif use_international_connection != None:
                if as_number in has_international_connection_dict.keys():
                    if has_international_connection_dict[as_number]:
                        asn_with_isp_mark.append(as_number)
                        if get_international_connection_only:
                            international_connection_only.append(as_number)
    if get_international_connection_only:
        asn_with_isp_mark = international_connection_only

    return asn_with_isp_mark




# returns all pairs of connected AS according to file contents
def get_caida_data_asn(file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    all_asn = {}
    with open(os.path.join(path, file_name), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|', quotechar='|')
        for row in reader:

            if row[1] in all_asn.keys():
                all_asn[row[1]] += [row[0]]
            else:
                all_asn[row[1]] = [row[0]]

            if row[0] in all_asn.keys():
                all_asn[row[0]] += [row[1]]
            else:
                all_asn[row[0]] = [row[1]]

    return all_asn


# makes a Chilean BGP edge list using the AS relations described in the file and chilean ASN
def set_as_edge_list(bgp_rel_filename):
    graph_edge_list = []
    node_names = {}
    caida = get_caida_data_asn(bgp_rel_filename)
    chile = get_chile_asn()
    for asn in chile:
        if asn in caida.keys():
            neighbors = [x for x in caida[asn] if x in chile.keys()]
            if len(neighbors) > 0:
                node_names[asn] = 0
            for n in neighbors:
                graph_edge_list.append((asn, n))
                node_names[n] = 0
    return graph_edge_list, list(node_names.keys())


def has_international_connection(bgp_rel_filename):
    caida = get_caida_data_asn(bgp_rel_filename)
    chile = get_chile_asn()
    international_conn_dict = {}
    for asn in chile:
        if asn in caida.keys():
            neighbors = [x for x in caida[asn] if x not in chile.keys()]
            if len(neighbors) > 0:
                international_conn_dict[asn] = True
            else:
                international_conn_dict[asn] = False
        else:
            print(asn)
    return international_conn_dict


# returns graph for Chilean BGP edge list using the AS relations described in the file and chilean ASN
def make_graph(bgp_rel_filename, remove_nodes=[]):
    edge_list, node_names = set_as_edge_list(bgp_rel_filename)
    graph = igraph.Graph(len(node_names))
    graph.vs['name'] = node_names
    graph.add_edges(edge_list)
    if len(remove_nodes) > 0:
        graph.delete_vertices(remove_nodes)
    return graph


# Get providers using ISP nodes with international connections
def find_chilean_provider_nodes(isp_asn, bgp_rel_filename):
    caida = get_caida_data_asn(bgp_rel_filename)
    chile = get_chile_asn()
    providers = []
    print("number of ISP ASN: {}".format(len(isp_asn)))
    count = 0
    for asn in isp_asn:
        if asn in caida.keys():
            neighbors = [x for x in caida[asn] if x not in chile.keys()]
            if len(neighbors) > 0:
                count += 1
                providers.append(asn)
            else:
                pass
                #print("-----")
    print("number of ISP that go outside chile: {}".format(count))
    print(len(providers))
    return providers


def get_nodes_that_go_outside_chile(directed_graph, bgp_rel_filename, mode=None):
    return find_chilean_provider_nodes_directed(directed_graph, directed_graph.vs["name"], bgp_rel_filename, mode=mode)


def find_chilean_provider_nodes_directed(directed_graph, isp_asn, bgp_rel_filename, mode=None):
    providers = find_chilean_provider_nodes(isp_asn, bgp_rel_filename)
    node_names = directed_graph.vs['name']
    final_providers = []
    for provider in providers:
        if provider not in node_names:
            continue
        provider_id = directed_graph.vs.find(provider)
        if directed_graph.degree(provider_id, mode=mode) > 0: # before: directed_graph.degree(provider_id, mode='in')
            final_providers.append(provider)
    return final_providers


# Get number and "severity" of bridge nodes
def get_all_bridge_nodes(providers, graph):
    print(len(graph.vs))
    bridge_nodes_dict = {}
    nodes = graph.vs
    total_number_of_nodes = len(nodes)
    # for each node
    for node in nodes:
        graph_copy = graph.copy()
        nodes_lost = 0
    #   remove node
        graph_copy.delete_vertices([node])
    #   get connected components
        components = graph_copy.clusters()
    #   for each component
    #       if no providers are contained in current
    #           sum to number of nodes lost
        for component in components:
            has_provider = False
            node_names_within_component = graph_copy.vs(component)['name']
            for provider in providers:
                if provider in node_names_within_component:
                    has_provider = True
                    break
            if not has_provider:
                nodes_lost += len(component)
    #   add fraction of node lost to dict with ASN removed as key
        if nodes_lost > 0:
            node_name = node['name']
            bridge_nodes_dict[node_name] = nodes_lost / total_number_of_nodes
    # return dict
    return bridge_nodes_dict


# get directed edges
def get_caida_data_asn_as_directed_edges(file_name):
    chile = list(get_chile_asn().keys())
    is_peer = '0'
    edge_list = {}
    node_names = {}
    path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(path, file_name), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|', quotechar='|')
        for row in reader:
            if row[0] in chile and row[1] in chile:
                #if row[0] == '14259' or row[1] == '14259':
                #    print(row)
                node_names[row[0]] = '.'
                node_names[row[1]] = '.'
                if row[2] == is_peer:
                    edge_1 = (row[0], row[1])
                    edge_2 = (row[1], row[0])
                    edge_list[edge_1] = 1
                    edge_list[edge_2] = 1
                else:
                    edge = (row[1], row[0])
                    edge_list[edge] = 2
    return list(edge_list.keys()), list(node_names.keys())


# Use directed links instead of non-directed
def make_directed_graph(bgp_rel_filename, remove_nodes=[], use_html_names=True, use_index_names=False):
    print(" making directed graph from: {}".format(bgp_rel_filename))
    edge_list, node_names = get_caida_data_asn_as_directed_edges(bgp_rel_filename)
    if use_html_names:
        node_names = list(get_chile_asn().keys())
        print(len(node_names))
    graph = igraph.Graph(len(node_names), directed=True)
    graph.vs['name'] = node_names
    graph.add_edges(edge_list)
    if len(remove_nodes) > 0:
        graph.delete_vertices(remove_nodes)

    if use_index_names:
        for node in graph.vs:
            node['asn'] = node['name']
            node['name'] = "l{}".format(node.index)
    return graph


def get_all_bridge_nodes_directed(providers, graph):
    #print(len(graph.vs))
    #print(len(providers))
    #print(len(graph.clusters(mode='weak')))
    nodes = graph.vs
    total_number_of_nodes = len(nodes)
    bridge_nodes_dict = {}

    # for each node
    for node in nodes:
        graph_copy = graph.copy()
        nodes_lost = 0
    #   remove node
        graph_copy.delete_vertices([node])
    #   get connected components
        components = graph_copy.clusters(mode='weak')
    #   for each component
    #       if no providers are contained in current
    #           sum to number of nodes lost
        for component in components:
            node_names_within_component = graph_copy.vs(component)['name']
            providers_within_component = [x for x in providers if x in node_names_within_component]

            if len(providers_within_component) < 1:
                nodes_lost += len(component)
            else:
                has_path = []
                # initialize has_path array
                for i in range(total_number_of_nodes - 1):
                    has_path.append(0)
                # check nodes that have a path to some provider
                for provider in providers_within_component:
                    paths = graph_copy.get_shortest_paths(provider, mode='in', output='vpath')
                    # if node j has a path set has_path[j] = 1
                    for j in range(total_number_of_nodes - 1):
                        if len(paths[j]) > 0:
                            has_path[j] = 1
                nodes_lost += len(component) - sum(has_path)
    #   add fraction of node lost to dict with ASN removed as key only if they are bridge nodes
        if nodes_lost > 0:
            node_name = node['name']
            bridge_nodes_dict[node_name] = nodes_lost / total_number_of_nodes

    return bridge_nodes_dict


def get_bridge_nodes_directed_2(providers, graph):
    nodes = graph.vs
    total_number_of_nodes = len(nodes)
    bridge_nodes_dict = {}
    for node in nodes:
        deleted_node_name = node['name']
        reachable_nodes = []
        graph_copy = graph.copy()
        graph_copy.delete_vertices([node])
        for provider in providers:
            if provider == node['name']:
                continue
            #print(graph.vs(name=provider)[0].index)
            paths = graph_copy.get_shortest_paths(provider, mode='in', output='vpath')
            for i in range(len(paths)):
                if len(paths[i]) > 0:
                    reachable_nodes.append(i)
        set_of_reachable_nodes = list(set(reachable_nodes))
        unreachable_nodes = []
        for i in range(len(graph_copy.vs)):
            if i not in set_of_reachable_nodes:
                unreachable_nodes.append(graph_copy.vs[i]['name'])
        #if len(set_of_reachable_nodes) == 298:
        #    print(unreachable_nodes+[deleted_node_name])
        if len(set_of_reachable_nodes) < 299:
            nodes_lost = len(unreachable_nodes)
            bridge_nodes_dict[deleted_node_name] = nodes_lost / total_number_of_nodes

            print("Node removed: {}, Number of reachable nodes: {}, Lost nodes: {}".format(deleted_node_name, len(set_of_reachable_nodes), len(unreachable_nodes)))

            # check if unreachable nodes are neighbors of the deleted node
            neighbors_of_deleted_node_1 = graph.neighbors(deleted_node_name, mode="in")
            neighbors_of_deleted_node_2 = graph.neighbors(deleted_node_name, mode="out")
            neighbors_of_deleted_node = list(set(neighbors_of_deleted_node_1 + neighbors_of_deleted_node_2))
            neighbors_of_deleted_node_names = graph.vs[neighbors_of_deleted_node]["name"]
            # find unreachable nodes that are neighbors
            aux_list = []
            for unreachable_node in unreachable_nodes:
                if unreachable_node in neighbors_of_deleted_node_names:
                    aux_list.append(unreachable_node)
                else:
                    print(unreachable_node)
                    print("270102" in unreachable_nodes)
            print("-------> {}".format(len(aux_list)))
    return bridge_nodes_dict


# Make figures
def print_graph(graph, providers=[], bridge_nodes=[], bn_providers=[], out_nodes=[], use_label=False):
    labels = graph.vs["name"]
    layout = graph.layout_auto()
    color = []
    for n in graph.vs:
        if n['name'] in bridge_nodes:
            color.append('#254bf7')
        elif n['name'] in bn_providers:
            color.append('red')
        elif n['name'] in providers:
            color.append('#ff7373')
        elif n['name'] in out_nodes:
            color.append('green')
        else:
            color.append('#8197fc')
    visual_style = {}
    if use_label:
        visual_style["vertex_label"] = labels

    visual_style["vertex_color"] = color
    visual_style["bbox"] = (1000, 1000)
    visual_style["edge_arrow_size"] = 0.8
    visual_style["vertex_size"] = 20
    igraph.plot(graph, layout=layout, **visual_style)


def get_node_clasification_directed(bgp_file_name):
    tentative_providers = ['7418',  # telefonica? '52489', '52396',
                           '22047',  # vtr ? '19632',
                           '6535', '6429', '263173', '27978', '19338',  # telmex
                           '27651', '27925', '6471', '27986', '28047', '19228',  # entel '52252',
                           '14117', '27680', '16629', '15311',  # telefonica del sur
                           '27995',  # claro
                           '14259',  # Gtd  '270059', '263184',
                           '16629', '7004',  # CTC '263208'
                           '18822',  # manquehuenet,
                           '263237'  # '263702'
                           ]
    tentative_providers = get_chile_provider_candidates()

    chile_asn = get_chile_asn()

    directed_graph = make_directed_graph(bgp_file_name, remove_nodes=['64111', '52368', '52512'])
    nodes_with_international_connection = get_nodes_that_go_outside_chile(directed_graph, bgp_file_name, mode='in')
    chilean_providers_directed_graph = find_chilean_provider_nodes_directed(directed_graph, tentative_providers, bgp_file_name, mode='in')
    bridge_nodes_directed_graph_using_out_nodes = get_all_bridge_nodes_directed(nodes_with_international_connection, directed_graph)
    print("++++++++++++++")
    print(len(nodes_with_international_connection))
    print(len(chilean_providers_directed_graph))
    print("++++++++++++++")

    #set_chilean_providers = set(chilean_providers_directed_graph)
    set_chilean_providers = set(tentative_providers)
    set_bridge_nodes_using_out_nodes = set(bridge_nodes_directed_graph_using_out_nodes.keys())
    set_nodes_with_international_connection = set(nodes_with_international_connection)

    set_nodes_of_interest = set_chilean_providers.union(set_bridge_nodes_using_out_nodes.union(set_nodes_with_international_connection))

    dict_info_nodes_of_interest = {}
    for node in set_nodes_of_interest:
        dict_info_nodes_of_interest[node] = {}
        if node in set_chilean_providers:
            dict_info_nodes_of_interest[node]["is_provider"] = True
        else:
            dict_info_nodes_of_interest[node]["is_provider"] = False
        if node in set_bridge_nodes_using_out_nodes:
            dict_info_nodes_of_interest[node]["is_bridge_node"] = True
        else:
            dict_info_nodes_of_interest[node]["is_bridge_node"] = False
        if node in set_nodes_with_international_connection:
            dict_info_nodes_of_interest[node]["is_out_node"] = True
        else:
            dict_info_nodes_of_interest[node]["is_out_node"] = False

    print("|    ASN     |   prov   |   bn  |   on  |    name")
    for node in set_nodes_of_interest:
        node_name = node
        for i in range(6 - len(node)):
            node_name += " "
        line = "|    {}  |".format(node_name)
        if dict_info_nodes_of_interest[node]["is_provider"]:
            line += "    YES   |"
        else:
            line += "          |"
        if dict_info_nodes_of_interest[node]["is_bridge_node"]:
            line += "  YES  |"
        else:
            line += "       |"
        if dict_info_nodes_of_interest[node]["is_out_node"]:
            line += "  YES  |"
        else:
            line += "       |"
        line += "   {}".format(chile_asn[node])
        print(line)


def brute_test():

    get_node_clasification_directed('20211201_as_rel2.csv')
    #exit(89)

    tentative_providers2 = ['7418', '52489', '52396',  # telefonica?
                 '22047', '19632', # vtr ?
                 '6535', '6429', '263173', '27978', '19338',  # telmex
                 '27651', '27925', '6471', '27986', '28047', '19228', '52252', # entel
                 '14117', '27680', '16629', '15311',  #telefonica del sur
                 '27995',  #claro
                 '14259', '270059', '263184', # Gtd
                 '16629', '7004', '263208', # CTC
                 '18822',  #manquehuenet,
                 '263237', '263702'  # estos son ultra importantes
                           ]
    #print(len(tentative_providers))
    tentative_providers = list(set(get_chile_provider_candidates()).union(set(tentative_providers2)))
    print(len(tentative_providers))
    chilean_providers = find_chilean_provider_nodes(tentative_providers, '20211201_as_rel2.csv')
    directed_graph = make_directed_graph('20211201_as_rel.csv', remove_nodes=['64111', '52368', '52512'])

    in_neighbors = directed_graph.neighbors('266830', mode='in')
    in_neighbors_names = []
    for n in in_neighbors:
        in_neighbors_names.append(directed_graph.vs['name'][n])
    print(in_neighbors_names)

    print(directed_graph.neighbors('266830', mode='out'))
    exit(99)

    non_directed_graph = make_graph('20211201_as_rel2.csv', remove_nodes=['64111', '52368', '52512'])
    print("-------------")
    nodes_with_international_connection = get_nodes_that_go_outside_chile(directed_graph, '20211201_as_rel2.csv')
    print('263237' in nodes_with_international_connection)
    print('263702' in nodes_with_international_connection)
    print("-------------")
    #chilean_providers_directed_graph = find_chilean_provider_nodes_directed(directed_graph, tentative_providers, '20211201_as_rel2.csv')
    chilean_providers_directed_graph = tentative_providers
    print("------+++++-------")
    print(len(chilean_providers_directed_graph))
    print("------+++++-------")

    print("number of providers (directed): {}".format(len(chilean_providers_directed_graph)))
    print("number of international connection nodes (directed): {}".format(len(nodes_with_international_connection)))

    bridge_nodes_directed_graph = get_all_bridge_nodes_directed(chilean_providers_directed_graph, directed_graph)
    print("number of bridge nodes using providers as providers (???): {}".format(len(bridge_nodes_directed_graph)))
    bridge_nodes_directed_graph_using_out_nodes = get_all_bridge_nodes_directed(nodes_with_international_connection, directed_graph)
    print("number of bridge nodes using out nodes as providers: {}".format(len(bridge_nodes_directed_graph_using_out_nodes)))

    # veamos como cambia lo brutal de los bridge nodes
    bridge_nodes_intesection = [x for x in list(bridge_nodes_directed_graph.keys()) if x in list(bridge_nodes_directed_graph_using_out_nodes.keys())]
    for node in bridge_nodes_intesection:
        if bridge_nodes_directed_graph[node] != bridge_nodes_directed_graph_using_out_nodes[node]:
            print("[{}] loss using providers: {}, loss using out nodes: {}".format(node, bridge_nodes_directed_graph[node]*263, bridge_nodes_directed_graph_using_out_nodes[node]*263))

    exit(4)

    bridge_nodes_non_directed_graph = get_all_bridge_nodes(chilean_providers_directed_graph, non_directed_graph)

    bridge_nodes = []
    provider_bridge_nodes = []
    for node in bridge_nodes_directed_graph.keys():
        if node in chilean_providers_directed_graph:
            provider_bridge_nodes.append(node)
        else:
            bridge_nodes.append(node)

    print_graph(directed_graph, providers=chilean_providers_directed_graph, bridge_nodes=bridge_nodes, bn_providers=provider_bridge_nodes, out_nodes=nodes_with_international_connection)
    exit(78)
    print(directed_graph.neighbors('263237', mode='out'))
    for n in chilean_providers_directed_graph:
        print("- {}".format(n))
        paths = directed_graph.get_shortest_paths(n, mode='in', output='vpath')
        print(len([x for x in paths if len(x) > 0]))
