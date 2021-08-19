import csv
import numpy
import networkx as nx
from interdependent_network_library import csv_title_generator
import tests_library as tl
import os
import random
import igraph
import interdependent_network_library


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

def data_at_x_percent_damage(node_damage_fraction, number_of_nodes, path, geometry, exp, attack, system_name, legacy=False, lv=None):
    file_line_number = get_line_number_with(node_damage_fraction, number_of_nodes)

    if not lv:
        imax_axis = [3]  # get_imax_tested()
        version = "average"

        LCC = []
        for imax in imax_axis:
            file_name = generate_csv_file_name(geometry, exp, imax, attack, version, system_name)
            if legacy:
                file_name = "legacy_{}".format(file_name)
            with open(os.path.join(path, file_name)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line = 0
                for row in csv_reader:
                    if line == file_line_number:
                        LCC.append(float(row[1]))
                        break
                    line += 1

        return {"x_axis": imax_axis, "y_axis": LCC}
    else:
        path = path.replace("average_results/", "")
        imax_axis = [3, 5, 7, 10]  # get_imax_tested()
        average_gls = []
        for imax in imax_axis:
            # get average on the fly
            gl = []
            for version in range(1, 11):
                file_name = "result_ppv3_lv{}_{}_exp_{}_ndep_{}_att_physical_v{}_m_{}.csv".format(lv, geometry, exp, imax, version, system_name)
                with open(os.path.join(path, "physical_random_attacks", file_name)) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line = 0
                    for row in csv_reader:
                        if line == file_line_number:
                            gl.append(float(row[1]))
                            break
                        line += 1
            average_gls.append(numpy.mean(gl))
        return {"x_axis": imax_axis, "y_axis": average_gls}



def create_average_results_file_in(path, destination_path, geometry, exp, imax, attack, versions, system_name,
                                   legacy=False, debug=False, lv=1):
    all_data = {}
    for version in versions:
        file_name = generate_csv_file_name(geometry, exp, imax, attack, version, system_name)
        if legacy:
            file_name = "legacy_{}".format(file_name)
        if debug:
            file_name = "debug_{}".format(file_name)

        with open(os.path.join(path, file_name)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 1
            for row in csv_reader:
                if line_count == 1:
                    line_count += 1
                    continue
                key = row[0]
                if key not in all_data:
                    all_data[key] = []
                all_data[key].append(float(row[1]))
                line_count += 1
    for key in all_data:
        mean = numpy.mean(all_data[key])
        all_data[key] = mean
    file_name = generate_csv_file_name(geometry, exp, imax, attack, "average", system_name)
    if legacy:
        file_name = "legacy_{}".format(file_name)
    if debug:
        file_name = "debug_{}".format(file_name)
    final_file_name_and_path = os.path.join(destination_path, file_name)

    with open(final_file_name_and_path, mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['1-p', 'Mean'])
        for key in sorted(all_data.keys()):
            file_writer.writerow([str(key), str(all_data[key])])


def get_imax_tested():
    return [1, 3, 5, 7, 10]


def generate_csv_file_name(geometry, exp, imax, attack, version, system_name, other=""):
    geometry = str(geometry)
    exp = str(exp)
    imax = str(imax)
    attack = str(attack)
    version = str(version)
    system_name = str(system_name)
    if version == "average":
        return "average_result_{}_exp_{}_ndep_{}_att_{}_m_{}.csv".format(geometry,exp,imax,attack,system_name)

    elif other != "":
        return "{}_{}_exp_{}_v{}_m_{}.csv".format(other, geometry, exp, version, system_name)

    else:
        return "result_{}_exp_{}_ndep_{}_att_{}_v{}_m_{}.csv".format(geometry, exp, imax, attack, version, system_name)


def get_line_number_with(node_damage_fraction, number_of_nodes):
    return numpy.ceil(node_damage_fraction*number_of_nodes)


def get_all_data_for(path, geometry, exp, imax, attack, systems, strategies_paths={}, legacy=False, debug=False,
                     recv_file_name=None):
    version = "average"
    lines = {}
    aux_line = []
    x_axis = []
    x_axis_done = False

    if recv_file_name:
        for strategy in strategies_paths.keys():
            lines[strategy] = {}
            for v in range(1, 11):
                file_name = recv_file_name.format(v)
                path = strategies_paths[strategy]
                file_path = os.path.join(path, file_name)
                with open(file_path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    line_count = 1
                    for row in csv_reader:
                        if line_count == 1:
                            line_count += 1
                            continue
                        if not x_axis_done:
                            x_axis.append(float(row[0]))
                        aux_line.append(float(row[1]))
                x_axis_done = True
                lines[strategy][v] = aux_line
                aux_line = []
            lines["x_axis"] = x_axis
    elif strategies_paths:
        system_name = systems
        for strategy in strategies_paths.keys():

            path = strategies_paths[strategy]
            file_name = generate_csv_file_name(geometry, exp, imax, attack, version, system_name)
            if legacy:
                file_name = "legacy_{}".format(file_name)
            if debug:
                file_name = "debug_{}".format(file_name)
            file_path = os.path.join(path, file_name)
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 1
                for row in csv_reader:
                    if line_count == 1:
                        line_count += 1
                        continue
                    if not x_axis_done:
                        x_axis.append(float(row[0]))
                    aux_line.append(float(row[1]))
            x_axis_done = True
            lines[strategy] = aux_line
            aux_line = []
        lines["x_axis"] = x_axis
    else:
        for system_name in systems:
            file_name = generate_csv_file_name(geometry, exp, imax, attack, version, system_name)
            if legacy:
                file_name = "legacy_{}".format(file_name)
            if debug:
                file_name = "debug_{}".format(file_name)
            file_path = os.path.join(path, file_name)
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 1
                for row in csv_reader:
                    if line_count == 1:
                        line_count += 1
                        continue
                    if not x_axis_done:
                        x_axis.append(float(row[0]))
                    aux_line.append(float(row[1]))
            x_axis_done = True
            lines[system_name] = aux_line
            aux_line = []
        lines["x_axis"] = x_axis
    return lines


def get_cost_of_added_edges(path, cost_function, physical_nodes_file, added_edges_file):
    # get nodes allocation
    nodes_allocations = []

    with open(physical_nodes_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            nodes_allocations.append((float(row[1]), float(row[2])))

    # get edges
    edges = []
    with open(os.path.join(path, added_edges_file)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            u = (row[0]).replace("p", "")
            v = (row[1]).replace("p", "")
            edges.append([int(u), int(v)])

    return cost_function(nodes_allocations, edges)


def get_edges_for_given_cost(path, cost_function, physical_nodes_file, added_edges_file, target_cost):
    # get nodes allocation
    nodes_allocations = []
    with open(physical_nodes_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            nodes_allocations.append((float(row[1]), float(row[2])))

    # get edges
    edges = []
    with open(os.path.join(path, added_edges_file)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            u = (row[0]).replace("p", "")
            v = (row[1]).replace("p", "")
            edges.append([int(u), int(v)])
    closest_i = 0
    delta_cost = 100000
    for i in range(1250, len(edges)):
        current_edges = edges[0:(i+1)]
        cost = cost_function(nodes_allocations, current_edges)

        if numpy.abs(cost - target_cost) < delta_cost:
            delta_cost = numpy.abs(cost - target_cost)
            closest_i = i
    return closest_i


def cost_by_length(nodes_allocations, edges):
    cost = 0

    for edge in edges:
        node_1 = numpy.array(nodes_allocations[edge[0]])
        node_2 = numpy.array(nodes_allocations[edge[1]])
        cost += numpy.linalg.norm(node_1 - node_2)

    return cost


def generate_latex_table_with(first_row, data, caption="", label=""):
    columns = len(first_row)
    table_format = "|"
    for k in range(columns):
        table_format += "l|"

    table_string = ""
    end_line = "\\\\ \\hline\n"

    table_string += "\\begin{table}[]\n"
    table_string += "\\begin{tabular}{" + table_format + "}\n"
    table_string += "\\hline\n"

    table_string += str(first_row[0])
    for i in range(1, len(first_row)):
        table_string += " & " + str(first_row[i])
    table_string += end_line

    for row in data:
        table_string += str(row[0])
        for j in range(1, len(row)):
            table_string += " & " + str(row[j])
        table_string += end_line

    table_string += "\\end{tabular}\n"
    table_string += "\\caption{" + caption + "}\n"
    table_string += "\\label{" + label + "}\n"
    table_string += "\\end{table}\n"
    return table_string


def get_degrees_from_file(path, strategy_path=None):
    if not path:
        return {}, 0
    base_graph = set_graph_from_csv(path)
    if strategy_path:
        graph = set_graph_from_csv(strategy_path, graph=base_graph)
    else:
        graph = base_graph

    degree = graph.degree()
    graph.vs['degree'] = degree
    max_degree = max(degree)
    node_degree = {}
    for node in graph.vs:
        node_degree[node['name']] = node['degree']

    return node_degree, max_degree


def get_average_degree_distribution_from_file(path, geometry, system_name, mode="sum-all", exp="2.5", nodes_list=[],
                                              v=None, strategy_path=None):

    if mode == "list-only":
        version_list = [v]
    else:
        version_list = range(1, 11)
    all_degree_distribution = []
    full_strategy_path = None
    # get degrees
    for version in version_list:
        full_path = path + generate_csv_file_name(geometry, exp, "", "", version, system_name, other="physic")
        if strategy_path:
            full_strategy_path = strategy_path + "candidates_{}_exp_2.5_v{}_m_{}.csv".format(geometry,version,system_name)

        node_degree, max_degree = get_degrees_from_file(full_path, strategy_path=full_strategy_path)

        degree_distribution = numpy.zeros(max_degree)

        for n in node_degree:
            if mode == "list-only" and n not in nodes_list:
                continue
            n_degree = node_degree[n]
            index = n_degree - 1
            degree_distribution[index] += 1
        all_degree_distribution.append(list(degree_distribution))

    for i in range(len(all_degree_distribution)):
        while len(all_degree_distribution[i]) < max_degree:
            all_degree_distribution[i].append(0)
    average_node_degrees = numpy.zeros(max_degree)

    average_by = 10.0
    if mode == "list-only":
        average_by = 1.0

    if mode == "sum-all" or mode == "list-only":
        for node_list in all_degree_distribution:
            for i in range(max_degree):
                average_node_degrees[i] += node_list[i]/average_by
    data = []
    for i in range(1, max_degree+1):
        data.append([i, numpy.round(average_node_degrees[i-1],1)])

    return data


def get_total_edges(geometry, exp, system_name, strategy=None):
    all_data = run_data()
    total_edges = []
    strategy_edges = 0
    link_path = all_data["model_links_path"]
    versions = all_data["versions"]
    if len(geometry) == 2:
        geometry = "{}x{}".format(geometry[0], geometry[1])
    for version in versions:
        if strategy:
            file_name = generate_csv_file_name(geometry, exp, "", "", version, system_name, other="candidates")
            file_path = "physical_data/{}_edges/".format(strategy.replace(" ", "_"))
            with open(file_path+file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                strategy_edges = lines_in_file(csv_reader)
        file_name = "physic_{}_exp_{}_v{}_m_{}.csv".format(geometry, all_data["exp"], version, system_name)
        file_path = os.path.join(link_path, file_name)
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            edges = strategy_edges + lines_in_file(csv_reader)
            total_edges.append(edges)
    return numpy.mean(total_edges), numpy.std(total_edges)


def generate_edges_table(models, geometries, exp=2.5):
    data = []
    first_row = ["width:length"]

    for geometry in geometries:
        row = []
        if geometry == "100x100" or geometry == (100, 100):
            row.append("(1:1)")
        elif geometry == "20x500" or geometry == (20, 500):
            row.append("(1:25)")
        for model in models:
            if len(first_row) < (1 + len(models)):
                first_row.append(model)
            mean, std = get_total_edges(geometry, exp, model)
            row.append("{} ({})".format(mean, std))
        data.append(row)
    return generate_latex_table_with(first_row, data, caption="", label="")


def get_data_from_localized_attack(model, geometry, strategy, ndep, version, r, legacy=False, lv=None):
    x_center = []
    y_center = []
    nodes_removed = []
    g_l = []
    radius = []
    all_data = run_data()
    paths = all_data["results_paths"]["LA"]

    if lv:
        file_name = "result_ppv3_lv{}_{}_exp_2.5_ndep_{}_att_localized_v{}_m_{}.csv".format(lv, geometry, ndep, version, model)
    else:
        file_name = "result_{}_exp_2.5_ndep_{}_att_localized_v{}_m_{}.csv".format(geometry, ndep, version, model)
        if legacy:
            file_name = "legacy_{}".format(file_name)

    file_path = os.path.join(paths[strategy], file_name)
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[4] == str(r):
                x_center.append(float(row[0]))
                y_center.append(float(row[1]))
                nodes_removed.append(parse_nodes_removed_from_localized_attack(row[2]))
                g_l.append(float(row[3]))
                radius.append(float(row[4]))
    return x_center, y_center, radius, {"nodes removed": nodes_removed, "g_l": g_l}


def get_data_from_seismic_attack(model, geometry, strategy, ndep, version, lv=1):
    x_center = []
    y_center = []
    nodes_removed = []
    magnitude = []
    depth = []
    event_type = []
    g_l = []
    radius = []
    paths = run_data()["seismic_result_paths"]

    file_name = "result_ppv3_lv{}_{}_exp_2.5_ndep_{}_att_seismic_v{}_m_{}.csv".format(lv, geometry, ndep, version, model)
    headline = True
    with open(os.path.join(paths[strategy], file_name)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if headline:
                headline = False
                continue
            x_center.append(float(row[0]))
            y_center.append(float(row[1]))
            g_l.append(float(row[2]))
            radius.append(float(row[3]))
            magnitude.append(float(row[4]))
            depth.append(float(row[5]))
            event_type.append(float(row[6]))
            nodes_removed.append(parse_nodes_removed_from_localized_attack(row[7]))

    return x_center, y_center, radius, {"nodes removed": nodes_removed, "g_l":g_l, "Mw": magnitude, "H": depth, "Feve": event_type}


def parse_nodes_removed_from_localized_attack(list_string):
    list_string = (list_string.replace("[", "")).replace("]", "")
    node_list = list_string.split(".")
    if node_list == ['']:
        node_list = []

    return node_list


def get_average_gl_for_localized_attacks(model, geometry, strategy, ndep, versions, r):
    g_l = []
    for version in versions:
        x, y, r, data = get_data_from_localized_attack(model, geometry, strategy, ndep, version, r)
        g_l += data["g_l"]
    return numpy.mean(g_l), numpy.std(g_l)


def create_average_damage_table_model_vs_radius(models, radius, ndep, geometry, version, strategy):
    first_row = ["radius/model"]
    data = []
    first_row_ready = False
    for r in radius:
        current_row = [str(r)]
        for model in models:
            if not first_row_ready:
                first_row.append(model)
            mean, std = get_average_gl_for_localized_attacks(model, geometry, strategy, ndep, version, r)
            current_row.append("{}, ({})".format(mean, std))
        if len(first_row) == (1 + len(models)):
            first_row_ready = True
        data.append(current_row)
    shape = ""
    if geometry == "100x100":
        shape = "(1:1)"
    elif geometry == "20x500":
        shape = "(1:25)"
    caption = "Average results for {} models with $I_max={}$. Strategy {}.".format(shape, ndep, strategy)

    return generate_latex_table_with(first_row, data, caption=caption, label="")


def get_localized_damage_distribution(start, end, bucket_number, model, geometry, strategy, ndep, r):
    g_l = []
    for version in range(1,11):
        x, y, r, data = get_data_from_localized_attack(model, geometry, strategy, ndep, version, r)
        g_l += data["g_l"]
    buckets = create_buckets(start, end, bucket_number, g_l)
    contents = []
    labels = []

    for key in buckets.keys():
        contents.append(buckets[key]["values"])
        labels.append(key)
    return contents, labels


def get_degree_distribution_from_subset(nodes_list, model, geometry, strategy, version, exp="2.5"):
    dict_st = {"random":"random", "degree":"strategy_1", "distance":"strategy_2"}
    base_data_path = "physical_data/{}_physic/".format(model)
    if strategy == "simple graphs":
        strategy_path = None
    else:
        strategy_path = "physical_data/{}_edges/".format(dict_st[strategy])
    average = get_average_degree_distribution_from_file(base_data_path, geometry, exp, model, mode="list-only",
                                                        nodes_list=nodes_list, v=version, strategy_path=strategy_path)
    return average


def get_degree_distribution_from_localized_attack(x_center, y_center, model, geometry, strategy, r, ndep=1, exp="2.5"):
    node_list = {}
    max_dist_len = 0
    for version in range(1, 11):
        nodes = find_removed_nodes_from_localized_attack(x_center, y_center, r, model, geometry, strategy, ndep, version)
        node_list[version] = {"node amount": len(nodes),
                              "node list": nodes,
                               "degree distribution": get_degree_distribution_from_subset(nodes, model, geometry, strategy, version)}

        if len(node_list[version]["degree distribution"]) > max_dist_len:
            max_dist_len = len(node_list[version]["degree distribution"])

    total_dist = numpy.zeros(max_dist_len)
    for i in range(max_dist_len):
        for version in range(1, 11):
            if i < len(node_list[version]["degree distribution"]):
                total_dist[i] += node_list[version]["degree distribution"][i][1]/10.0
    data = []
    for i in range(max_dist_len):
        data.append([(i+1),total_dist[i]])

    return data, node_list


def find_removed_nodes_from_localized_attack(target_x, target_y, target_r, model, geometry, strategy, ndep, version):
    node_list = []
    x, y, radius, data = get_data_from_localized_attack(model, geometry, strategy, ndep, version, target_r)
    for i in range(len(x)):
        if x[i] == target_x and y[i] == target_y and radius[i] == target_r:
            node_list.append(data["nodes removed"][i])
            break
    return node_list[0]


def create_buckets(start, end, bucket_number, values, degree=False):
    step = (end - start)/bucket_number

    groups = {}
    if not degree:
        for i in range(bucket_number):
            low_value = i * step + start
            high_value = (i + 1) * step + start
            groups["[{}, {}]".format(low_value, high_value)] = {"low": low_value, "high": high_value, "values": 0}

        for value in values:
            for key in groups.keys():
                low = groups[key]["low"]
                high = groups[key]["high"]
                if low < value <= high:
                    groups[key]["values"] += 1
                if low == 0 and value == 0:
                    groups[key]["values"] += 1

    else:
        max_degree = int(max(values))
        for i in range(1, (max_degree + 1)):
            groups[str(i)] = {"values": 0}
        for value in values:
            for key in groups.keys():
                if value == int(key):
                    groups[key]["values"] += 1
    return groups


def correlated_damage_vs_nodes_removed(model, geometry, strategy, ndep, r, v=None, legacy=False, lv=None, is_seismic=False):
    damage = []
    nodes_removed = []
    nodes_list = []
    versions = []
    full_data = {"x_center": [], "y_center": []}

    if v:
        version_list = [v]
    else:
        version_list = (run_data())["versions"]#range(1, 11)
    for version in version_list:
        if is_seismic:
            x, y, z, data = get_data_from_seismic_attack(model, geometry, strategy, ndep, version, lv=lv)
        else:
            x, y, z, data = get_data_from_localized_attack(model, geometry, strategy, ndep, version, r, legacy=legacy, lv=lv)

        g_l = data["g_l"]
        node_list = data["nodes removed"]

        for i in range(len(g_l)):
            damage.append((1 - g_l[i]))
            nodes_removed.append(len(node_list[i]))
            nodes_list.append(node_list[i])
            versions.append(version)
            for key in data.keys():
                if key not in full_data.keys():
                    full_data[key] = []
                full_data[key].append(data[key][i])
            full_data["x_center"].append(x[i])
            full_data["y_center"].append(y[i])
    return damage, nodes_removed, nodes_list, versions, full_data


def amount_of_providers_in_node_list(node_list, geometry, ndep):
    provider_list = physical_provider_list(ndep)
    return [x for x in node_list if x in provider_list]


def logic_provider_list(ndep):
    provider_list = []
    path_file = (run_data())["providers_paths"][ndep]
    with open(path_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == "physical":
                break
            if not row[0] == "logical":
                provider_list.append(row[0])

    return provider_list


def physical_provider_list(ndep):
    provider_list = []
    path_file = (run_data())["providers_paths"][ndep]
    seen_physical_marker = False
    with open(path_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if seen_physical_marker:
                provider_list.append(row[0])
            if row[0] == "physical":
                seen_physical_marker = True
    return provider_list


def get_degree_distribution_from_list(values):
    g = create_buckets(0, max(values), max(values), values, degree=True)
    return g


def get_interdegree_distribution_from_list(node_list, geometry, ndep):
    degrees = get_interdegree_from_list(node_list, geometry, ndep)
    values = degrees.values()
    return get_degree_distribution_from_list(values)


def get_interdegree_from_list(node_list, geometry, ndep):
    path_file = (run_data())["interlink_paths"][ndep]
    degree_list = numpy.zeros(len(node_list))
    with open(path_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] in node_list:
                index = node_list.index(row[0])
                degree_list[index] += 1
    degree_dict = {}
    for i in range(len(node_list)):
        degree_dict[node_list[i]] = degree_list[i]
    return degree_dict


def get_internodes_from_list(node_list, ndep):
    path_file = (run_data())["interlink_paths"][ndep]
    logic_nodes = {}
    with open(path_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] in node_list:
                if row[1] not in logic_nodes.keys():
                    logic_nodes[row[1]] = 1
                else:
                    logic_nodes[row[1]] += 1
    return logic_nodes


def get_logic_nodes_interlinks(ndep):
    path_file = (run_data())["interlink_paths"][ndep]
    logic_nodes = {}
    with open(path_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1] not in logic_nodes.keys():
                logic_nodes[row[1]] = 1
            else:
                logic_nodes[row[1]] += 1
    return logic_nodes


def get_failed_logic_nodes(target_list, ndep):
    failed_nodes = []
    logic_nodes_inter_links = get_logic_nodes_interlinks(ndep)
    for node in target_list.keys():
        if target_list[node] == logic_nodes_inter_links[node]:
            failed_nodes.append(node)
    return failed_nodes


def create_nx_graph(geometry, model, version, extra_edges=None):
    x = 0
    y = 1
    G = nx.Graph()
    nodes = []
    edges = []
    all_data = run_data()
    # load node names and positions
    if len(geometry) > 2:
        dimensions = geometry.split("x")
        space = (int(dimensions[x]), int(dimensions[y]))

    file_path = os.path.join(all_data["nodes_allocations"][space][int(version)])
    print(file_path)
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            nodes.append((row[0], {'pos': (float(row[1]), float(row[2]))}))
    G.add_nodes_from(nodes)
    
    # load edges

    file_path_name = "physic_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
    file_path_edges = os.path.join(all_data["model_links_path"], file_path_name)
    print(file_path_edges)
    with open(file_path_edges) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            node_u = row[0]#int(row[0].replace("p", ""))
            node_v = row[1]#int(row[1].replace("p", ""))
            edge = (node_u, node_v)
            edges.append(edge)
    if extra_edges:
        if extra_edges in ["degree", "random", "distance", "local_hubs"]:
            file_path_name = "candidates_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
            file_path_edges = os.path.join(all_data["extra_edges_path"][extra_edges], file_path_name)
        elif extra_edges in ["degree_aux", "distance_aux"]:
            file_path_name = "candidates_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
            file_path_edges = "../networks/physical_networks/extra_edges/{}/{}".format(extra_edges, file_path_name)
        else:
            file_path_edges = "../networks/physical_networks/extra_edges/candidates_{}.csv".format(extra_edges)
        print(file_path_edges)
        with open(file_path_edges) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                node_u = row[0]  # int(row[0].replace("p", ""))
                node_v = row[1]  # int(row[1].replace("p", ""))
                edge = (node_u, node_v)
                edges.append(edge)
    G.add_edges_from(edges)

    return G


def lines_in_file(file_descriptor):
    i = 0
    for row in file_descriptor:
        i += 1
    return i


def logic_node_betweenness(node_list, fname):
    file_path = "/Users/ivana/PycharmProjects/thesis_experiments/networks/logical_networks"#(run_data())["logic_network_path"]
    logic_graph = set_graph_from_csv(os.path.join(file_path, fname))

    node_list_indexes = []
    for i in range(len(node_list)):
        n = node_list[i]
        node_list_indexes.append(logic_graph.vs.find(name=n).index)

    all_bet = logic_graph.vs.betweenness()

    betwenness = []
    for i in range(len(node_list)):
        betwenness.append([node_list[i], all_bet[node_list_indexes[i]]])
    return betwenness


def logic_node_degree(node_list):
    file_path = (run_data())["logic_network_path"]
    logic_graph = set_graph_from_csv(file_path)
    node_list_indexes = []
    for i in range(len(node_list)):
        n = node_list[i]
        node_list_indexes.append(logic_graph.vs.find(name=n).index)

    all_bet = logic_graph.vs.degree()
    degree = []
    for i in range(len(node_list)):
        degree.append([node_list[i], all_bet[node_list_indexes[i]]])
    return degree


def gl_after_removal(node_list, ndep, geometry="20x500", other_providers=None):
    file_path = (run_data())["logic_network_path"]
    logic_graph = set_graph_from_csv(file_path)
    providers = logic_provider_list(ndep)
    new_logic_graph = get_nodes_lost_by_cc(logic_graph, node_list, providers, ret_graph=True)
        #attack_nodes(logic_graph, node_list, geometry, ndep, other_providers=other_providers)
    functional_nodes_in_logic_net = len([a for a in new_logic_graph.vs if new_logic_graph.degree(a.index) > 0])
    return (functional_nodes_in_logic_net * 1.0) / (300 * 1.0)


def logic_nodes_lost_after_removal(node_list, ndep, geometry="20x500"):
    file_path = (run_data())["logic_network_path"]
    logic_graph = set_graph_from_csv(file_path)
    return attack_nodes(logic_graph, node_list, geometry, ndep, ret="nodes")


def functional_physical_nodes_after_removal(node_list, model, version, ndep, geometry, strategy="simple graphs"):
    all_data = run_data()
    base_path = all_data["model_links_path"]
    base_file = "physic_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)

    base_physical_graph = set_graph_from_csv(os.path.join(base_path, base_file))
    if not strategy == "simple graphs":
        # add extra edges
        strategy_path = all_data["extra_edges_path"][strategy]
        strategy_file = "candidates_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
        file_path = os.path.join(strategy_path, strategy_file)
        graph = set_graph_from_csv(file_path, graph=base_physical_graph)
    else:
        graph = base_physical_graph
    providers = physical_provider_list(ndep)
    new_physical_graph = get_nodes_lost_by_cc(graph, node_list, providers, ret_graph=True)#attack_nodes(graph, node_list, geometry, ndep, mode="physical")

    functional_nodes_in_physical_graph = len([a for a in new_physical_graph.vs if new_physical_graph.degree(a.index) > 0])

    return (functional_nodes_in_physical_graph * 1.0) / (2000 * 1.0)


def physical_nodes_lost_after_removal(node_list, model, version, ndep, geometry, strategy="simple graphs"):
    all_data = run_data()
    base_path = all_data["model_links_path"]
    base_file = "physic_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
    base_physical_graph = set_graph_from_csv(os.path.join(base_path, base_file))
    if not strategy == "simple graphs":
        # add extra edges
        strategy_path = all_data["extra_edges_path"][strategy]
        strategy_file = "candidates_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
        file_path = os.path.join(strategy_path, strategy_file)
        graph = set_graph_from_csv(file_path, graph=base_physical_graph)
    else:
        graph = base_physical_graph
    providers = physical_provider_list(ndep)
    return get_nodes_lost_by_cc(graph, node_list, providers)
    #return attack_nodes(graph, node_list, geometry, ndep, mode="physical", ret="nodes")


def attack_nodes(graph, list_of_nodes_to_delete, geometry, ndep, mode="logic", ret="graph", other_providers=None):
    # remove nodes
    nodes_to_delete = [node for node in list_of_nodes_to_delete if node in graph.vs['name']]
    graph.delete_vertices(nodes_to_delete)

    if mode == "logic":
        if other_providers:
            providers = other_providers

        else:
            providers = logic_provider_list(ndep)
            providers.remove('logic')
            #print("attack_nodes(...): {}".format(providers))
    else:
        providers = physical_provider_list(ndep)
    alive_nodes = graph.vs['name']
    nodes_without_connection_to_provider = set(range(len(graph.vs)))
    for provider in providers:
        if provider not in alive_nodes:
            continue
        length_to_provider = graph.shortest_paths(provider)[0]
        zipped_list = zip(length_to_provider, range(len(graph.vs)))
        current_nodes_without_connection_to_provider = set([a[1] for a in zipped_list if a[0] == float('inf')])
        nodes_without_connection_to_provider = nodes_without_connection_to_provider.intersection(current_nodes_without_connection_to_provider)
    node_names = [graph.vs['name'][x] for x in nodes_without_connection_to_provider]
    graph.delete_vertices(nodes_without_connection_to_provider)
    if ret == "graph":
        return graph
    elif ret == "nodes":
        return node_names


def get_nodes_lost_by_cc(physical_graph, nodes_to_delete, providers, ret_graph=False):
    new_lost_nodes = []
    physical_graph_copy = physical_graph.copy()
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
    if ret_graph:
        physical_graph_copy.delete_vertices(new_lost_nodes)
        return physical_graph_copy
    else:
        return new_lost_nodes


def damage_LA_vs_RA(model, geometry, strategy, ndep, radius, legacy=False, lv=None):

    damage, nodes_removed, c, d, t = correlated_damage_vs_nodes_removed(model, geometry, strategy, ndep, radius,
                                                                        legacy=legacy, lv=lv)
    mean_damage = 1-numpy.mean(damage)
    mean_nodes_removed = numpy.ceil(numpy.mean(nodes_removed))

    path = (run_data())["average_results_path"][strategy]

    rnd_damage_data = data_at_x_percent_damage(mean_nodes_removed/2000, 2000, path, geometry, 2.5, "physical", model,
                                               legacy=legacy, lv=lv)
    if len(rnd_damage_data['x_axis']) == 1:
        index = 0
    else:
        index = (rnd_damage_data['x_axis']).index(int(ndep))
    if len(rnd_damage_data['y_axis']) < 1:
        print([model, geometry, strategy, ndep, radius, legacy])
        exit(10)
    rnd_damage = rnd_damage_data['y_axis'][index]

    return mean_nodes_removed, rnd_damage, mean_damage


def get_LA_RA_lineplot_info_for_damage_comparison(radius_list, model_list, strategy, geometry, ndep, legacy=False, lv=None):
    shape = ""
    if geometry == "20x500":
        shape = "(1:25)"
    elif geometry == "100x100":
        shape = "(1:1)"
    x = []
    lines = {}
    for model in model_list:
        lines["LA - {} {}".format(model, shape)] = []
        lines["RA - {} {}".format(model, shape)] = []
    for r in radius_list:
        for model in model_list:
            nodes_removed, ra_damage, la_damage = damage_LA_vs_RA(model, geometry, strategy, ndep, r, legacy=legacy, lv=lv)

            lines["RA - {} {}".format(model, shape)].append(numpy.round(ra_damage,5))
            lines["LA - {} {}".format(model, shape)].append(numpy.round(la_damage,5))
        x.append(r)

    return lines, x


def get_LA_RA_table_for_damage_comparison(radius_list, model_list, strategy, geometry, ndep, legacy=False):
    first_line = ["r", "nodes removed"]
    for model in model_list:
        first_line.append("{} LA".format(model))
        first_line.append("{} RA".format(model))
    data = []
    is_first = True
    for r in radius_list:
        current_data = []
        if is_first:
            current_data.append(str(r))
        for model in model_list:
            nodes_removed, ra_damage, la_damage = damage_LA_vs_RA(model, geometry, strategy, ndep, r, legacy=legacy)
            if is_first:
                current_data.append(int(nodes_removed))
                is_first = False
            current_data.append(numpy.round(la_damage,3))
            current_data.append(numpy.round(ra_damage,3))
        data.append(current_data)
        is_first = True
    a = generate_latex_table_with(first_line, data,caption="$G_L$ comparison of LA and RA", label="tab:LAvsRA")


def get_total_interlinks(dict):
    sum = 0
    for k in dict.keys():
        sum += dict[k]['values']*int(k)
    return sum

###############################
def aux_bet(failed_nodes):
    failed_nodes = list(failed_nodes)
    betweenness = logic_node_betweenness(failed_nodes)
    # average betweenness of removed logic nodes
    bet = []
    for b in betweenness:
        bet.append(b[1])
    if len(bet) > 0:
        return max(bet)/((300-1)*(300-2))
    else:
        return 0


def difference_on_logic_nodes_removed(node_list, geometry, ndep, v, model):
    # get logic nodes lost initialy because of the node_list_removal
    internode_list = get_internodes_from_list(node_list, ndep)
    failed_nodes = get_failed_logic_nodes(internode_list, ndep)
    a = logic_nodes_lost_after_removal(failed_nodes, ndep)


    # get nodes lost considering the extra physical nodes lost because providers
    p_nodes_no_prov = physical_nodes_lost_after_removal(node_list,model,v,ndep,geometry)
    all_p_nodes = node_list + p_nodes_no_prov
    internode_list = get_internodes_from_list(all_p_nodes, ndep)
    failed_nodes_2 = get_failed_logic_nodes(internode_list, ndep)

    l1 = failed_nodes + a
    l2 = failed_nodes_2
    inter = len([x for x in l2 if x in l1])
    return len(l1)+len(l2)-inter


def full_attack_nodes_new(interdependent_network, nodes_to_attack, find=[]):

    physical_network = interdependent_network.get_phys()
    phys_suppliers = interdependent_network.get_phys_providers()
    logic_network = interdependent_network.get_as()
    logic_suppliers = interdependent_network.get_as_providers()
    interlink_graph = interdependent_network.get_interlinks()

    logic_name_by_index = tl.get_name_by_index(logic_network)

    physical_roseta = tl.get_roseta_from_network(physical_network)
    logical_roseta = tl.get_roseta_from_network(logic_network)
    inner_inter_roseta = tl.get_roseta_from_network(interlink_graph)

    phys_name_by_index = tl.get_name_by_index(physical_network)

    intern_name_by_index, inter_roseta_phys, inter_roseta_logic = tl.parse_interlink_network(interlink_graph, phys_name_by_index, logic_name_by_index)

    n_phys = len(physical_network.vs)
    n_logic = len(logic_network.vs)
    iteration_results = []
    if len(find) > 0:
        is_find = tl.attack_nodes_test(phys_name_by_index, logic_name_by_index, intern_name_by_index,
                                                physical_network, phys_suppliers, inter_roseta_phys,
                                                inter_roseta_logic, nodes_to_attack, physical_roseta,
                                                logical_roseta, logic_network, logic_suppliers, interlink_graph,
                                                inner_inter_roseta, find=find)
        if is_find == True:
            return True
        else:
            return False

    #gl = (n_logic - len(logic_nodes_deleted)) / n_logic


def full_attack_nodes(logic_graph, physical_graph, inter_graph, physical_provider_list,
                      logic_provider_list,list_of_nodes_to_delete, find=[], verbose=False):
        current_graph_A = logic_graph
        current_graph_B = physical_graph
        current_interaction_graph = inter_graph
        while True:
            # if there are no more nodes to delete, i.e, the network has stabilized, then stop
            if len(list_of_nodes_to_delete) == 0:
                break
            # Delete the nodes to delete on each network, including the interactions network
            nodes_to_delete_in_A = [node for node in list_of_nodes_to_delete if node in current_graph_A.vs['name']]
            nodes_to_delete_in_B = [node for node in list_of_nodes_to_delete if node in current_graph_B.vs['name']]
            if verbose:
                print("current interlinks:")
                print(len(current_interaction_graph.es()))
                print("nodes removed:")
                print(nodes_to_delete_in_A)
            for f in find:
                if f in nodes_to_delete_in_A:
                    return True
            if verbose:
                print("bet {}".format(aux_bet(nodes_to_delete_in_A)))
                print(nodes_to_delete_in_B)
            current_graph_A.delete_vertices(nodes_to_delete_in_A)
            current_graph_B.delete_vertices(nodes_to_delete_in_B)

            current_interaction_graph.delete_vertices(
                [n for n in list_of_nodes_to_delete if n in current_interaction_graph.vs['name']])

            # Determine all nodes that fail because they don't have connection to a provider
            nodes_without_connection_to_provider_in_A = set(range(len(current_graph_A.vs)))
            alive_nodes_in_A = current_graph_A.vs['name']
            for provider_node in logic_provider_list:
                if provider_node not in alive_nodes_in_A:
                    continue
                length_to_provider_in_network_A = current_graph_A.shortest_paths(provider_node)[0]
                zipped_list_A = zip(length_to_provider_in_network_A, range(len(current_graph_A.vs)))
                current_nodes_without_connection_to_provider_in_A = \
                    set([a[1] for a in zipped_list_A if a[0] == float('inf')])
                nodes_without_connection_to_provider_in_A = \
                    nodes_without_connection_to_provider_in_A \
                        .intersection(current_nodes_without_connection_to_provider_in_A)

            nodes_without_connection_to_provider_in_B = set(range(len(current_graph_B.vs)))
            alive_nodes_in_B = current_graph_B.vs['name']
            for provider_node in physical_provider_list:
                if provider_node not in alive_nodes_in_B:
                    continue
                # print provider_node, "is alive"
                length_to_provider_in_network_B = current_graph_B.shortest_paths(provider_node)[0]
                zipped_list_B = zip(length_to_provider_in_network_B, range(len(current_graph_B.vs)))
                current_nodes_without_connection_to_provider_in_B = \
                    set([a[1] for a in zipped_list_B if a[0] == float('inf')])
                nodes_without_connection_to_provider_in_B = \
                    nodes_without_connection_to_provider_in_B \
                        .intersection(current_nodes_without_connection_to_provider_in_B)
            # save the names (unique identifier) of the nodes lost because can't access a provider
            names_of_nodes_lost_in_A = set(current_graph_A.vs(list(nodes_without_connection_to_provider_in_A))['name'])

            names_of_nodes_lost_in_B = set(current_graph_B.vs(list(nodes_without_connection_to_provider_in_B))['name'])

            # Delete all nodes that fail because they don't have connection to a provider on each network including
            # interactions network
            if verbose:
                print("nodes that lost connection to a provider caused by last removal:")
                print(names_of_nodes_lost_in_A)
            for f in find:
                if f in names_of_nodes_lost_in_A:
                    return True
            if verbose:
                print("bet {}".format(aux_bet(names_of_nodes_lost_in_A)))
                print(names_of_nodes_lost_in_B)
            current_graph_A.delete_vertices(nodes_without_connection_to_provider_in_A)
            current_graph_B.delete_vertices(nodes_without_connection_to_provider_in_B)
            nodes_to_delete = list(names_of_nodes_lost_in_A.union(names_of_nodes_lost_in_B))
            current_interaction_graph.delete_vertices(
                [n for n in nodes_to_delete if n in current_interaction_graph.vs['name']])

            # Get the nodes lost because they have lost all support from the other network
            zipped_list_interactions = zip(current_interaction_graph.degree(), current_interaction_graph.vs['name'])
            # Add them to the nodes to delete on the next iteration
            if verbose:
                print("interlinks after last removal: ")
                print(len(current_interaction_graph.es()))
            list_of_nodes_to_delete = [a[1] for a in zipped_list_interactions if a[0] < 1]

        if len(find) > 0:
            return False
        return current_graph_A


def gl_after_removal_full_attack(node_list, model, version, ndep, geometry, strategy="simple graphs", verbose=False):
    all_data = run_data()
    base_path = all_data["model_links_path"]
    base_file = "physic_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
    base_physical_graph = set_graph_from_csv(os.path.join(base_path, base_file))
    if not strategy == "simple graphs":
        # add extra edges
        strategy_path = all_data["extra_edges_path"][strategy]
        strategy_file = "candidates_{}_exp_2.5_v{}_m_{}.csv".format(geometry, version, model)
        file_path = os.path.join(strategy_path, strategy_file)
        physical_graph = set_graph_from_csv(file_path, graph=base_physical_graph)
    else:
        physical_graph = base_physical_graph
    file_path = all_data["logic_network_path"]
    logic_graph = set_graph_from_csv(file_path)

    inter_path = all_data["interlink_paths"][ndep]
    inter_graph = set_graph_from_csv(inter_path)

    logic_prov_list = logic_provider_list(ndep)

    physical_prov_list = physical_provider_list(ndep)

    new_logic_graph = full_attack_nodes(logic_graph, physical_graph, inter_graph, physical_prov_list, logic_prov_list,
                                        node_list, verbose=verbose)

    functional_nodes_in_logic_net = len([a for a in new_logic_graph.vs if new_logic_graph.degree(a.index) > 0])

    return (functional_nodes_in_logic_net * 1.0) / (300 * 1.0)


def is_removed_during_attack(find, node_list, model, version, ndep, geometry, strategy="simple graphs", lv=1):
    path = "/Users/ivana/PycharmProjects/thesis_experiments/networks/"
    exp = "2.5"
    ppv = 3
    geometry = geometry.split("x")
    x_coordinate = int(geometry[0])
    y_coordinate = int(geometry[1])
    logic_dir = os.path.join(path, "logical_networks")
    physical_dir = os.path.join(path, "physical_networks", "links")
    providers_dir = os.path.join(path, "providers")

    interlink_dir = os.path.join(path, "interdependencies", "provider_priority")
    providers_dir = os.path.join(providers_dir, "provider_priority")
    node_loc_dir = os.path.join(path, "physical_networks", "node_locations")

    interlink_title = csv_title_generator("dependence", "", "", "", ndep, 6, version=ppv)
    providers_title = csv_title_generator("providers", "", "", "", ndep, 6, version=ppv)

    logic_title = "logic_exp_{}_v{}.csv".format(exp, lv)

    nodes_loc_title = csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version)
    physic_title = csv_title_generator("physic", x_coordinate, y_coordinate, exp, version=version, model=model)
    logic_dir = os.path.join(logic_dir, logic_title)
    physical_dir = os.path.join(physical_dir, physic_title)
    interlink_dir = os.path.join(interlink_dir, interlink_title)
    providers_dir = os.path.join(providers_dir, providers_title)
    nodes_loc_dir = os.path.join(node_loc_dir, nodes_loc_title)

    network_system = interdependent_network_library.InterdependentGraph()
    network_system.create_from_csv(logic_dir, physical_dir, interlink_dir, nodes_loc_dir, providers_csv=providers_dir)

    if strategy != 'simple graphs':
        path = os.path.dirname(os.path.abspath(__file__))
        path = path.replace("/data_proc", "")
        start_title = "candidates"

        #if len(title_mod) > 0:
        #    start_title = "{}_{}".format(start_title, title_mod)
        title = csv_title_generator(start_title, x_coordinate, y_coordinate, exp, version=version, model=model)
        path = os.path.join(path, "networks", "physical_networks", "extra_edges", strategy, title)

        edges_to_add = interdependent_network_library.get_list_of_tuples_from_csv(path)
        network_system.add_edges_to_physical_network(edges_to_add)
        #print(" -- -> Added edges from: {}".format(path))
        sub_dir = strategy

    return full_attack_nodes_new(network_system, node_list, find=find)


def get_all_logical_nodes_lost_from_original_pnode_list(node_list, model, version, geometry, ndep, strategy):
    p_nodes_no_prov = physical_nodes_lost_after_removal(node_list, model, version, ndep, geometry, strategy=strategy)
    all_p_nodes = node_list + p_nodes_no_prov
    internode_list = get_internodes_from_list(all_p_nodes, ndep)
    failed_nodes_2 = get_failed_logic_nodes(internode_list, ndep)
    return failed_nodes_2


def read_scatter_plot_data(model, ndep, geometry, radius, strategy, legacy=False, lv=-1):
    strategy_n = strategy.replace(" ", "_")
    f_name = "scatter_plot_data_model_{}_ndep_{}_geometry_{}_radius_{}_st_{}.csv".format(model, ndep, geometry,
                                                                                          radius, strategy)
    if legacy:
        f_name = "legacy_{}".format(f_name)
    elif lv > 0:
        f_name = "lv{}_{}".format(lv, f_name)

    data = {"betweenness": [],
            "isl50": [],
            "logic damage": [],
            "physic damage": []}
    file_path = os.path.join((run_data())["scatter_plot_path"][strategy], f_name)

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] == "betweenness":
                continue
            data["betweenness"].append(float(row[0]))
            if row[1] == "True":
                data["isl50"].append(True)
            else:
                data["isl50"].append(False)
            data["logic damage"].append(float(row[2]))
            data["physic damage"].append(float(row[3]))

    return data


def number_of_connected_components(ndep, node_list=['l50']):
    file_path = "data/logic_20x500_exp_2.5_v1.csv"
    providers = logic_provider_list(ndep)[1::]
    if 'l50' in providers:
        print("ndep {} has l50 as provider".format(ndep))
        providers.remove('l50')
    logic_graph = set_graph_from_csv(file_path)

    logic_graph.delete_vertices(node_list)

    name_dict = {}
    i = 0
    for v in logic_graph.vs:
        vname = v['name']
        name_dict[vname] = i
        i += 1

    comp = logic_graph.clusters()

    for i in range(len(comp)):
        c = comp[i]
        for p in providers:
            pi = name_dict[p]
            if pi in c:
                print("Provider {} in component {}".format(p,i))


def run_data():
    legacy = False
    spaces = [(20, 500), (100, 100)]
    exp = "2.5"
    attack = "physical"
    versions = range(1, 11)

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nodes_allocations = {}

    nodes_allocations_path = os.path.join(base_path, "networks", "physical_networks", "node_locations")
    # create dict with all node allocations
    for space in spaces:
        nodes_allocations[space] = {}
        for version in versions:
            node_loc_title = os.path.join(nodes_allocations_path,
                                          csv_title_generator("nodes", space[0], space[1], "2.5", version=version))
            nodes_allocations[space][version] = node_loc_title

    extra_edges_path = {"random": os.path.join(base_path, "networks", "physical_networks", "extra_edges", "random"),
                        #"degree": os.path.join(base_path, "networks", "physical_networks", "extra_edges", "degree"),
                        #"distance": os.path.join(base_path, "networks", "physical_networks", "extra_edges", "distance"),
                        "local_hubs": os.path.join(base_path, "networks", "physical_networks", "extra_edges",
                                                   "local_hubs"),
                        "distance_aux": os.path.join(base_path, "networks", "physical_networks", "extra_edges",
                                                     "distance_aux"),
                        "degree_aux": os.path.join(base_path, "networks", "physical_networks", "extra_edges",
                                                   "degree_aux")}

    file_space_names = {(20, 500): "20x500", (100, 100): "100x100"}
    figure_space_names = {(20, 500): "(1:25)", (100, 100): "(1:1)"}

    results_path_RA = {"random": os.path.join(base_path, "test_results", "random", "physical_random_attacks"),
                       #"degree": os.path.join(base_path, "test_results", "degree", "physical_random_attacks"),
                       "degree_aux": os.path.join(base_path, "test_results", "degree_aux", "physical_random_attacks"),
                       "distance": os.path.join(base_path, "test_results", "distance", "physical_random_attacks"),
                       "distance_aux": os.path.join(base_path, "test_results", "distance_aux", "physical_random_attacks"),
                       "simple graphs": os.path.join(base_path, "test_results", "simple_graphs", "physical_random_attacks"),
                       "local_hubs": os.path.join(base_path, "test_results", "local_hubs", "physical_random_attacks"),
                       "random_distance": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "distance"),
                       "random_local_hubs": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "local_hubs"),
                       "random_cap1.0": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "cap1.0"),
                       "random_cap0.75": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "cap0.75"),
                       "random_cap0.25": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "cap0.25"),
                       "random_cap0.5": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "cap0.5"),
                       "random_cap0.15": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "cap0.15"),
                       "random_cap0.05": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "cap0.05"),
                       "random_cap0.01": os.path.join(base_path, "test_results", "random", "physical_random_attacks", "cap0.01")}
    results_path_LA = {"random": os.path.join(base_path, "test_results", "random", "localized_attacks"),
                       #"degree": os.path.join(base_path, "test_results", "degree", "localized_attacks"),
                       "degree_aux": os.path.join(base_path, "test_results", "degree_aux", "localized_attacks"),
                       "distance": os.path.join(base_path, "test_results", "distance", "localized_attacks"),
                       "distance_aux": os.path.join(base_path, "test_results", "distance_aux", "localized_attacks"),
                       "simple graphs": os.path.join(base_path, "test_results", "simple_graphs", "localized_attacks"),
                       "local_hubs": os.path.join(base_path, "test_results", "local_hubs", "localized_attacks")
                       }
    results_paths = {"LA": results_path_LA,
                     "RA": results_path_RA}

    seismic_result_paths = {"simple graphs": os.path.join(base_path, "test_results", "seismic", "simple_graphs",),
                            "distance_aux": os.path.join(base_path, "test_results", "seismic", "distance_aux"),
                            "degree_aux": os.path.join(base_path, "test_results", "seismic", "degree_aux"),
                            "local_hubs": os.path.join(base_path, "test_results", "seismic", "local_hubs"),
                            "random": os.path.join(base_path, "test_results", "seismic", "random")}

    average_results_path = {"random": os.path.join(base_path, "test_results", "average_results", "random"),
                            #"degree": os.path.join(base_path, "test_results", "average_results", "degree"),
                            "degree_aux": os.path.join(base_path, "test_results", "average_results", "degree_aux"),
                            "distance_aux": os.path.join(base_path, "test_results", "average_results", "distance_aux"),
                            "local_hubs": os.path.join(base_path, "test_results", "average_results", "local_hubs"),
                            #"distance": os.path.join(base_path, "test_results", "average_results", "distance"),
                            "simple graphs": os.path.join(base_path, "test_results", "average_results", "simple_graphs"),
                            "random_distance": os.path.join(base_path, "test_results", "average_results", "random_distance"),
                            "random_local_hubs": os.path.join(base_path, "test_results", "average_results", "random_local_hubs"),
                            "random_cap0.75": os.path.join(base_path, "test_results", "average_results", "random_cap0.75"),
                            "random_cap1.0": os.path.join(base_path, "test_results", "average_results", "random_cap1.0"),
                            "random_cap0.25": os.path.join(base_path, "test_results", "average_results", "random_cap0.25"),
                            "random_cap0.5": os.path.join(base_path, "test_results", "average_results", "random_cap0.5"),
                            "random_cap0.15": os.path.join(base_path, "test_results", "average_results", "random_cap0.15"),
                            "random_cap0.05": os.path.join(base_path, "test_results", "average_results", "random_cap0.05"),
                            "random_cap0.01": os.path.join(base_path, "test_results", "average_results", "random_cap0.01")
                            }

    scatter_plot_path = {"random": os.path.join(base_path, "test_results", "scatter_plots", "random"),
                         #"degree": os.path.join(base_path, "test_results", "scatter_plots", "degree"),
                         "degree_aux": os.path.join(base_path, "test_results", "scatter_plots", "degree_aux"),
                         "local_hubs": os.path.join(base_path, "test_results", "scatter_plots", "local_hubs"),
                         "distance_aux": os.path.join(base_path, "test_results", "scatter_plots", "distance_aux"),
                         "distance": os.path.join(base_path, "test_results", "scatter_plots", "distance"),
                         "simple graphs": os.path.join(base_path, "test_results", "scatter_plots", "simple_graphs")}

    models = ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]
    model_link_path = os.path.join(base_path, "networks", "physical_networks", "links")

    logic_network_path = os.path.join(base_path, "networks", "logical_networks", "legacy_logic_20x500_exp_2.5_v1.csv")

    interlink_types = {"provider_priority": "pp", "full_random": "fr", "semi_random": "sr"}

    strategies = ["simple graphs", "random",
                  #"degree",
                  "distance", "distance_aux", "degree_aux"]

    interlink_paths = {}
    for ndep in get_imax_tested():
        file_name = "dependence_ndep_{}_lprovnum_6_v3.csv".format(ndep)
        if legacy:
            file_name = "dependence_20x500_exp_2.5_ndep_{}_lprovnum_6_v1.csv".format(ndep)
            file_name = "legacy_{}".format(file_name)
        interlink_paths[ndep] = os.path.join(base_path, "networks", "interdependencies", "provider_priority", file_name)
    providers_paths = {}
    for ndep in get_imax_tested():
        file_name = "providers_ndep_{}_lprovnum_6_v3.csv".format(ndep)
        if legacy:
            file_name = "providers_20x500_exp_2.5_ndep_{}_lprovnum_6_v1.csv".format(ndep)
            file_name = "legacy_{}".format(file_name)
        providers_paths[ndep] = os.path.join(base_path, "networks", "providers", "provider_priority", file_name)

    strategies_used_names = {"distance_aux": "Distance",
                             "degree_aux": "Degree",
                             "local_hubs": "Local hubs",
                             "random": "Random",
                             "0.01": "$\\rho($distance$)$",
                             "0.05": "$\\rho($local hubs$)$",
                             "0.25": "$0.25\\times\\rho_{rand}$",
                             "0.5": "$0.5\\times\\rho_{rand}$",
                             "0.75": "$0.75\\times\\rho_{rand}$"}

    all_info_dict = {"geometry": spaces,
                     "versions": versions,
                     "exp": exp,
                     "attack": attack,
                     "nodes_allocations": nodes_allocations,
                     "extra_edges_path": extra_edges_path,
                     "models": models,
                     "model_links_path": model_link_path,
                     "root_path": base_path,
                     "strategies": strategies,
                     "results_paths": results_paths,
                     "average_results_path": average_results_path,
                     "scatter_plot_path": scatter_plot_path,
                     "logic_network_path": logic_network_path,
                     "interlink_paths": interlink_paths,
                     "providers_paths": providers_paths,
                     "interlink_types": interlink_types,
                     "file_space_names": file_space_names,
                     "figure_space_names": figure_space_names,
                     "seismic_result_paths": seismic_result_paths,
                     "strategies_used_names": strategies_used_names}
    return all_info_dict


