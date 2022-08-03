import data_proc.data_processing as dp
import os
import matplotlib.pyplot as plt
import numpy as np
from data_proc.plotting import n_line_plot


def plot_bridge_nodes(bridge_nodes_data, interlinks=None, title="", use_x="interlinks", use_y="inv_GL"):
    inv_gls = []
    functional_clusters = []
    size = 10
    colors = []
    number_of_interlinks = []
    number_of_links = []
    max_inv_gl_node = ""
    interlinks_per_node = interlinks
    max_inv_gl = 0
    print("number of bridge nodes: {}".format(len(bridge_nodes_data.keys())))
    for node in bridge_nodes_data.keys():
        if interlinks_per_node and use_x == "interlinks":
            number_of_interlinks.append(interlinks_per_node[node])
        elif use_x == "links":
            number_of_links.append(bridge_nodes_data[node]["number_of_neighbors"]/300.0)

        if use_y == "inv_GL_vs_degree" and use_x == "links":
            inv_gl = bridge_nodes_data[node]["nodes_lost"] - bridge_nodes_data[node]["number_of_neighbors"]
        else:
            inv_gl = bridge_nodes_data[node]["nodes_lost"] / 300.0
        if inv_gl > max_inv_gl:
            max_inv_gl = inv_gl
            max_inv_gl_node = node

        func_clusters = bridge_nodes_data[node]["functional_clusters"]

        inv_gls.append(inv_gl)
        functional_clusters.append(func_clusters)
        if bridge_nodes_data[node]["is_provider"]:
            colors.append('#f03b20')
        else:
            colors.append('#252525')
        if inv_gl > 0.05 and interlinks_per_node:
            print("node {} = {}".format(node, inv_gl))
            pass
            #print(" -> {} has {} interlinks : {}".format(node, interlinks_per_node[node], inv_gl))
    fig, ax = plt.subplots()
    if interlinks_per_node and use_x == "interlinks":
        x_axis = number_of_interlinks
        plt.xlabel('# interlinks', fontsize=15)
    elif use_x == "links":
        x_axis = number_of_links
        plt.xlabel('# links', fontsize=15)
    else:
        x_axis = functional_clusters
        plt.xlabel('# funct. clusters', fontsize=15)
    if interlinks_per_node:
        pass
        #print(" -- Max (1-gl) = {} has {} interlinks\n".format(max(inv_gls), interlinks_per_node[max_inv_gl_node]))
    bridge_nodes_range = [min(inv_gls), max(inv_gls)]
    #print(" -- Bridge node (1-gl) range = ({},{})\n".format(min(inv_gls), max(inv_gls)))
    ax.scatter(x_axis, inv_gls, s=[x * size for x in np.ones(len(x_axis))], alpha=1, c=colors,
               label="bridge nodes", edgecolor='black', linewidth=0.2)
    #ax.legend(loc='upper left')
    plt.title(title)
    if use_y == "inv_GL_vs_degree" and use_x == "links":
        plt.ylabel(r'nodes_lost -  degree$', fontsize=18)
    else:
        plt.ylabel(r'1-$G_{L}$', fontsize=18)

    plt.show()
    return bridge_nodes_range


