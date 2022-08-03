import os
import sys
sys.path.append(os.getcwd())
import data_proc.common_plots as cp
import data_proc.plotting as pt
import data_proc.LA_vs_RA_plots as vs
import data_proc.data_processing as dp
import data_proc.logic_network_analysis as lna
import data_proc.bridgenode_correlations as bnc
import data_proc.generate_tgl_table as gtglt
import data_proc.get_average_cost as cost
import numpy as np
#import common_plots as cp
#import plotting as pt
#import LA_vs_RA_plots as vs


ppv = 3


def pre_process_LA_scatter_data(model, radius=20, ndep=3, strategy=["distance_aux", "local_hubs", "degree_aux", "random", "simple graphs"]):
    geometry = ["20x500", "100x100"]
    for g in geometry:
        for st in strategy:
            pt.write_stuff(g, st, use_model=[model], ndep=ndep, radius=radius)


def pre_process_seismic_scatter_data(model, ndep=3, strategy=["distance_aux", "local_hubs", "degree_aux", "random", "simple graphs"]):
    geometry = ["20x500"]
    for g in geometry:
        for st in strategy:
            pt.write_stuff(g, st, use_model=[model], ndep=ndep, is_seismic=True)


def get_lines_cap3(save_figure=True, prefix="", lvs=range(1, 11), spaces=[(20, 500), (100, 100)]):
    strategy = "simple graphs"
    interlink_type = "provider_priority"

    for logic_net_version in lvs:
        print(logic_net_version)
        for space in spaces:
            print(space)
            for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
                cp.show_averages_for_all_imax(logic_net_version, interlink_type, ppv, model, space, strategy, m_results=False, save_fig=False, autoclose=False, save_to="", all_imax=None, prefix=prefix)


def get_boxplots_cap_3(save_figure=True, ndeps=list(range(1, 11)), prefix=""):
    for ndep in ndeps:
        print(ndep)
        for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
            cp.show_curves_as_points_by_space("provider_priority", ppv, model, "simple graphs", ndep, m_results=False, save_fig=save_figure, prefix=prefix)


def generate_tgl_table_cap3(imax, prefix=""):
    gtglt.tgl_table_for_imax(imax, prefix=prefix)


def get_bars_cap_3(save_figure=True, prefix=""):
    for imax in range(1, 11):
        cp.show_curves_as_bar_and_error_by_model_double_plot("provider_priority", ppv, imax, "simple graphs", m_results=False, save_fig=save_figure, prefix=prefix)


def get_imax_lines_cap_3(save_figure=True, check_u_q=False, prefix=""):
    for lv in range(1, 11):
        cp.show_imaxes_as_lines_with_error_tgl(lv, "provider_priority", ppv, (20, 500), "simple graphs", m_results=False, save_fig=save_figure, check_u_q=check_u_q, prefix=prefix)


def get_detailed_iteration_analisys_cap_3(save_figure=True, ndeps=list(range(1, 11))):
    for space in [(20, 500), (100, 100)]:
        for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
            for ndep in ndeps:
                cp.stacked_plot_and_avg_gl_line(model, space, ndep, version=4, number_of_iterations=100, wigle=0.05, autoclose=False, save_fig=False)


def generate_u_q_table_cap3(prefix=""):
    cp.make_u_q_table_for_all_logic_versions_and_spaces(interlink_type="provider_priority", interlink_version=3, strategy="simple graphs", prefix=prefix)


def get_bridge_node_analysis_cap_4(save_figure=True):
    lna.plot_bridge_nodes_danziger_rev(mode="degree_damage", save_figure=save_figure)
    lna.plot_bridge_nodes_danziger_rev(mode="delta", save_figure=save_figure)


def get_correlations_table_cap4(prefix=""):
    bnc.make_correlation_table(bnc.get_data_for_correlation_table(prefix=prefix))


def get_tgl_table_after_adding_interlinks_cap4(save_figure=False, prefix=""):
    for lv in range(1, 11):
        cp.show_imaxes_as_lines_with_error_tgl(lv, "provider_priority", ppv, (20, 500), "simple graphs", m_results=[False, True], save_fig=save_figure, check_u_q=True, write_table=True,
                                               prefix=prefix, show=False)


def get_table_4p4_cap4(prefix=""):
    use_list = bnc.list_dict
    if prefix == "seq_comp_it100":
        use_list = bnc.list_dict_2
    bnc.table_imax_apparition(use_list)