def tuple_to_gname(tuple):
    return "{}x{}".format(tuple[0], tuple[1])


def find_bridge_nodes(logic_file_path, supplier_path, debug=False, get_all_nodes=False):
    # bridge nodes data
    bridge_nodes_data = {}
    # load providers
    logic_providers = []
    with open(supplier_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            if row[0] == "logic":
                continue
            if row[0] == "physical":
                break
            logic_providers.append(row[0])
    # load logic network from file
    logic_network = set_graph_from_csv(logic_file_path)
    logic_node_names = ['l{}'.format(i) for i in range(300)]

    for node in logic_node_names:
        clusters_without_providers = []
        clusters_with_providers = []

        net_copy = logic_network.copy()
        net_copy.delete_vertices([node])
        #net_copy.delete_vertices(['l52','l294'])
        clusters = net_copy.clusters()
        for c in clusters:
            cluster_ready = False
            name_c = net_copy.vs[c]['name']
            for provider in logic_providers:
                if provider in name_c:
                    clusters_with_providers.append(name_c)
                    cluster_ready = True
                    break
            if cluster_ready:
                continue
            else:
                clusters_without_providers.append(name_c)
        if len(clusters_without_providers) > 0 or get_all_nodes:
            bridge_nodes_data[node] = {}
            if debug:
                print("Removing {}".format(node))
                print(" - Is provider: {}".format(node in logic_providers))
                print(" There are clusters with no provider access")
            i = 1
            j = 0
            bridge_nodes_data[node]["nodes_lost"] = 0
            for c in clusters_without_providers:
                bridge_nodes_data[node]["nodes_lost"] += len(c)
                if len(c) > 1:
                    if debug:
                        print(" -{}- Lost cluster of size = {}".format(i, len(c)))
                    i += 1
                else:
                    j += 1
            #print(bridge_nodes_data[node]["nodes_lost"])
            #exit(99)
            if j > 0 and debug:
                print(" -- Lost {} clusters of size = 1".format(j))

            if debug:
                print("There are {} clusters with providers".format(len(clusters_with_providers)))
            bridge_nodes_data[node]["functional_clusters"] = len(clusters_with_providers)
            bridge_nodes_data[node]["is_provider"] = node in logic_providers
        elif len(clusters_with_providers) > 1 and debug:
            print("Removing {}".format(node))
            print(" - Is provider: {}".format(node in logic_providers))
            print(" +++ There are {} clusters with providers".format(len(clusters_with_providers)))
    return bridge_nodes_data


def get_interlinks_for_logic_nodes(interlinks_path, mode="number"):
    interlinks_per_node = {}
    logic_node_names = ['l{}'.format(i) for i in range(300)]
    for node in logic_node_names:
        if mode == "number":
            interlinks_per_node[node] = 0
        elif mode == "nodes":
            interlinks_per_node[node] = []
    with open(interlinks_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            physical_node = row[0]
            logic_node = row[1]
            # physical_node = row[0]
            if mode == "number":
                interlinks_per_node[logic_node] += 1
            elif mode == "nodes":
                interlinks_per_node[logic_node].append(physical_node)
    return interlinks_per_node


def add_interlinks_to_bridge_nodes(ndep, logic_file_path, supplier_path, interlinks_path):
    bridge_nodes_data = find_bridge_nodes(logic_file_path, supplier_path)
    interlinks_per_node = get_interlinks_for_logic_nodes(interlinks_path, mode="nodes")
    physical_node_names = ["p{}".format(i) for i in range(2000)]
    extra_interlinks = []
    for logical_node in bridge_nodes_data.keys():
        inv_gl = bridge_nodes_data[logical_node]["nodes_lost"] / 300.0
        number_of_interlinks = len(interlinks_per_node[logical_node])
        if inv_gl > 0.1 and number_of_interlinks < ndep:
            interlinks_sample = physical_node_names.copy()
            for n in interlinks_per_node[logical_node]:
                interlinks_sample.remove(n)
            interlinks_to_add = ndep - number_of_interlinks
            links_to_add = random.sample(interlinks_sample, interlinks_to_add)
            for physical_node in links_to_add:
                extra_interlinks.append((physical_node, logical_node))
    return extra_interlinks




