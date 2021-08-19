import data_proc.data_processing as dp
import data_proc.plotting as pt
#import data_processing as dp
#import plotting as pt
import numpy as np


def plot_la_ra_difference_for_strategy(strategy, ndep, models, ylim=[0.88,1], is_legacy=False, lv=1):
    title = "Localized Attacks (LA) vs Random Attacks (RA)"
    if strategy != "simple graphs":
        title += "\nwith {} link addition".format(strategy)

    lines_ln, x = dp.get_LA_RA_lineplot_info_for_damage_comparison([4, 8, 12, 16, 20], models, strategy,
                                                                   "20x500", ndep, legacy=is_legacy, lv=lv)

    lines_sq, x = dp.get_LA_RA_lineplot_info_for_damage_comparison([4, 8, 12, 16, 20], models, strategy
                                                                   , "100x100", ndep, legacy=is_legacy, lv=lv)

    # merge lines but add those under RA first
    dict_lines_ra = {}
    dict_lines_la = {}
    for key in lines_ln.keys():
        if key.find("RA") > -1:
            dict_lines_ra[key] = lines_ln[key]
        else:
            dict_lines_la[key] = lines_ln[key]
    for key in lines_sq.keys():
        if key.find("RA") > -1:
            dict_lines_ra[key] = lines_sq[key]
        else:
            dict_lines_la[key] = lines_sq[key]
    dict_lines = {}
    for key in dict_lines_ra.keys():
        dict_lines[key] = dict_lines_ra[key]
    for key in dict_lines_la.keys():
        dict_lines[key] = dict_lines_la[key]

    x = [0.2, 0.4, 0.6, 0.8, 1]
    dict_lines_ln = {}
    dict_lines_sq = {}

    i = 0
    for k in dict_lines.keys():
        if i % 6 < 3:
            dict_lines_ln[k] = dict_lines[k]
        else:
            dict_lines_sq[k] = dict_lines[k]
        i += 1

    pt.n_line_plot(dict_lines, x, title, double_pair_color=True, xlim=[0.19, 1.01], ylim=ylim, xlabel=r'$a$',
                   line_size=[1,1,1,1,1,1,1,1,1,1,1,1], marker_size=[1,1,1,1,1,1,1,1,1,1,1,1]*1)
    #pt.n_line_plot(dict_lines_sq, x, title, double_pair_color=True, xlim=[0.19, 1.01], ylim=ylim, xlabel=r'$a$')

#plot_la_ra_difference_for_strategy("random", 3, is_legacy=True, ylim=[0.85, 1])
#plot_la_ra_difference_for_strategy("degree",3, ylim=[0.89,1])
#plot_la_ra_difference_for_strategy("random",3, ylim=[0.92,1])
#plot_la_ra_difference_for_strategy("distance",3, ylim=[0.92,1])


def data_for_MRN_distance_GG_table_LA(radius_list, ndep):
    vs = [1,2,3,4,5,6,7,8,9,10]
    geometry = "20x500"
    first_row = ["$r$","RNG","GG", "RNG + distance", "RNG + random"]
    data = []
    for r in radius_list:
        current_row = []
        current_row.append(str(r))
        mrn = dp.get_average_gl_for_localized_attacks("RNG", geometry, "simple graphs", ndep, vs, r)
        current_row.append("{} ({})".format(np.round(mrn[0], decimals=3),np.round(mrn[1], decimals=3)))
        gg = dp.get_average_gl_for_localized_attacks("GG", geometry, "simple graphs", ndep, vs, r)
        current_row.append("{} ({})".format(np.round(gg[0], decimals=3), np.round(gg[1], decimals=3)))
        mrn_dist = dp.get_average_gl_for_localized_attacks("RNG", geometry, "distance", ndep, vs, r)
        current_row.append("{} ({})".format(np.round(mrn_dist[0], decimals=3), np.round(mrn_dist[1], decimals=3)))
        mrn_rand = dp.get_average_gl_for_localized_attacks("RNG", geometry, "random", ndep, vs, r)
        current_row.append("{} ({})".format(np.round(mrn_rand[0], decimals=3), np.round(mrn_rand[1], decimals=3)))
        data.append(current_row)

    a = dp.generate_latex_table_with(first_row,data,caption="$G_L$ comparison of RNG and GG under LA.",label="tab:MRNdistance-GG-LA")
    print(a)


