import data_proc.data_processing as dp
import os
import data_proc.common_plots as cp
import matplotlib.pyplot as plt
import numpy as np


def bridge_node_interlink_coefficient(bridge_nodes, interlinks):
    sum = 0
    for node in bridge_nodes.keys():
        inv_gl = bridge_nodes[node]["nodes_lost"]/300.0
        current_node_interlinks = interlinks[node]
        sum += inv_gl/current_node_interlinks
    return sum


def make_correlation_table(correlation_dict):
    print("\\begin{table}[]")
    print("\\small")
    print("\\tabcolsep = 0.11cm")
    print("\\begin{tabular}{|c|l|l|l|l|l|l|l|}")
    print("\\hline")
    print("$q$                 & space  & RNG & GG & GPA & 5NN & YAO & ER \\\\ \\hline")
    for lv in range(1, 11):
        line_1 = "\\multirow{2}{*}{" + str(lv) + "}  & (1:25)"
        line_2 = "                    & (1:1) "
        for model in ['RNG', 'GG', 'GPA', '5NN', 'YAO', 'ER']:
            line_1 += " &  {} ".format(correlation_dict[model][lv][(20, 500)])
            line_2 += " &  {} ".format(correlation_dict[model][lv][(100, 100)])
        line_1 += " \\\\ \\cline{2-8}"
        line_2 += "\\\\ \\hline"
        print(line_1)
        print(line_2)
    print("\\end{tabular}")
    print("\\end{table}")


def get_data_for_correlation_table(prefix=""):
    if len(prefix) > 1:
        if prefix[-1] != "_":
            prefix += "_"
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    interlink_type = "provider_priority"
    interlink_version = 3

    strategy = "simple graphs"

    bn_list = []
    p_means_list = []
    correlations = {}
    for model in ['RNG', 'GG', 'GPA', '5NN', 'YAO', 'ER']:
        correlations[model] = {}
        for lv in range(1, 11):
            correlations[model][lv] = {}
            for space in [(20, 500), (100, 100)]:
                bn_list = []
                p_means_list = []
                for ndep in list(range(1, 11)):
                    logic_file_name = "logic_exp_2.5_v{}.csv".format(lv)

                    logic_network_path = os.path.join(base_path, "networks", "logical_networks", logic_file_name)

                    provider_file_name = "providers_ndep_{}_lprovnum_6_v{}.csv".format(ndep, interlink_version)
                    providers_path = os.path.join(base_path, "networks", "providers", "provider_priority", provider_file_name)

                    interlinks_file_name = "dependence_ndep_{}_lprovnum_6_v{}.csv".format(ndep, interlink_version)
                    interlinks_path = os.path.join(base_path, "networks", "interdependencies", "provider_priority",
                                                   interlinks_file_name)
                    interlinks_per_node = dp.get_interlinks_for_logic_nodes(interlinks_path)
                    bridge_nodes_data = dp.find_bridge_nodes(logic_network_path, providers_path)
                    bn_coefficient = bridge_node_interlink_coefficient(bridge_nodes_data, interlinks_per_node)
                    lvs, curves_as_p = cp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, legacy=False, m_results=False, add_to_title=prefix)
                    p_means = np.mean(curves_as_p)
                    bn_list.append(bn_coefficient)
                    p_means_list.append(p_means)
                corr = np.corrcoef(bn_list, p_means_list)
                correlations[model][lv][space] = np.round(corr[0, 1], 3)
    return correlations


def times_imax_appears_in(imax, setlist):
    total = len(setlist)
    appears = 0
    for a_list in setlist:
        if imax in a_list:
            appears += 1
    return appears/total


def table_imax_apparition(setlist_dict):
    print("\\begin{table}[]")
    print("\\small")
    print("\\tabcolsep = 0.11cm")
    print("\\begin{tabular}{|l|l|l|l|l|}")
    print("\\hline")
    print("$I_{max}$ & Combined (1:1) + (1:25) & (1:1) & (1:25) & (1:25) + extra interlinks \\\\ \\hline")
    total_1to1 = len(setlist_dict[(100, 100)])
    total_1to25 = len(setlist_dict[(20, 500)])
    total_elements = total_1to1 + total_1to25
    total_with_extra_links = len(setlist_dict[(0, 0)])
    sum_total_elements = 0
    sum_1to1 = 0
    sum_1to25 = 0
    sum_with_extra_links = 0
    for imax in range(1, 11):
        current_line = " {} ".format(imax)
        appears_total_elements = np.round(times_imax_appears_in(imax, setlist_dict[(100, 100)] + setlist_dict[(20, 500)]) * 100, 2)
        current_line += "& {}\% ".format(appears_total_elements)
        appears_1to1 = np.round(times_imax_appears_in(imax, setlist_dict[(100, 100)]) * 100, 2)
        current_line += "& {}\% ".format(appears_1to1)
        appears_1to25 = np.round(times_imax_appears_in(imax, setlist_dict[(20, 500)]) * 100, 2)
        current_line += "& {}\% ".format(appears_1to25)
        appears_extralinks = np.round(times_imax_appears_in(imax, setlist_dict[(0, 0)]) * 100, 2)
        current_line += "& {}\% \\\\ \\hline".format(appears_extralinks)
        print(current_line)
    print("\\end{tabular}")
    print("\\end{table}")


list_dict = {(100, 100): [[7, 9], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9],
                          [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9],
                          [7, 8], [7, 8], [7, 8], [7, 8], [7, 8], [7, 8],
                          [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9],
                          [7], [7], [7], [7], [7], [7],
                          [7], [7], [7], [7], [7], [7],
                          [4, 6, 8], [4, 6, 8], [4, 6, 8], [4, 6, 8], [4, 6, 8], [4, 6, 8],
                          [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9],
                          [3, 7], [3, 7], [3, 7], [3, 7], [3, 7], [3, 7, 9],
                          [4, 8, 10], [4, 8, 10], [4, 8, 10], [4, 8, 10], [4, 8, 10], [4, 8, 10]
                          ],
             (20, 500): [[7, 9], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9],
                         [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9],
                         [7, 8], [7, 8], [7, 8], [7, 8], [7, 8], [7, 8],
                         [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9], [4, 7, 9],
                         [7], [7], [7], [7], [7], [7],
                         [7], [7], [7], [7], [7], [7],
                         [4, 6, 8, 10], [4, 6, 8, 10], [4, 6, 8, 10], [4, 6, 8], [4, 6, 8], [4, 6, 8],
                         [5, 9], [5, 9], [5, 9], [5, 9], [5, 9], [5, 9],
                         [3, 7], [3, 7], [3, 7], [3, 7], [3, 7], [3, 7],
                         [4, 8, 10], [4, 8, 10], [4, 8, 10], [4, 8, 10], [4, 8, 10], [4, 8, 10]
                         ],
             (0, 0): [[7], [7], [7], [7], [7], [7],
                      [8], [8], [7], [8], [8], [8],
                      [5, 7], [5, 7], [5, 7], [5], [5], [7],
                      [7], [7], [7], [7], [7],
                      [4, 8], [4, 8], [8], [8], [8],
                      [7], [7, 9], [7, 9], [7, 9], [7, 9], [7, 9],
                      [7], [7], [7], [7], [7],
                      [8], [8], [8]
                      ]}