def plot_bridge_nodes_danziger_rev(title="", mode="degree_damage", save_figure=False):
    bn_data_list = []
    for ndep in range(1, 11):

        for lv in range(1, 11):
            # en general los bridge nodes no solo sacan a sus vecinos pero sacan menos o más. PERO y el número de clusters?
            # en cualquier caso si tiene que ver con el tema de ser hubs, pero hasta qué punto?

            bn_data = get_bridge_node_data_using_previous_results(ndep=ndep, lv=lv)
            bn_data_list.append(bn_data)

    bridge_nodes_data = bn_data_list
    size = 25
    x_axis = []
    y_axis = []

    fig, ax = plt.subplots()

    if mode == "degree_damage":
        plt.ylabel('Bridge node degree', fontsize=15)
        plt.xlabel(r'1-$G_{L}$', fontsize=18)

        fig_name = 'damage_degree.png'
        fig_path = '../figures/cap4/{}'.format(fig_name)
        print(fig_path)

        # los bridge nodes son una lista de diccionarios
        for bn_dict in bridge_nodes_data:
            for node in bn_dict.keys():
                y_axis.append(bn_dict[node]["degree"])
                x_axis.append(bn_dict[node]["nodes_lost"] / 300.0)
    else:
        plt.xlabel(r'1-$G_{L}$', fontsize=18)
        plt.ylabel(r'$NC_{>1}$', fontsize=18)

        fig_name = 'damage_delta.png'
        fig_path = '../figures/cap4/{}'.format(fig_name)
        print(fig_path)

        for bn_dict in bridge_nodes_data:
            for node in bn_dict.keys():

                biggest_cluster_size = max([len(x) for x in bn_dict[node]['non_functional_clusters']])
                sizes_array = []
                for i in range(biggest_cluster_size):
                    sizes_array.append(0)
                for cluster in bn_dict[node]['non_functional_clusters']:
                    cluster_size = len(cluster)
                    sizes_array[cluster_size - 1] += 1

                x_axis.append(bn_dict[node]["nodes_lost"] / 300.0)
                y_axis.append((bn_dict[node]["nodes_lost"] - sizes_array[0]) / bn_dict[node]["nodes_lost"] * 1.0)

    ax.scatter(x_axis, y_axis, s=[x * size for x in np.ones(len(x_axis))], alpha=1, label="bridge nodes", color='#fa3983', edgecolor='black', linewidth=0.5)
    #ax.legend(loc='upper left')
    plt.title(title)

    if save_figure:
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', pad_inches=0.002)

    plt.show()


def histogram_for_bridge_nodes(nodes_data_list, personalized_buckets):
    buckets = []
    buckets_providers = []
    hist_providers =[]
    for i in range(300):
        buckets.append(0)
        buckets_providers.append(0)
    for nodes_data in nodes_data_list:
        for node in nodes_data.keys():
            nodes_lost = int(nodes_data[node]["nodes_lost"])
            buckets[nodes_lost] += 1
            if nodes_data[node]["is_provider"]:
                buckets_providers[nodes_lost] += 1

    final_histogram = []
    for b in personalized_buckets:
        sum = 0
        sum_prov = 0
        for i in range(b[0], b[1]+1):
            sum += buckets[i]
            sum_prov += buckets_providers[i]
        final_histogram.append(sum)
        hist_providers.append(sum_prov)

    return final_histogram, hist_providers

lv = 10
ppv = 3


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logic_network_path = os.path.join(base_path, "networks", "logical_networks", "legacy_logic_20x500_exp_2.5_v1.csv")
file_name = "legacy_providers_20x500_exp_2.5_ndep_{}_lprovnum_6_v1.csv".format(3)
providers_path = os.path.join(base_path, "networks", "providers", file_name)
file_name2 = "legacy_dependence_20x500_exp_2.5_ndep_{}_lprovnum_6_v1.csv".format(3)
interlinks_path = os.path.join(base_path, "networks", "interdependencies", "full_random", file_name2)
#interlinks_per_node = dp.get_interlinks_for_logic_nodes(interlinks_path)

#bridge_nodes_data = dp.find_bridge_nodes(logic_network_path, providers_path)
#plot_bridge_nodes(bridge_nodes_data, interlinks=interlinks_per_node, title="Legacy ndep 3")


def get_bridge_node_data_using_previous_results(ndep,lv=1):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    ppv = 3
    # if i > 0:
    #    ppv = 1
    logic_file_name = "logic_exp_2.5_v{}.csv".format(lv)

    logic_network_path = os.path.join(base_path, "networks", "logical_networks", logic_file_name)

    provider_file_name = "providers_ndep_{}_lprovnum_6_v{}.csv".format(ndep, ppv)
    providers_path = os.path.join(base_path, "networks", "providers", "provider_priority", provider_file_name)

    bridge_nodes_data = dp.find_bridge_nodes(logic_network_path, providers_path)

    return bridge_nodes_data


def damage_versus_links(bridge_node_data, title, use_y="inv_GL"):
    bridge_nodes_range_gl = plot_bridge_nodes(bridge_node_data, interlinks=None, title=title, use_x="links", use_y=use_y)


