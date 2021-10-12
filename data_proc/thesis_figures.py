import os
import sys
sys.path.append(os.getcwd())
import data_proc.common_plots as cp
import data_proc.plotting as pt
import data_proc.LA_vs_RA_plots as vs
import data_proc.data_processing as dp
#import common_plots as cp
#import plotting as pt
#import LA_vs_RA_plots as vs



ppv = 3


def pre_process_LA_scatter_data(model, ndep=3, strategy=["distance_aux", "local_hubs", "degree_aux", "random", "simple graphs"]):
    geometry = ["20x500", "100x100"]
    for g in geometry:
        for st in strategy:
            pt.write_stuff(g, st, use_model=[model], ndep=ndep)


def pre_process_seismic_scatter_data(model, ndep=3, strategy=["distance_aux", "local_hubs", "degree_aux", "random", "simple graphs"]):
    geometry = ["20x500"]
    for g in geometry:
        for st in strategy:
            pt.write_stuff(g, st, use_model=[model], ndep=ndep, is_seismic=True)


def get_bars_cap_3(save_figure=True):
    for imax in range(1, 11):
        cp.show_curves_as_bar_and_error_by_model_double_plot("provider_priority", ppv, imax, "simple graphs", m_results=False, save_fig=save_figure)


def get_imax_lines_cap_3(save_figure=True, check_u_q=False):
    for lv in range(1, 11):
        cp.show_imaxes_as_lines_with_error_tgl(lv, "provider_priority", ppv, (20, 500), "simple graphs", m_results=False, save_fig=save_figure, check_u_q=check_u_q)


def get_boxplots_cap_3(save_figure=True, ndeps=list(range(1, 11))):
    for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
        for ndep in ndeps:
            cp.show_curves_as_points_by_space("provider_priority", ppv, model, "simple graphs", ndep, m_results=False, save_fig=save_figure)


def get_imax_lines_cap_4(save_figure=True, check_u_q=False):
    for lv in range(1, 11):
        cp.show_imaxes_as_lines_with_error_tgl(lv, "provider_priority", ppv, (20, 500), "simple graphs", m_results=[False, True], save_fig=save_figure, check_u_q=check_u_q)


def get_boxplots_cap_5(save_figure=True):
    for sp in [(20, 500), (100, 100)]:
        for imax in [3, 5, 7, 10]:
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="distance_aux", space=sp, save_fig=save_figure)
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="local_hubs", space=sp, save_fig=save_figure)
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="degree_aux", space=sp, save_fig=save_figure)
            cp.show_curves_as_points_by_space("provider_priority", ppv, "", "simple graphs", imax, strategy_2="random", space=sp, save_fig=save_figure)


def get_curves_cap_5(save_figure=True, debug=False, lv=1):
    for imax in [3, 5, 7, 10]:
        for sp in [(20, 500), (100, 100)]:
            for model in ["RNG", "GPA", "GG", "5NN", "YAO", "ER"]:
                cp.gl_compare_strategies(lv, sp, model, imax, debug=debug, save_fig=save_figure)


def get_double_curves_st_comp_cap5(save_figure=True, lv=1):
    for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
        cp.show_imaxes_as_lines_with_error_tgl(lv, "provider_priority", ppv, (20, 500), "", save_fig=save_figure, strategies_comp=model)
        cp.show_imaxes_as_lines_with_error_tgl(1, "provider_priority", ppv, (20, 500), "", save_fig=save_figure, strategies_comp=model, name_mod='1250')

   
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


def get_scatter_plot_find_cap_6(save_figure=True, imax=3, strategies=["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]):
    geometries = ["20x500", "100x100"]
    radius = 20
    for s in geometries:
        for st in strategies:
            pt.scatter_plot(["5NN", "GG", "RNG", "GPA", "YAO", "ER"], s, st, imax, radius, map="find", legacy=False, save_fig=save_figure)


def get_hdla_tables(imax):
    number_of_hdla = {}
    hdla_range = {}
    strategies = ["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]
    st_name = {"simple graphs": "Original", "distance_aux": "Distance", "local_hubs": "Local hubs", "degree_aux": "Degree", "random": "Random"}
    radius = 20
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
    print("\\begin{table}[]")
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
                    line += "& ({},{}) ".format(round(min(hdla_range[s][st][this_range]), 3), round(max(hdla_range[s][st][this_range]), 3))
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
    print("\\caption{$G_L$ ranges of HDLA, and LA minus HDLA (Non-HDLA) of systems with and without physical links added for $I_{max}=" + str(imax) + "$, and $a=1$.}")
    print("\\label{tab:LA-ranges-imax-" + str(imax) + "}")
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
    print("\\begin{table}[]")
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

    print("\\caption{Summary table for simple attacks ($I_{max}=" + str(imax) + "$).}")

    print("\\label{tab:seismic-summary-imax-" + str(imax) + "}")
    print("\\end{table}")


def la_sa_comparison_scatter_cap_7(save_fig=True, sclose=False, st="simple graphs"):
    for imax in [3, 5, 7, 10]:
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
    print("\\begin{table}[]")
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

    print("\\hline")
    print("\\end{tabular}")

    print("\\caption{Comparison between localized attacks and seismic attacks ($I_{max}=" + str(imax) + "$).}")

    print("\\label{tab:sa-la-comparison-imax-" + str(imax) + "}")
    print("\\end{table}")


#get_double_curves_st_comp_cap5(save_figure=True, lv=1)