def get_table_4p5_cap4(prefix=""):
    cp.make_u_q_table_comparison_after_adding_interlinks(interlink_type="provider_priority", interlink_version=3, strategy="simple graphs", prefix=prefix)


def get_imax_lines_cap_4(save_figure=True, check_u_q=False, prefix=""):
    for lv in range(1, 11):
        cp.show_imaxes_as_lines_with_error_tgl(lv, "provider_priority", ppv, (20, 500), "simple graphs", m_results=[False, True], save_fig=save_figure, check_u_q=check_u_q, prefix=prefix)


def get_table_5p1():
    lna.table_with_bn_gl_value_ranges_for_all_imax()


def get_curves_cap_5(save_figure=True, debug=False, lv=1, prefix=""):
    # CREO QUE NO SE USA // USAR v2
    for imax in [3, 5, 7, 10]:
        for sp in [(20, 500), (100, 100)]:
            for model in ["RNG", "GPA", "GG", "5NN", "YAO", "ER"]:
                cp.gl_compare_strategies(lv, sp, model, imax, debug=debug, save_fig=save_figure, prefix=prefix)


def get_curves_cap_5_v2(save_figure=True, debug=False, lv=1, prefix=""):
    strategies = ["distance_aux", "local_hubs", "degree_aux", "random"]
    interlink_type = "provider_priority"
    spaces = [(20, 500), (100, 100)]

    for strategy in strategies:
        for space in spaces:
            for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
                cp.show_averages_for_all_imax(lv, interlink_type, ppv, model, space, strategy, m_results=False, save_fig=False, autoclose=False, save_to="", all_imax=[3, 5, 7, 10], prefix=prefix)


def get_boxplots_cap_5(save_figure=True, prefix=""):
    for sp in [(20, 500), (100, 100)]:
        for imax in [3, 5, 7, 10]:
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="distance_aux", space=sp, save_fig=save_figure, prefix=prefix)
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="local_hubs", space=sp, save_fig=save_figure, prefix=prefix)
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="degree_aux", space=sp, save_fig=save_figure, prefix=prefix)
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="random", space=sp, save_fig=save_figure, prefix=prefix)


def get_cap_random_boxplots_cap5(save_fig=True, ndep=3, prefix=""):
    mr = True
    legacy = False
    cp.show_legacy_tgl_boxplot("RNG", ndep=ndep, mod_random=mr, save_figure=save_fig, legacy=legacy, prefix=prefix)
    cp.show_legacy_tgl_boxplot("GG", ndep=ndep, mod_random=mr, save_figure=save_fig, legacy=legacy, prefix=prefix)
    cp.show_legacy_tgl_boxplot("5NN", ndep=ndep, mod_random=mr, save_figure=save_fig, legacy=legacy, prefix=prefix)
    cp.show_legacy_tgl_boxplot("YAO", ndep=ndep, mod_random=mr, save_figure=save_fig, legacy=legacy, prefix=prefix)
    cp.show_legacy_tgl_boxplot("GPA", ndep=ndep, mod_random=mr, save_figure=save_fig, legacy=legacy, prefix=prefix)
    cp.show_legacy_tgl_boxplot("ER", ndep=ndep, mod_random=mr, save_figure=save_fig, legacy=legacy, prefix=prefix)


def get_double_curves_st_comp_cap5(save_figure=True, lv=1, prefix=""):
    for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
        cp.show_imaxes_as_lines_with_error_tgl(lv, "provider_priority", ppv, (20, 500), "", save_fig=save_figure, strategies_comp=model, prefix=prefix)
        cp.show_imaxes_as_lines_with_error_tgl(1, "provider_priority", ppv, (20, 500), "", save_fig=save_figure, strategies_comp=model, name_mod='1250', prefix=prefix)


def get_length_correlation_figure_cap5(save_fig=True, ndep=3, prefix=""):
    cp.show_legacy_tgl_vs_max_link_length((20, 500), ndep=ndep, save_figure=save_fig, legacy=False, models=["RNG", "GG", "5NN"], img_ver=1, prefix=prefix)
    cp.show_legacy_tgl_vs_max_link_length((20, 500), ndep=ndep, save_figure=save_fig, legacy=False, models=["GPA", "YAO", "ER"], img_ver=2, prefix=prefix)
    cp.show_legacy_tgl_vs_max_link_length((100, 100), ndep=ndep, save_figure=save_fig, legacy=False, models=["RNG", "GG", "5NN"], img_ver=1, prefix=prefix)
    cp.show_legacy_tgl_vs_max_link_length((100, 100), ndep=ndep, save_figure=save_fig, legacy=False, models=["GPA", "YAO", "ER"], img_ver=2, prefix=prefix)


