import data_proc.common_plots as cp
import data_proc.plotting as pt
import data_proc.LA_vs_RA_plots as vs
import sys


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


def get_boxplots_cap_3(save_figure=True):
    for model in ["RNG", "GG", "5NN", "YAO", "GPA", "ER"]:
        for ndep in range(1, 11):
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


def m():
    st = ["local_hubs"]
    for model in ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]:
        print("Using ndep: {}, for st: {}".format(5, st))
        pre_process_LA_scatter_data(model, ndep=5, strategy=st)
        print("Using ndep: {}, for st: {}".format(7, st))
        pre_process_LA_scatter_data(model, ndep=7, strategy=st)
        print("Using ndep: {}, for st: {}".format(10, st))
        pre_process_LA_scatter_data(model, ndep=10, strategy=st)


if len(sys.argv) < 3:
    exit("Argv error")
model = sys.argv[1]
strategy = sys.argv[2]
if strategy == "simple_graphs":
    strategy = "simple graphs"

pre_process_seismic_scatter_data(model, ndep=3, strategy=[strategy])#"distance_aux", "local_hubs", , "random", "simple graphs"


#get_scatter_plot_find_cap_6(save_figure=True, imax=5, strategies=["distance_aux", "local_hubs", "degree_aux", "random"])
#get_scatter_plot_find_cap_6(save_figure=True, imax=7, strategies=["distance_aux", "local_hubs", "degree_aux", "random"])
#get_scatter_plot_find_cap_6(save_figure=True, imax=10, strategies=["distance_aux", "local_hubs", "degree_aux", "random"])