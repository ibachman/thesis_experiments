import data_proc.common_plots as cp
import data_proc.data_processing as dp
import numpy as np


def make_link_length_table_original_strategies():

    models = ["RNG", "GG", "5NN"]  #
    strategies = ["distance_aux", "local_hubs", "degree_aux", "random"]
    spaces = [(20, 500), (100, 100)]  # [(100, 100)]#,
    coord_dir = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/node_locations/"
    max_link_lengths = {}
    for s in spaces:
        max_link_lengths[s] = {}
        for m in models:
            max_link_lengths[s][m] = {}
            for st in strategies:
                max_link_lengths[s][m][st] = []
                for v in range(1, 11):
                    strategy_path = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/extra_edges/{}/candidates_{}x{}_exp_2.5_v{}_m_{}.csv".format(st, s[0], s[1], v, m)
                    edge_list = cp.load_edges_as_list(strategy_path)
                    cord_name = "nodes_{}x{}_exp_2.5_v{}.csv".format(s[0], s[1], v)
                    coord_dict = cp.get_list_of_coordinates_from_csv(coord_dir + cord_name)
                    all_lengths = cp.all_link_lengths(coord_dict, edge_list)
                    this_version_max_link_length = max(all_lengths)
                    max_link_lengths[s][m][st].append(this_version_max_link_length)
    all_data = dp.run_data()
    print("\\begin{table}[]")
    print("\\centering")
    print("\\begin{tabular}{|l|l|l|l|l|}")
    print("\\hline")
    print("Space                   & Strategy   & RNG   & GG    & 5NN   \\\\ \\hline")
    for s in spaces:
        s_name = all_data["figure_space_names"][s]
        line = "\\multirow{4}{*}{" + s_name + "} "
        for st in strategies:

            line += "& {} ".format(all_data["strategies_used_names"][st])
            for m in models:
                mean = round(np.mean(max_link_lengths[s][m][st]), 2)
                std = round(np.std(max_link_lengths[s][m][st]), 2)
                line += "& {} ({})".format(mean, std)
            if st != "random":
                line += "\\\\ \\cline{2-5}"
            else:
                line += "\\\\ \\hline"
            print(line)
            line = ""
    print("\\end{tabular}")
    print("\\caption{}")
    print("\\label{}")
    print("\\end{table}")


def make_link_length_table_random_modifications():

    models = ["RNG", "GG", "5NN"]  #
    strategies = ["0.01", "0.05", "0.25", "0.5", "0.75"]
    spaces = [(20, 500), (100, 100)]  # [(100, 100)]#,
    coord_dir = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/node_locations/"
    max_link_lengths = {}
    for s in spaces:
        max_link_lengths[s] = {}
        for m in models:
            max_link_lengths[s][m] = {}
            for st in strategies:
                max_link_lengths[s][m][st] = []
                for v in range(1, 11):
                    strategy_path = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/extra_edges/random/candidates_cl_cap{}_{}x{}_exp_2.5_v{}_m_{}.csv".format(st, s[0],
                                                                                                                                                                                         s[1], v, m)
                    edge_list = cp.load_edges_as_list(strategy_path)
                    cord_name = "nodes_{}x{}_exp_2.5_v{}.csv".format(s[0], s[1], v)
                    coord_dict = cp.get_list_of_coordinates_from_csv(coord_dir + cord_name)
                    all_lengths = cp.all_link_lengths(coord_dict, edge_list)
                    this_version_max_link_length = max(all_lengths)
                    max_link_lengths[s][m][st].append(this_version_max_link_length)
    all_data = dp.run_data()
    print("\\begin{table}[]")
    print("\\centering")
    print("\\begin{tabular}{|l|l|l|l|l|}")
    print("\\hline")
    print("Space                   & Max. link length   & RNG   & GG    & 5NN   \\\\ \\hline")
    for s in spaces:
        s_name = all_data["figure_space_names"][s]
        line = "\\multirow{4}{*}{" + s_name + "} "
        for st in strategies:

            line += "& {} ".format(all_data["strategies_used_names"][st])
            for m in models:
                mean = round(np.mean(max_link_lengths[s][m][st]), 2)
                std = round(np.std(max_link_lengths[s][m][st]), 2)
                line += "& {} ({})".format(mean, std)
            if st != "random":
                line += "\\\\ \\cline{2-5}"
            else:
                line += "\\\\ \\hline"
            print(line)
            line = ""
    print("\\end{tabular}")
    print("\\caption{}")
    print("\\label{}")
    print("\\end{table}")


def length_gl_correlation_figure(save_fig=True):
    cp.show_legacy_tgl_vs_max_link_length((20, 500), ndep=3, save_figure=save_fig)
    cp.show_legacy_tgl_vs_max_link_length((100, 100), ndep=3, save_figure=save_fig)


def cap_random_boxplots(save_fig=True):
    mr = True
    cp.show_legacy_tgl_boxplot("RNG", ndep=3, mod_random=mr, save_figure=save_fig)
    cp.show_legacy_tgl_boxplot("GG", ndep=3, mod_random=mr, save_figure=save_fig)
    cp.show_legacy_tgl_boxplot("5NN", ndep=3, mod_random=mr, save_figure=save_fig)


def original_boxplots(save_fig=True):
    mr = False
    cp.show_legacy_tgl_boxplot("RNG", ndep=3, mod_random=mr, save_figure=save_fig)
    cp.show_legacy_tgl_boxplot("GG", ndep=3, mod_random=mr, save_figure=save_fig)
    cp.show_legacy_tgl_boxplot("5NN", ndep=3, mod_random=mr, save_figure=save_fig)


cap_random_boxplots(save_fig=False)

