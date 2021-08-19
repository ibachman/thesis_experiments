import data_proc.data_processing as dp
import os
import matplotlib.pyplot as plt
import numpy as np
from data_proc.plotting import n_line_plot


def plot_bridge_nodes(bridge_nodes_data, interlinks=None, title=""):
    inv_gls = []
    functional_clusters = []
    size = 10
    colors = []
    number_of_interlinks = []
    max_inv_gl_node = ""
    max_inv_gl = 0
    print("number of bridge nodes: {}".format(len(bridge_nodes_data.keys())))
    for node in bridge_nodes_data.keys():
        inv_gl = bridge_nodes_data[node]["nodes_lost"]/300.0
        if inv_gl > max_inv_gl:
            max_inv_gl = inv_gl
            max_inv_gl_node = node

        func_clusters = bridge_nodes_data[node]["functional_clusters"]
        if interlinks_per_node:
            number_of_interlinks.append(interlinks_per_node[node])
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
    if interlinks_per_node:
        x_axis = number_of_interlinks
        plt.xlabel('# interlinks', fontsize=15)
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
    plt.ylabel(r'1-$G_{L}$', fontsize=18)

    plt.show()
    return bridge_nodes_range


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
interlinks_per_node = dp.get_interlinks_for_logic_nodes(interlinks_path)

#bridge_nodes_data = dp.find_bridge_nodes(logic_network_path, providers_path)
#plot_bridge_nodes(bridge_nodes_data, interlinks=interlinks_per_node, title="Legacy ndep 3")

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
        interlinks_per_node = dp.get_interlinks_for_logic_nodes(interlinks_path)

        bridge_nodes_data = dp.find_bridge_nodes(logic_network_path, providers_path)
        #print(bridge_nodes_data.keys())
        #print("\nndep {}, lv {}: total bridge nodes = {}, ppv {}".format(ndep, lv, len(bridge_nodes_data.keys()), ppv))

        links = dp.add_interlinks_to_bridge_nodes(ndep, logic_network_path, providers_path, interlinks_path)
        links = ""
        print("({}, {}, {}): {},".format(ppv, ndep, lv, links))
        i += 1
        bridge_nodes_range_gl = plot_bridge_nodes(bridge_nodes_data, interlinks=interlinks_per_node,
                          title="ndep {}, lv {}, ppv {}".format(ndep, lv, ppv))
        all_bridge_node_ranges["min"] = min(all_bridge_node_ranges["min"], bridge_nodes_range_gl[0])
        all_bridge_node_ranges["max"] = max(all_bridge_node_ranges["max"], bridge_nodes_range_gl[1])
        all_nodes = dp.find_bridge_nodes(logic_network_path, providers_path, get_all_nodes=True)
        all_nodes_list.append(all_nodes)
    print("Range for q={}: ({},{})".format(lv, np.round(all_bridge_node_ranges["min"], 3), np.round(all_bridge_node_ranges["max"], 3)))

exit(9)
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