# data_for_MRN_distance_GG_table_LA([2,4,6,8,10,20],3)

def get_cost_efficiency(strategy, geometry, model, legacy=False, imax=3):
    costs = {(20, 500): {"RNG": {"random": 107199.24, "degree_aux": 108260.99,
                                 "distance": 5053.18, "distance_aux": 1345.94},
                         "GG": {"random": 109240.11, "degree_aux": 106637.27,
                                "distance": 5348.77, "distance_aux": 1450.28},
                         "5NN": {"random": 106967.22, "degree_aux": 107967.13,
                                 "distance_aux": 1574.63, "distance": 5525.47}},
             (100, 100): {"RNG": {"random": 33225.15, "degree_aux": 33474.73,
                                  "distance": 4830.97, "distance_aux": 1295.18},
                          "GG": {"random": 33467.1, "degree_aux": 34003.937,
                                 "distance": 5230.64, "distance_aux": 1450.28},
                          "5NN": {"random": 33466.26, "degree_aux": 33613.86,
                                  "distance": 5260.35, "distance_aux": 1530.73}}}
    all_data = dp.run_data()
    # Base data
    average_data_paths = all_data["average_results_path"]
    data_types = all_data["strategies"]
    # Graph parameters
    exp = all_data["exp"]
    attack = all_data["attack"]
    amount_of_physical_nodes = 2000
    systems = all_data["models"]
    versions = all_data["versions"]
    all_delta_gl = []
    if type(geometry) is tuple:
        gname = dp.tuple_to_gname(geometry)
    else:
        gname = geometry
    data = dp.get_all_data_for("", gname, exp, imax, attack, model, strategies_paths=average_data_paths, legacy=legacy)
    strategy_data = data[strategy]
    base_data = data["simple graphs"]
    for i in range(len(strategy_data)):
        delta_gl = strategy_data[i] - base_data[i]
        all_delta_gl.append(delta_gl)

    avg_delta_gl = np.sum(all_delta_gl) * 1000
    efficiency = avg_delta_gl / costs[geometry][model][strategy]
    print("Efficiency {} {} {}: {}".format(model, geometry, strategy, efficiency))


def aux_main():
    geometries = [(20, 500), (100, 100)]
    strategies = ["distance_aux", "distance", "degree_aux", "random"]
    models = ["RNG", "GG", "5NN"]
    for model in models:
        for geometry in geometries:
            for strategy in strategies:

                get_cost_efficiency(strategy, geometry, model, legacy=True)