def bn_data_danziger_analysis():
    count_deltaloss_g_0 = 0
    count_deltaloss_l_0 = 0

    count_higher_damage = 0
    count_lower_damage = 0

    bn_data_list = []
    for ndep in range(1,11):

        print("NDEP: {} +++-------------------------------------".format(ndep))
        for lv in range(1,11):
            # en general los bridge nodes no solo sacan a sus vecinos pero sacan menos o más. PERO y el número de clusters?
            # en cualquier caso si tiene que ver con el tema de ser hubs, pero hasta qué punto?

            bn_data = get_bridge_node_data_using_previous_results(ndep=ndep, lv=lv)
            bn_data_list.append(bn_data)
            #damage_versus_links(bn_data, "damage vs degree (ndep = 3)", use_y="inv_GL_vs_degree")

            print("-------------------------------------")
            for node in bn_data.keys():
                if 1 >= bn_data[node]["nodes_lost"]/300.0 >= 0.1:
                    count_higher_damage += 1
                    # order non-functional clusters (NFC) by size
                    biggest_cluster_size = max([len(x) for x in bn_data[node]['non_functional_clusters']])
                    sizes_array=[]
                    for i in range(biggest_cluster_size):
                        sizes_array.append(0)
                    for cluster in bn_data[node]['non_functional_clusters']:
                        cluster_size = len(cluster)
                        sizes_array[cluster_size-1] += 1
                    ## readable sizes_array
                    read_size_array = ""
                    for i in range(len(sizes_array)):
                        if sizes_array[i] > 0:
                            add_str = "- size {}: {} ".format(i+1, sizes_array[i])
                            read_size_array += add_str
                    read_size_array += "-"

                    ## print data
                    delta_loss = (bn_data[node]["nodes_lost"]-sizes_array[0])/300.0
                    delta_loss_over_total_loss = (bn_data[node]["nodes_lost"]-sizes_array[0])*1.0/bn_data[node]["nodes_lost"]

                    if delta_loss > 0:
                        count_deltaloss_g_0 += 1
                        print("A: ",delta_loss)
                        print("B: ", delta_loss_over_total_loss)
                        print("BN {} - Degree: {} - Nodes lost: {} - # NFC: {} - cluster with sizes: {}".format(node,bn_data[node]["degree"], bn_data[node]["nodes_lost"],
                                                                                                                    len(bn_data[node]['non_functional_clusters']),
                                                                                                                    read_size_array))
                    else:
                        count_deltaloss_l_0 += 1
                else:
                    count_lower_damage += 1

            print("+++-------------------------------------")

            #bn_data = get_bridge_node_data_using_previous_results(ndep=8, lv=lv)
            #damage_versus_links(bn_data, "damage vs degree (ndep = 8)", use_y="inv_GL_vs_degree")
    print("only lost size 1 clusters:", count_deltaloss_l_0, "rest:", count_deltaloss_g_0, "-> %", count_deltaloss_g_0/(count_deltaloss_g_0 + count_deltaloss_l_0))
    print("higher damage %: {}, lower damage %: {}".format(count_higher_damage/(count_higher_damage + count_lower_damage), count_lower_damage/(count_higher_damage + count_lower_damage)))
#plot_bridge_nodes_danziger_rev(title="")
#plot_bridge_nodes_danziger_rev(title="", mode="delta")