def get_table_link_length_original_strategies_cap5():
    models = ["RNG", "GG", "5NN", "GPA", "YAO", "ER"]  #
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
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\makebox[\\linewidth]{\\small")
    print("\\tabcolsep = 0.11cm")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    print("Space                   & Strategy   & RNG   & GG    & 5NN & GPA & YAO & ER   \\\\ \\hline")
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
                line += "\\\\ \\cline{2-8}"
            else:
                line += "\\\\ \\hline"
            print(line)
            line = ""
    print("\\end{tabular}")
    print("}")
    print("\\caption{}")
    print("\\label{}")
    print("\\end{table}")


def make_link_length_table_random_modifications_cap5():

    models = ["RNG", "GG", "5NN", "GPA", "YAO", "ER"]  #
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
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\makebox[\\linewidth]{\\small")
    print("\\tabcolsep = 0.11cm")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    print("Space                   & Max. link length   & RNG   & GG    & 5NN  & GPA & YAO & ER  \\\\ \\hline")
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
                line += "\\\\ \\cline{2-8}"
            else:
                line += "\\\\ \\hline"
            print(line)
            line = ""
    print("\\end{tabular}")
    print("}")
    print("\\caption{}")
    print("\\label{}")
    print("\\end{table}")


def get_table_5p6_cap5(imax, prefix):
    cost.check_cost_efficiency(imax, debug=False, prefix=prefix)


def get_table_5p7_cap5(prefix=""):
    cost.check_cost_efficiency_distance_plus(add_to_title="1250", prefix=prefix)


def get_table_5p9_cap5(prefix=""):
    cost.check_cost_efficiency_distance_bs(add_to_title="3000", prefix=prefix)


def get_double_delta_gl_la_ra_cap6(save_figure=True, lv=1):
    models = ["RNG", "GPA", "GG", "5NN", "YAO", "ER"]
    strategy = ["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]
    for imax in [3]:#, 5, 7, 10]:
        for st in strategy:
            vs.plot_la_ra_delta_for_strategy(st, imax, models, is_legacy=False, lv=lv, save_fig=save_figure)


def get_scatter_plot_base_cap_6(save_figure=True, imax=3, strategies=["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]):
    geometries = ["20x500", "100x100"]
    radius = 20
    for s in geometries:
        for st in strategies:
            pt.scatter_plot(["5NN", "GG", "RNG", "GPA", "YAO", "ER"], s, st, imax, radius, map="models", legacy=False, save_fig=save_figure)


def get_scatter_plot_find_cap_6(save_figure=True, imax=3, strategies=["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"], radius=20):
    geometries = ["20x500", "100x100"]
    for s in geometries:
        print("---------------> {}".format(s))
        for st in strategies:
            pt.scatter_plot(["5NN", "GG", "RNG", "GPA", "YAO", "ER"], s, st, imax, radius, map="find", legacy=False, save_fig=save_figure)


def get_hdla_tables_cap6(imax, radius=20):
    a = radius/20
    if a == 1.0:
        a = "1"
    number_of_hdla = {}
    hdla_range = {}
    strategies = ["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]
    st_name = {"simple graphs": "Original", "distance_aux": "Distance", "local_hubs": "Local hubs", "degree_aux": "Degree", "random": "Random"}

    geometries = ["20x500", "100x100"]
    s_name = {"20x500": "(1:25)", "100x100": "(1:1)"}
    for s in geometries:
        number_of_hdla[s] = {}
        hdla_range[s] = {}
        for st in strategies:
            hdla_range[s][st] = {}
            number_of_hdla[s][st] = pt.scatter_plot(["5NN", "GG", "RNG", "GPA", "YAO", "ER"], s, st, imax, radius, map="find", legacy=False, save_fig=False, return_data=True)
            higher, lower = pt.scatter_plot(["5NN", "GG", "RNG", "GPA", "YAO", "ER"], s, st, imax, radius, map="models", legacy=False, save_fig=False, return_data=True)
            hdla_range[s][st]['high'] = higher
            hdla_range[s][st]['low'] = lower
    # print table
    ## headers
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\makebox[\\linewidth]{\\small")
    print("\\tabcolsep = 0.11cm")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    print("\\multicolumn{11}{|c|}{$I_{max}=" + str(imax) + "$}                                                                                          \\\\ \\hline")
    print("\\multirow{2}{*}{$s$} &")
    print("  \\multirow{2}{*}{$st$} &")
    print("  \\multicolumn{7}{l|}{Number of HDLA} &")
    print("  \\multirow{2}{*}{$G_L$ range (HDLA)} &")
    print("  \\multirow{2}{*}{$G_L$ range (Non-HDLA)} \\\\ \\cline{3-9}")
    print("                        &                & Total & RNG & GG & GPA & 5NN & YAO & ER &                 &                  \\\\ \\hline")
    ordered_columns_hdla_number = ['total', 'RNG', 'GG', 'GPA', '5NN', 'YAO', 'ER']
    ordered_ranges = ['low', 'high']
    for s in geometries:
        line = "\\multirow{5}{*}{" + s_name[s] + "} "
        for st in strategies:
            line += "& {} ".format(st_name[st])
            for hdla_col in ordered_columns_hdla_number:
                line += "& {} ".format(number_of_hdla[s][st][hdla_col])
            for this_range in ordered_ranges:
                if len(hdla_range[s][st][this_range]) > 0:
                    min_r = round(min(hdla_range[s][st][this_range]), 3)
                    max_r = round(max(hdla_range[s][st][this_range]), 3)
                    if 0.5034 > min_r >= 0.503:
                        min_r = 0.5
                    if 0.5034 > max_r >= 0.503:
                        max_r = 0.5
                    line += "& $({},{})$ ".format(min_r, max_r)
                else:
                    line += "& $\phi$ "
            if st != "random":
                line += "\\\\ \\cline{2-11} "
            else:
                line += "\\\\ \\hline"
            print(line)
            line = "                        "
    print("\\end{tabular}")
    print("}")
    print("\\caption[$G_L$ ranges of HDLA and non-HDLA $(I_{max}=3,a=" + str(a) + ")$]{$G_L$ ranges of HDLA, and LA minus HDLA (Non-HDLA) of systems with and without physical links added for $I_{"
                                                                               "max}=" + str(imax) + "$, and $a=" + str(a) + "$.}")
    print("\\label{tab:LA-ranges-imax-" + str(imax) + "-a" + str(a) + "}")
    print("\\end{table}")
    #print(max(hdla_range["20x500"]["simple graphs"]['low']))


def get_scatter_plot_base_cap_7(save_figure=True, imax=3, models=["5NN", "GG", "RNG", "GPA", "YAO", "ER"], strategies=["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"],
                                sclose=False):
    geometries = ["20x500"]
    radius = 20
    for s in geometries:
        for st in strategies:
            pt.scatter_plot(models, s, st, imax, radius, map="models", legacy=False, save_fig=save_figure, is_seismic=True, chapter=7, autoclose=sclose)


def get_scatter_plot_magnitude_cap_7(save_figure=True, imax=3, models=["5NN", "GG", "RNG", "GPA", "YAO", "ER"], strategies=["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"],
                                     sclose=False):
    geometries = ["20x500"]
    radius = 20
    for s in geometries:
        for st in strategies:
            pt.scatter_plot(models, s, st, imax, radius, map="magnitude", legacy=False, save_fig=save_figure, is_seismic=True, chapter=7, autoclose=sclose)


def get_scatter_plot_find_cap_7(save_figure=True, imax=3, models=["RNG", "5NN", "GG", "GPA", "YAO", "ER"], strategies=["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"],
                                sclose=False):
    geometries = ["20x500"]
    radius = 20
    for s in geometries:
        for st in strategies:
            pt.scatter_plot(models, s, st, imax, radius, map="find", legacy=False, save_fig=save_figure, is_seismic=True, chapter=7, autoclose=sclose)


def get_seismic_table_data_cap_7(imax=3, strategy="simple graphs"):
    models = ["RNG", "5NN", "GG", "GPA", "YAO", "ER"]
    geometry = "20x500"
    radius = 20
    lv = 1
    hdlas_per_model = {}
    Mw_per_model = {"HDLA": {}, "non-HDLA": {}}
    gls = {"HDLA": {}, "non-HDLA": {}}
    nonhdlas_per_model = {}

    number_of_HDLA = {}
    number_of_nonHDLA = {}
    HDLA_gl_range = {}
    nonHDLA_gl_range = {}
    HDLA_Mw_range = {}
    nonHDLA_Mw_range = {}

    for model in models:
        hdlas_per_model[model] = []
        nonhdlas_per_model[model] = []
        Mw_per_model["HDLA"][model] = []
        Mw_per_model["non-HDLA"][model] = []
        gls["HDLA"][model] = []
        gls["non-HDLA"][model] = []
        nonhdlas_per_model[model] = []

        number_of_HDLA[model] = []
        number_of_nonHDLA[model] = []
        HDLA_gl_range[model] = []
        nonHDLA_gl_range[model] = []
        HDLA_Mw_range[model] = []
        nonHDLA_Mw_range[model] = []

        for version in range(1, 11):

            x_center, y_center, radius, other_data = dp.get_data_from_seismic_attack(model, geometry, strategy, imax, version, lv=1, find="l50")
            for k in range(len(x_center)):
                is_l50 = other_data["is_l50"][k]
                Mw = other_data["Mw"][k]
                GL = other_data["g_l"][k]
                if GL <= 0.503:
                    if is_l50:
                        hdlas_per_model[model].append(1)
                        Mw_per_model["HDLA"][model].append(Mw)
                        gls["HDLA"][model].append(other_data["g_l"][k])
                    else:
                        print("AYUDA")
                else:
                    Mw_per_model["non-HDLA"][model].append(Mw)
                    nonhdlas_per_model[model].append(1)
                    gls["non-HDLA"][model].append(GL)
        if len(Mw_per_model["HDLA"][model]) < 1:
            Mw_per_model["HDLA"][model].append(-1)
        if len(gls["HDLA"][model]) < 1:
            gls["HDLA"][model].append(-1)

        number_of_HDLA[model].append(len(hdlas_per_model[model]))
        number_of_nonHDLA[model].append(len(nonhdlas_per_model[model]))
        HDLA_gl_range[model].append((min(gls["HDLA"][model]), max(gls["HDLA"][model])))
        nonHDLA_gl_range[model].append((min(gls["non-HDLA"][model]), max(gls["non-HDLA"][model])))
        HDLA_Mw_range[model].append((min(Mw_per_model["HDLA"][model]), max(Mw_per_model["HDLA"][model])))
        nonHDLA_Mw_range[model].append((min(Mw_per_model["non-HDLA"][model]), max(Mw_per_model["non-HDLA"][model])))
        debug = False
        if debug:
            print(" -- Nº HDLA: {}\nHDLA Mw range: ({}, {})".format(len(hdlas_per_model[model]), min(Mw_per_model["HDLA"][model]), max(Mw_per_model["HDLA"][model])))
            print("HDLA GL range: ({}, {})".format(min(gls["HDLA"][model]), max(gls["HDLA"][model])))
            print(" -- Nº Non-HDLA: {}".format(len(nonhdlas_per_model[model])))
            print("non-HDLA Mw range: ({}, {})".format(min(Mw_per_model["non-HDLA"][model]), max(Mw_per_model["non-HDLA"][model])))
            print("non-HDLA GL range: ({}, {})".format(min(gls["non-HDLA"][model]), max(gls["non-HDLA"][model])))

    return number_of_HDLA, number_of_nonHDLA, HDLA_gl_range, nonHDLA_gl_range, HDLA_Mw_range, nonHDLA_Mw_range


def make_seismic_table_simple_graphs_cap_7(st="simple graphs"):
    print("\\begin{table}[]")
    print("\\centering")
    print("\\begin{tabular}{|l|l|l|l|l|}")
    print("\\hline")
    for imax in [3, 5, 7, 10]:
        print("\\multicolumn{5}{|c|}{$I_{max}=" + str(imax) + "$} \\\\ \\hline")
        print("$m$            & Number of HDSA & $M_w$ range (HDSA) & $G_L$ range (HDSA) & $G_L$ range (Non-HDSA) \\\\ \\hline")
        number_of_HDLA, number_of_nonHDLA, HDLA_gl_range, nonHDLA_gl_range, HDLA_Mw_range, nonHDLA_Mw_range = get_seismic_table_data_cap_7(imax=imax, strategy=st)

        for model in ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]:
            if number_of_HDLA[model][0] > 0:
                Mw_range = HDLA_Mw_range[model][0]
                gl_range = HDLA_gl_range[model][0]
            else:
                Mw_range = "-"
                gl_range = "-"
            print("{} & {} & {} & {} & {} \\\\ \\hline".format(model, number_of_HDLA[model][0], Mw_range, gl_range, nonHDLA_gl_range[model][0]))

    print("\\end{tabular}")
    if st == "local_hubs":
        st = "local hubs"
    print("\\caption{Summary table for simple attacks (" + st.replace("_aux", "") + ").}")
    if st == "local hubs":
        st = "local-hubs"
    print("\\label{tab:seismic-summary-" + st.replace("_aux", "") + "}")
    print("\\end{table}")


def make_seismic_table_all_strategies_cap_7(imax=3):
    st_names_dict = {"simple graphs": "Original", "distance_aux": "Distance", "local_hubs": "Local hubs", "degree_aux": "Degree", "random": "Random"}
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\small")
    print("\\tabcolsep = 0.11cm")
    print("\\begin{tabular}{|l|l|l|l|l|}")
    print("\\hline")
    for st in ["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]:
        print("\\multicolumn{7}{|c|}{$st$ = " + st_names_dict[st] + "} \\\\ \\hline")
        print("$m$            & Number of HDSA & $M_w$ range (HDSA) & $G_L$ range (HDSA) & $G_L$ range (Non-HDSA) \\\\ \\hline")
        number_of_HDLA, number_of_nonHDLA, HDLA_gl_range, nonHDLA_gl_range, HDLA_Mw_range, nonHDLA_Mw_range = get_seismic_table_data_cap_7(imax=imax, strategy=st)

        for model in ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]:
            if number_of_HDLA[model][0] > 0:
                Mw_range = HDLA_Mw_range[model][0]
                gl_range = HDLA_gl_range[model][0]
            else:
                Mw_range = "-"
                gl_range = "-"
            print("{} & {} & {} & {} & {} \\\\ \\hline".format(model, number_of_HDLA[model][0], Mw_range, gl_range, nonHDLA_gl_range[model][0]))

    print("\\end{tabular}")

    print("\\caption[Seismic attacks summary after adding extra physical links ($I_{max}=" + str(imax) + "$)]{Summary of seismic attacks performed over systems with extra physical links added,"
                                                                                                         " and $I_{max}=" + str(imax) + "$.}")

    print("\\label{tab:seismic-summary-imax-" + str(imax) + "}")
    print("\\end{table}")


def la_sa_comparison_scatter_cap_7(save_fig=True, sclose=False, st="simple graphs", ndep=None):
    if ndep is None:
        imaxes = [3, 5, 7, 10]
    else:
        imaxes = [ndep]
    for imax in imaxes:
        cp.la_sa_comparison_scatter_plot(ndep=imax, save_fig=save_fig, autoclose=sclose, strategy=st)


def make_la_sa_comparison_table_cap_7(st="simple graphs"):
    models = ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]
    print("\\begin{table}[]")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    for imax in [3, 5, 7, 10]:
        print("\\multicolumn{8}{|c|}{$I_{max}=" + str(imax) + "$} \\\\ \\hline")
        print("       & RNG & GG & GPA & 5NN & YAO & ER & Total\\\\ \\hline")
        line_high = "Damage SA > Damage LA "
        line_mid = "Damage SA $\sim$ Damage LA "
        line_low = "Damage SA < Damage LA "
        total = 103000
        all_upper = 0
        all_mid = 0
        all_lower = 0
        for model in models:
            upper, mid, lower, lower_gl_delta, higher_gl_delta = dp.compare_seismic_attacks_with_localized_attacks(model, imax, strategy=st, lv=1)
            line_high += "& {}\\% ".format(round(100 * upper/total, 1))
            line_mid += "& {}\\% ".format(round(100 * mid/total, 1))
            line_low += "& {}\\% ".format(round(100 * lower/total, 1))
            all_upper += upper
            all_mid += mid
            all_lower += lower

        line_high += "& {}\\% \\\\ \\hline".format(round(100 * all_upper/(total * len(models)), 1))
        line_mid += "& {}\\% \\\\ \\hline".format(round(100 * all_mid/(total * len(models)), 1))
        line_low += "& {}\\% \\\\ \\hline".format(round(100 * all_lower/(total * len(models)), 1))
        print(line_high)
        print(line_mid)
        print(line_low)

    print("\\hline")
    print("\\end{tabular}")
    if st == "local_hubs":
        st = "local hubs"
    print("\\caption{Comparison between localized attacks and seismic attacks (" + st.replace("_aux", "") + ").}")
    if st == "local hubs":
        st = "local-hubs"
    print("\\label{tab:sa-la-comparison-" + st.replace("_aux", "") + "}")
    print("\\end{table}")


def make_la_sa_comparison_table_all_strategies_cap_7(imax):
    models = ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]

    st_names_dict = {"simple graphs": "Original", "distance_aux": "Distance", "local_hubs": "Local hubs", "degree_aux": "Degree", "random": "Random"}
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\small")
    print("\\tabcolsep = 0.11cm")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    for st in ["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]:
        print("\\multicolumn{8}{|c|}{$st$ = " + st_names_dict[st] + "} \\\\ \\hline")
        print("       & RNG & GG & GPA & 5NN & YAO & ER & Total\\\\ \\hline")
        line_high = "Damage SA > Damage LA "
        line_mid = "Damage SA $\sim$ Damage LA "
        line_low = "Damage SA < Damage LA "
        total = 103000
        all_upper = 0
        all_mid = 0
        all_lower = 0
        for model in models:
            upper, mid, lower, lower_gl_delta, higher_gl_delta = dp.compare_seismic_attacks_with_localized_attacks(model, imax, strategy=st, lv=1)
            line_high += "& {}\\% ".format(round(100 * upper / total, 1))
            line_mid += "& {}\\% ".format(round(100 * mid / total, 1))
            line_low += "& {}\\% ".format(round(100 * lower / total, 1))
            all_upper += upper
            all_mid += mid
            all_lower += lower
        line_high += "& {}\\% \\\\ \\hline".format(round(100 * all_upper / (total * len(models)), 1))
        line_mid += "& {}\\% \\\\ \\hline".format(round(100 * all_mid / (total * len(models)), 1))
        line_low += "& {}\\% \\\\ \\hline".format(round(100 * all_lower / (total * len(models)), 1))
        print(line_high)
        print(line_mid)
        print(line_low)

    print("\\end{tabular}")

    print("\\caption[Comparison between localized attacks and seismic attacks after adding extra physical links ($I_{max}=" + str(imax) + "$)]{Comparison between localized attacks and seismic "
                                                                                                                                          "attacks for systems with extra physical links added, "
                                                                                                                                          "and $I_{max}=" + str(imax) + "$.}")

    print("\\label{tab:sa-la-comparison-imax-" + str(imax) + "}")
    print("\\end{table}")


def make_supplementary_images(chapter_number, save_fig=True, auto_save=False):
    interlink_type = "provider_priority"
    interlink_version = 3
    versions = list(range(1, 11))
    for logic_net_version in versions:
        for space in [(20, 500), (100, 100)]:
            for physical_model in ["RNG", "GG", "5NN", "GPA", "YAO", "ER"]:
                if chapter_number == 3:
                    strategy = "simple graphs"
                    cp.show_averages_for_all_imax(logic_net_version, interlink_type, interlink_version, physical_model, space, strategy, m_results=False,
                                                      save_to="supplementary/cap{}".format(chapter_number), save_fig=save_fig, autoclose=auto_save)
                elif chapter_number == 5:
                    if logic_net_version > 1:
                        return
                    for strategy in ["distance_aux", "local_hubs", "degree_aux", "random"]:
                        cp.show_averages_for_all_imax(logic_net_version, interlink_type, interlink_version, physical_model, space, strategy, m_results=False,
                                                          save_to="supplementary/cap{}".format(chapter_number), save_fig=save_fig, autoclose=auto_save, all_imax=[3, 5, 7, 10])


def latex_figures(space, chapter, logic_net_version, strategy):

    print("\\begin{figure}[t!]")
    print("\\centering")
    print("\\makebox[\\linewidth]{")
    print(" \\subfigure[RNG]{")
    physical_model = "RNG"
    fig_name = "lines_{}_lv{}_{}_{}.png".format(physical_model, logic_net_version, strategy.replace(" ", "_"), space)
    print("  \\includegraphics[width = 0.47\\linewidth]{" + "img_cap{}/{}".format(chapter, fig_name) + "}}")
    print(" \\subfigure[GG]{")
    physical_model = "GG"
    fig_name = "lines_{}_lv{}_{}_{}.png".format(physical_model, logic_net_version, strategy.replace(" ", "_"), space)
    print("  \\includegraphics[width = 0.47\\linewidth]{" + "img_cap{}/{}".format(chapter, fig_name) + "}}}")

    print("\\centering")
    print("\\makebox[\\linewidth]{")
    print(" \\subfigure[5NN]{")
    physical_model = "5NN"
    fig_name = "lines_{}_lv{}_{}_{}.png".format(physical_model, logic_net_version, strategy.replace(" ", "_"), space)
    print("  \\includegraphics[width = 0.47\\linewidth]{" + "img_cap{}/{}".format(chapter, fig_name) + "}}")
    print(" \\subfigure[YAO]{")
    physical_model = "YAO"
    fig_name = "lines_{}_lv{}_{}_{}.png".format(physical_model, logic_net_version, strategy.replace(" ", "_"), space)
    print("  \\includegraphics[width = 0.47\\linewidth]{" + "img_cap{}/{}".format(chapter, fig_name) + "}}}")

    print("\\centering")
    print("\\makebox[\\linewidth]{")
    print(" \\subfigure[GPA]{")
    physical_model = "GPA"
    fig_name = "lines_{}_lv{}_{}_{}.png".format(physical_model, logic_net_version, strategy.replace(" ", "_"), space)
    print("  \\includegraphics[width = 0.47\\linewidth]{" + "img_cap{}/{}".format(chapter, fig_name) + "}}")
    print(" \\subfigure[ER]{")
    physical_model = "ER"
    fig_name = "lines_{}_lv{}_{}_{}.png".format(physical_model, logic_net_version, strategy.replace(" ", "_"), space)
    print("  \\includegraphics[width = 0.47\\linewidth]{" + "img_cap{}/{}".format(chapter, fig_name) + "}}}")

    s = {"ln": "(1:25)", "sq": "(1:1)"}
    st = {"distance_aux": "Distance", "local_hubs": "Local hubs", "degree_aux": "Degree", "random": "Random"}
    if strategy == "simple graphs":
        short_caption = "Average robustness $s=\\text{" + s[space] + "}, q=" + str(logic_net_version) + "$"
        long_caption = "Average robustness by model for systems built over a {} space, and logical network version {}.".format(s[space], logic_net_version)
        label = "fig:line_lv{}_{}".format(logic_net_version, space)
    else:
        short_caption = "Average robustness $s=\\text{" + s[space] + "}, q=" + str(logic_net_version) + ", st=\\text{" + st[strategy] + "}$"
        long_caption = "Average robustness by model for systems built over a {} space, and logical network version {} after adding extra physical links according to {} strategy.".format(
            s[space], logic_net_version, st[strategy])
        label = "fig:line_lv{}_{}_{}".format(logic_net_version, space, st[strategy])
    print("\\caption[" + short_caption + "]{" + long_caption + "}")
    print("\\label{" + label + "}")
    print("\\end{figure}")


def get_all_supplementary_latex_for_cap3():
    for space in ["ln", "sq"]:
        for lv in range(1, 11):
            latex_figures(space, "3", lv, "simple graphs")


def get_all_supplementary_latex_for_cap5():
    for strategy in ["distance_aux", "local_hubs", "degree_aux", "random"]:
        for space in ["ln", "sq"]:
            latex_figures(space, "5", "1", strategy)


def get_delta_gl_vs_cost_cap5(save_fig=True):
    spaces = [(20, 500), (100, 100)]
    ndeps = [3, 5, 7, 10]
    for space in spaces:
        for ndep in ndeps:
            cp.show_delta_tgl_vs_cost(space, ndep=ndep, models=["RNG", "GG", "5NN"], img_ver=1, save_figure=save_fig)
            cp.show_delta_tgl_vs_cost(space, ndep=ndep, models=["GPA", "YAO", "ER"], img_ver=2, save_figure=save_fig)

# con esto puedo armar tablas de U_q
#cp.show_imaxes_as_lines_with_error_tgl(1, "provider_priority", ppv, (20, 500), "simple graphs", m_results=False, save_fig=False, check_u_q=True, write_table=False, prefix="", show=False)
#generate_u_q_table_cap3()