def plot_la_ra_delta_for_strategy(strategy, ndep, models, is_legacy=False, lv=1, save_fig=False):
    title = "Localized Attacks (LA) vs Random Attacks (RA)"
    if strategy != "simple graphs":
        title += "\nwith {} link addition".format(strategy)

    lines_ln, x = dp.get_LA_RA_lineplot_info_for_damage_comparison([4, 8, 12, 16, 20], models, strategy,
                                                                   "20x500", ndep, legacy=is_legacy, lv=lv)

    lines_sq, x = dp.get_LA_RA_lineplot_info_for_damage_comparison([4, 8, 12, 16, 20], models, strategy
                                                                   , "100x100", ndep, legacy=is_legacy, lv=lv)

    # merge lines but add those under RA first
    dict_lines_ra_ln = {}
    dict_lines_la_ln = {}
    dict_lines_delta_ln = {}

    dict_lines_ra_sq = {}
    dict_lines_la_sq = {}
    dict_lines_delta_sq = {}

    max_delta = 0
    min_delta = 1

    print("(1:25)")
    for key in lines_ln.keys():
        if key.find("RA") > -1:
            dict_lines_ra_ln[key] = lines_ln[key]
        else:
            dict_lines_la_ln[key] = lines_ln[key]
    for model in models:
        current_delta = []
        current_ra = []
        current_la = []
        for key in dict_lines_la_ln.keys():
            if key.find(model) > -1:
                current_la = dict_lines_la_ln[key]
        for key in dict_lines_ra_ln.keys():
            if key.find(model) > -1:
                current_ra = dict_lines_ra_ln[key]
        for i in range(len(current_ra)):
            delta_value = np.round(current_la[i] - current_ra[i], 4)
            current_delta.append(delta_value)
            if delta_value > max_delta:
                max_delta = delta_value
            if delta_value < min_delta:
                min_delta = delta_value
        new_key = "{} (1:25)".format(model)
        dict_lines_delta_ln[new_key] = current_delta
        print(new_key)
        print(dict_lines_delta_ln[new_key])

    print("(1:1)")
    for key in lines_sq.keys():
        if key.find("RA") > -1:
            dict_lines_ra_sq[key] = lines_sq[key]
        else:
            dict_lines_la_sq[key] = lines_sq[key]
    for model in models:
        current_delta = []
        current_ra = []
        current_la = []
        for key in dict_lines_la_sq.keys():
            if key.find(model) > -1:
                current_la = dict_lines_la_sq[key]
        for key in dict_lines_ra_sq.keys():
            if key.find(model) > -1:
                current_ra = dict_lines_ra_sq[key]
        for i in range(len(current_ra)):
            delta_value = np.round(current_la[i] - current_ra[i], 4)
            current_delta.append(delta_value)
            if delta_value > max_delta:
                max_delta = delta_value
            if delta_value < min_delta:
                min_delta = delta_value
        new_key = "{} (1:1)".format(model)
        dict_lines_delta_sq[new_key] = current_delta
        print(new_key)
        print(dict_lines_delta_sq[new_key])

    if save_fig:
        fig_path = '../figures/cap6/cap6_LAvsRA_st_{}_ndep_{}.png'.format(strategy.replace(" ", "_"), ndep)
    else:
        fig_path = None

    x_axis = [0.2, 0.4, 0.6, 0.8, 1]
    pt.double_ax_plot_line(dict_lines_delta_sq, dict_lines_delta_ln, x_axis,
                           x_label=r'$a$',
                           y_label=r'$\Delta\overline{G}_L$',
                           colors=['#7aa711', '#807dba', '#ec7014', '#dd3497', '#6baed6', '#B99D22'],
                           ylim=[-0.015, 0.13],
                           xlim=[0.18, 1.05],
                           line_styles=[],
                           linewidths=[1, 1, 1, 1, 1, 1],
                           markers=['o'],
                           marker_size=[5, 5, 5, 5, 5, 5],
                           lv=1,
                           save_fig_to=fig_path,
                           add_zero_line=True,
                           imax=ndep)


def test():
    models = ['RNG','GPA', 'GG', '5NN', 'YAO', 'ER']
    for ndep in [3, 5, 7, 10]:
        plot_la_ra_delta_for_strategy("simple graphs", ndep, models, is_legacy=False, lv=1, save_fig=True)
        plot_la_ra_delta_for_strategy("distance_aux", ndep, models, is_legacy=False, lv=1, save_fig=True)
        plot_la_ra_delta_for_strategy("local_hubs", ndep, models, is_legacy=False, lv=1, save_fig=True)
        plot_la_ra_delta_for_strategy("degree_aux", ndep, models, is_legacy=False, lv=1, save_fig=True)
        plot_la_ra_delta_for_strategy("random", ndep, models, is_legacy=False, lv=1, save_fig=True)

    #plot_la_ra_difference_for_strategy("simple graphs", 3, ['RNG', 'GPA'], ylim=[0.8, 1], is_legacy=False, lv=1)