def get_partial_data():
    ndep = 3
    all_nodes_list = []
    for lv in [1]:
        i = 0
        ppv = 3
        all_bridge_node_ranges = {"min": 1, "max": 0}
        for ndep in list(range(1, 11)):
            #if i > 0:
            #    ppv = 1
            logic_file_name = "logic_exp_2.5_v{}.csv".format(lv)

            logic_network_path = os.path.join(base_path, "networks", "logical_networks", logic_file_name)

            provider_file_name = "providers_ndep_{}_lprovnum_6_v{}.csv".format(ndep, ppv)
            providers_path = os.path.join(base_path, "networks", "providers", "provider_priority", provider_file_name)

            interlinks_file_name = "dependence_ndep_{}_lprovnum_6_v{}.csv".format(ndep, ppv)
            interlinks_path = os.path.join(base_path, "networks", "interdependencies", "provider_priority",
                                           interlinks_file_name)
            interlinks_per_node3 = dp.get_interlinks_for_logic_nodes(interlinks_path)

            bridge_nodes_data = dp.find_bridge_nodes(logic_network_path, providers_path)
            print(bridge_nodes_data['l50'])
            #print("\nndep {}, lv {}: total bridge nodes = {}, ppv {}".format(ndep, lv, len(bridge_nodes_data.keys()), ppv))

            links = dp.add_interlinks_to_bridge_nodes(ndep, logic_network_path, providers_path, interlinks_path)
            links = ""
            print("({}, {}, {}): {},".format(ppv, ndep, lv, links))
            i += 1
            bridge_nodes_range_gl = plot_bridge_nodes(bridge_nodes_data, interlinks=interlinks_per_node3,
                              title="ndep {}, lv {}, ppv {}".format(ndep, lv, ppv))
            all_bridge_node_ranges["min"] = min(all_bridge_node_ranges["min"], bridge_nodes_range_gl[0])
            all_bridge_node_ranges["max"] = max(all_bridge_node_ranges["max"], bridge_nodes_range_gl[1])
            all_nodes = dp.find_bridge_nodes(logic_network_path, providers_path, get_all_nodes=True)
            all_nodes_list.append(all_nodes)
        print("Range for q={}: ({},{})".format(lv, np.round(all_bridge_node_ranges["min"], 3), np.round(all_bridge_node_ranges["max"], 3)))


def make_table_with_buckets(all_nodes_list):
    p_buck = [[0, 0], [1, 2], [3, 4], [5, 14], [15, 29], [30, 59], [60, 89], [90, 119], [120, 149], [150, 179], [180, 209], [210, 239], [240, 269], [270, 299]]

    hist, prov_h = histogram_for_bridge_nodes(all_nodes_list, p_buck)

    print("\\begin{table}[]")
    print("\\begin{tabular}{|l|l|l|}")
    print("\\hline")
    print("$N_L^f$     & \\% nodes & \\% of providers \\\\ \\hline")
    print("1           & {}      & {}            \\\\ \\hline".format(np.round((hist[0]/30000)*100, 2), np.round((prov_h[0]/30000)*100, 3)))

    for i in range(1, len(hist)):
        line_1 = "({},{}]           & {}      & {}            \\\\ \\hline".format(p_buck[i][0], p_buck[i][1] + 1, np.round((hist[i]/30000)*100, 2), np.round((prov_h[i]/max(1, 30000))*100, 3))
        print(line_1)
    print("\\end{tabular}")
    print("\\end{table}")


def table_with_bn_gl_value_ranges_for_all_imax():

    print("\\begin{table}[]")
    print("\\centering")
    print("\\begin{tabular}{|l|l|}")
    print("\\hline")
    print("$q$ & $G_L$ range   \\\\ \\hline")
    for lv in range(1, 11):
        line = "{}   &".format(lv) + " {} \\\\ \\hline"

        all_min = []
        all_max = []
        for ndep in range(1, 11):

            # en general los bridge nodes no solo sacan a sus vecinos pero sacan menos o más. PERO y el número de clusters?
            # en cualquier caso si tiene que ver con el tema de ser hubs, pero hasta qué punto?

            bn_data = get_bridge_node_data_using_previous_results(ndep=ndep, lv=lv)
            # make a GL range
            min_gl = 10
            max_gl = 0
            for key in bn_data.keys():
                current_gl = np.round(1 - (bn_data[key]['nodes_lost'] / 300), 3)
                if current_gl < min_gl:
                    min_gl = current_gl
                if current_gl > max_gl:
                    max_gl = current_gl
            all_min.append(np.round(min_gl, 2))
            all_max.append(max_gl)
        range_gl = (min(all_min), max(all_max))
        print(line.format(range_gl))
    print("\\end{tabular}")
    print("\\caption[Bridge nodes $G_L$ range for each $q$]{Bridge nodes $G_L$ values ranges for each logical network version $q$. The $G_L$ ranges were obtained considering $I_{max}\\in\\{1,\\dots,"
          "10\\}$.}")
    print("\\label{tab:bridge_nodes_gl_range_by_q}")
    print("\\end{table}")

