import data_proc.data_processing as dp
import data_proc.plotting as plot
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import os
import csv
import seaborn as sns
import pandas as pd
import math


USE_INTERNAL = False


def show_plot(show_network,
              geometry_type,
              show_imax=None,
              data_type=None,
              get_damage_at_x_percent=False,
              show_all_data_for_imax=False,
              show_all_data_for_model=False,
              shape_comparison=False,
              all_shape_comparison=False,
              generate_average_files=False,
              show_all_strategies_for_imax_and_network=False,
              damage_fraction=1,
              legacy=False):

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

    model_colors = {"RNG": {"light": '#7aa711', "dark": '#006837', "st": '#556a4d'},
                    "GG": {"light": '#ec7014', "dark": '#cc4c02', "st": '#695442'},
                    "5NN": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'}}

    if type(geometry_type) is tuple:
        gname = dp.tuple_to_gname(geometry_type)
    else:
        gname = geometry_type
    # Get average data if asked for
    if get_damage_at_x_percent:
        damage = {}

        for system_name in systems:
            for dtype in data_types:
                average_data_path = average_data_paths[dtype]

                if get_damage_at_x_percent:
                    damage[system_name] = dp.data_at_x_percent_damage(damage_fraction, amount_of_physical_nodes,
                                                                      average_data_path, gname, exp, attack,
                                                                      system_name)

    # Data to show all the damage
    if show_all_data_for_imax:
        shape = ""
        if gname == "100x100":
            shape = "(1:1)"
        elif gname == "20x500":
            shape = "(1:25)"

        average_data_path = average_data_paths["simple graphs"]
        data = dp.get_all_data_for(average_data_path, gname, exp, show_imax, attack, systems, legacy=legacy)

        lines = {"RNG {}".format(shape): data["RNG"],
                 "GG {}".format(shape): data["GG"],
                 "5NN {}".format(shape): data["5NN"]}
        title = 'Average results for {}, {} = {} '.format(data_type, r'$I_{max}$', str(show_imax))
        plot.n_line_plot(lines, data["x_axis"], title)

    # Data to show the damage at a specific percentage of nodes removed
    if get_damage_at_x_percent:
        plot.three_line_plot(damage["RNG"]["y_axis"], damage["GG"]["y_axis"], damage["5NN"]["y_axis"],
                             damage["RNG"]["x_axis"], damage_fraction * 100)

    # Data to show strategies side by side
    if show_all_strategies_for_imax_and_network:
        shape = ""
        c_mode = ""
        if gname == "100x100":
            shape = "(1:1)"
            c_mode = "light"
        elif gname == "20x500":
            shape = "(1:25)"
            c_mode = "dark"

        data = dp.get_all_data_for("", gname, exp, show_imax, attack, show_network, strategies_paths=average_data_paths,
                                   legacy=legacy)
        data_0 = dp.get_all_data_for("", "100x100", exp, show_imax, attack, show_network, strategies_paths=average_data_paths,
                                   legacy=legacy)

        data2 = dp.get_all_data_for("", gname, exp, show_imax, attack, "GG", strategies_paths=average_data_paths,
                                    legacy=legacy)
        data3 = dp.get_all_data_for("", gname, exp, show_imax, attack, "5NN", strategies_paths=average_data_paths,
                                    legacy=legacy)
        show_mod_random = True

        if show_mod_random:
            lines = {#"simple {} {}".format(show_network, shape): data["simple graphs"],
                     #"simple {} {}".format(show_network, "(1:1)"): data_0["simple graphs"],
                     #"simple {} {}".format("GG-", shape): data2["simple graphs"],
                     #"simple {} {}".format("5NN-", shape): data3["simple graphs"],
                     #"{} {} + distance".format(show_network, shape): data["distance_aux"],
                     #"{} {} + random-dist".format(show_network, shape): data["random_distance"],
                     "{} {} + random 0.01".format(show_network, shape): data["random_cap0.01"],
                     "{} {} + random 0.05".format(show_network, shape): data["random_cap0.05"],
                     #"{} {} + random 0.15".format(show_network, shape): data["random_cap0.15"],
                     "{} {} + random 0.25".format(show_network, shape): data["random_cap0.25"],
                     #"{} {} + random 0.5".format(show_network, shape): data["random_cap0.5"],
                     #"{} {} + random 0.75".format(show_network, shape): data["random_cap0.75"],
                     "{} {} + random".format(show_network, shape): data["random"]}
            color_list = [#model_colors[show_network][c_mode],
                          # model_colors[show_network]["light"],
                          # model_colors["GG"][c_mode],
                          # model_colors["5NN"][c_mode],
                          model_colors[show_network]["st"],
                          model_colors[show_network]["st"],
                          #model_colors[show_network]["st"],model_colors[show_network]["st"], model_colors[show_network]["st"],
                          model_colors[show_network]["st"], model_colors[show_network]["st"]]
            # '#9b56c2','#9b56c2','#9b56c2','#9b56c2']
            # '#4681a0','#4681a0','#4681a0','#4681a0']
            # '#d8b846','#d8b846','#d8b846','#d8b846']
            # '#4e4cae','#4e4cae','#4e4cae','#4e4cae']
            mark_size = [#0,
                         # 0,
                         # 0,
                         8.5,8.5,
                         8.5,
                         13, 8,
                         8, 8]
            markers = [#"",
                       # "",
                       # "",
                       "^","+",
                       "v",
                       "*", "x",
                       "s", "o"]
            l_width = [#2,
                       # 2,
                       # 2,
                       0.7,0.7,
                       0.7,
                       0.7, 0.7, 0.7, 0.7]
        else:
            lines = {"simple {} {}".format(show_network, shape): data["simple graphs"],
                     # "simple {} {}".format(show_network, "(1:1)"): data_0["simple graphs"],
                     # "simple {} {}".format("GG-", shape): data2["simple graphs"],
                     # "simple {} {}".format("5NN-", shape): data3["simple graphs"],
                     "{} {} + distance".format(show_network, shape): data["distance_aux"],
                     "{} {} + random-dist".format(show_network, shape): data["random_distance"],
                     "{} {} + hubs".format(show_network, shape): data["local_hubs"],
                     "{} {} + random-hubs".format(show_network, shape): data["random_local_hubs"],
                     "{} {} + degree".format(show_network, shape): data["degree_aux"],
                     "{} {} + random".format(show_network, shape): data["random"]}
            color_list = [model_colors[show_network][c_mode],
                          # model_colors[show_network]["light"],
                          # model_colors["GG"][c_mode],
                          # model_colors["5NN"][c_mode],
                          model_colors[show_network]["st"], model_colors[show_network]["st"],
                          model_colors[show_network]["st"], model_colors[show_network]["st"],
                          model_colors[show_network]["st"], model_colors[show_network]["st"]]
            # '#9b56c2','#9b56c2','#9b56c2','#9b56c2']
            # '#4681a0','#4681a0','#4681a0','#4681a0']
            # '#d8b846','#d8b846','#d8b846','#d8b846']
            # '#4e4cae','#4e4cae','#4e4cae','#4e4cae']
            mark_size = [0,
                         # 0,
                         # 0,
                         8.5, 8.5,
                         13, 8,
                         8, 8]
            markers = ["",
                       # "",
                       # "",
                       "^", "v",
                       "*", "x",
                       "s", "o"]
            l_width = [2,
                       # 2,
                       # 2,
                       0.7, 0.7, 0.7, 0.7, 0.7, 0.7]


        title = 'Average results for {} = {} '.format(r'$I_{max}$', str(show_imax))


        plot.n_line_plot(lines, data["x_axis"], title, c_list=color_list, markers=markers, marker_size=mark_size,
                         line_size=l_width)

    if show_all_data_for_model:
        shape = ""
        if gname == "100x100":
            shape = "(1:1)"
        elif gname == "20x500":
            shape = "(1:25)"
        imax_list = dp.get_imax_tested()
        lines = {}
        for imax in imax_list:
            data = dp.get_all_data_for("", gname, exp, imax, attack, show_network, average_data_paths, legacy=legacy)
            line_name = "{} = {}".format(r'$I_{max}$', imax)
            lines[line_name] = data[data_type]

            if data_type == "random":
                add_name = "Random link addition"
            elif data_type == "degree_aux":
                add_name = "Degree link addition"
            elif data_type == "distance":
                add_name = "Hubs link addition"
            elif data_type == "distance_aux":
                add_name = "Distance link addition"
            else:
                add_name = "no addition"

        title = "{} {} robustness for all {} tested ({})".format(show_network,shape,r'$I_{max}$', add_name)
        plot.n_line_plot(lines, data["x_axis"], title)

    if shape_comparison:
        data = dp.get_all_data_for("", "20x500", exp, show_imax, attack, show_network, average_data_paths, legacy=legacy)

        data2 = dp.get_all_data_for("", "100x100", exp, show_imax, attack, show_network, average_data_paths, legacy=legacy)

        lines = {"simple {} (1:25)".format(show_network): data["simple graphs"],
                 #"simple {} (1:1)".format(show_network): data2["simple graphs"],
                 "{} + Distance (1:25)".format(show_network): data["distance_aux"],
                 "{} + Hubs (1:25)".format(show_network): data["distance"],
                 "{} + Degree (1:25)".format(show_network): data["degree_aux"],
                 "{} + Random (1:25)".format(show_network): data["random"]}

        color_list = [model_colors[show_network]["dark"],# model_colors[show_network]["light"],
                      model_colors[show_network]["st"], model_colors[show_network]["st"],
                      model_colors[show_network]["st"], model_colors[show_network]["st"]]
                      #'#ae1fff',
                      #'#2b8cbe',
                      #'#fec806',
                      #'#bd0026']

        liness = {"simple {} (1:1)".format(show_network): data2["simple graphs"],
                 # "simple {} (1:1)".format(show_network): data2["simple graphs"],
                 "{} + Random (1:1)".format(show_network): data2["random"],
                 "{} + Degree (1:1)".format(show_network): data2["degree"],
                 "{} + Distance (1:1)".format(show_network): data2["distance"]}
        title = 'Average results for {} = {} '.format(r'$I_{max}$', str(show_imax))
        mark_size = [0, 0, 5, 8, 5, 5]
        markers = ["", "", "^", "*", "s", "o"]
        l_width = [1.8, 1.8, 0.7, 0.7, 0.7, 0.7]
        plot.n_line_plot(lines, data["x_axis"], title, c_list=color_list, markers=markers, marker_size=mark_size,
                         line_size=l_width)

    if all_shape_comparison:
        data_dict_1 = {}
        data_dict_2 = {}
        lines = {}
        data = dp.get_all_data_for("", "20x500", exp, show_imax, attack, "RNG", average_data_paths, legacy=legacy)
        for network in ["RNG", "GG", "5NN"]:
            data_dict_1[network] = dp.get_all_data_for("", "20x500", exp, show_imax, attack, network,
                                                       average_data_paths, legacy=legacy)
            data_dict_2[network] = dp.get_all_data_for("", "100x100", exp, show_imax, attack, network,
                                                       average_data_paths, legacy=legacy)
            lines["{} (1:25)".format(network)] = data_dict_1[network]["simple graphs"]
            lines["{} (1:1)".format(network)] = data_dict_2[network]["simple graphs"]
        title = 'Average results for {} = {} '.format(r'$I_{max}$', str(show_imax))

        plot.n_line_plot(lines, data["x_axis"], title, color_pairs=True)


def generate_all_averages(geometry_type, lv=1, system=None, ndep=None, legacy=False, debug=False, data_path=None, st=None):
    all_data = dp.run_data()
    # Base data
    data_paths = all_data["results_paths"]
    all_data = dp.run_data()
    exp = all_data["exp"]
    attack = all_data["attack"]
    systems = ['RNG', 'GG', '5NN']#, 'YAO', 'ER', 'GPA']#all_data["models"]
    versions = all_data["versions"]
    average_data_paths = all_data["average_results_path"]
    data_types = ['simple graphs']#, 'random', 'distance', 'distance_aux', 'degree_aux']#all_data["strategies"]

    imaxs = dp.get_imax_tested()

    if data_path:
        data_paths = {"RA": {st: data_path}}
        avg_path = average_data_paths["random"]
        avg_path = avg_path.replace("/random", "/{}".format(st))
        average_data_paths = {st: avg_path}
        data_types = [st]
    if ndep:
        imaxs = [ndep]
    if system:
        systems = [system]
    if type(geometry_type) is tuple:
        gname = dp.tuple_to_gname(geometry_type)
    else:
        gname = geometry_type
    for imax in imaxs:
        for system_name in systems:
            for dtype in data_types:
                average_data_path = average_data_paths[dtype]
                data_path = data_paths["RA"][dtype]
                dp.create_average_results_file_in(data_path, average_data_path, gname, exp, imax, attack,
                                                  versions, system_name, legacy=legacy, debug=debug)


def compare_legacy_and_debug(system_name, strategy, get_avg=False):
    # get averages
    if get_avg:
        generate_all_averages((100, 100), system=system_name, ndep=3, legacy=True, debug=True)
        generate_all_averages((20, 500), system=system_name, ndep=3, legacy=True, debug=True)
    # get graphics
    all_data = dp.run_data()
    attack = all_data["attack"]
    average_data_paths = {strategy: all_data["average_results_path"][strategy]}
    model_colors = {"RNG": {"light": '#7aa711', "dark": '#006837', "st": '#556a4d'},
                    "GG": {"light": '#ec7014', "dark": '#cc4c02', "st": '#695442'},
                    "5NN": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'}}
    color_list = [model_colors[system_name]["dark"], model_colors[system_name]["light"]]
    # show (1:25)
    data_debug = dp.get_all_data_for("", "20x500", 2.5, 3, attack, system_name, average_data_paths,
                                     legacy=True, debug=True)
    data_legacy = dp.get_all_data_for("", "20x500", 2.5, 3, attack, system_name, average_data_paths,
                                      legacy=True, debug=False)
    lines = {"legacy {} (1:25)".format(system_name): data_legacy["simple graphs"],
             "debug {} (1:25)".format(system_name): data_debug["simple graphs"]}

    plot.n_line_plot(lines, data_legacy["x_axis"], "", c_list=color_list)
    # show (1:1)
    data_debug = dp.get_all_data_for("", "100x100", 2.5, 3, attack, system_name, average_data_paths,
                                     legacy=True, debug=True)
    data_legacy = dp.get_all_data_for("", "100x100", 2.5, 3, attack, system_name, average_data_paths,
                                      legacy=True, debug=False)
    lines = {"legacy {} (1:1)".format(system_name): data_legacy["simple graphs"],
             "debug {} (1:1)".format(system_name): data_debug["simple graphs"]}

    plot.n_line_plot(lines, data_legacy["x_axis"], "", c_list=color_list)


def show_each_physical_version(logic_net_version, interlink_type, interlink_version, physical_model, ndep, space,
                               strategy, legacy=False):
    # get all data (10 lines)
    all_data = dp.run_data()
    attack = all_data["attack"]
    exp = all_data["exp"]
    versions = all_data["versions"]
    interlink_type_name = all_data["interlink_types"][interlink_type]
    data_paths = {strategy: all_data["results_paths"]["RA"][strategy]}
    space_name = all_data["file_space_names"][space]
    fig_space_name = all_data["figure_space_names"][space]
    if legacy:
        file_name_1 = "debug_legacy_result_{}_exp_{}_ndep_{}_att_physical_v".format(space_name, exp, ndep)
        file_name_2 = "_m_{}.csv".format(physical_model)
    else:
        file_name_1 = "result_{}v{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v".format(interlink_type_name,
                                                                                  interlink_version, logic_net_version,
                                                                                  space_name, exp, ndep)
        file_name_2 = "_m_{}.csv".format(physical_model)
    file_name = file_name_1 + "{}" + file_name_2

    data = dp.get_all_data_for("", space_name, 2.5, ndep, attack, physical_model, data_paths, recv_file_name=file_name)
    lines = {}
    colors = ['#7aa711', '#ec7014', '#ae017e', '#009179', '#f7c81e', '#8506b8','#000000', '#ff0000', '#0800ff',
              '#158280', '#5c6363', '#8506b8']
    line_width = []
    for v in versions:
        line_name = "{} {} {} v{}".format(physical_model, fig_space_name, strategy,v)
        lines[line_name] = data[strategy][v]
        line_width.append(0.5)

    plot.n_line_plot(lines, data["x_axis"], "ndep {}, lv {}".format(ndep, logic_net_version), c_list=colors, line_size=line_width)


def show_all_models_for_version(version, logic_net_version, interlink_type, interlink_version, physical_models, ndep, space,
                               strategy, legacy=False):
    # get all data (10 lines)
    all_data = dp.run_data()
    attack = all_data["attack"]
    exp = all_data["exp"]
    versions = all_data["versions"]
    interlink_type_name = all_data["interlink_types"][interlink_type]
    data_paths = {strategy: all_data["results_paths"]["RA"][strategy]}
    space_name = all_data["file_space_names"][space]
    fig_space_name = all_data["figure_space_names"][space]
    all_model_data = {}
    lines = {}

    colors = ['#7aa711', '#ec7014', '#ae017e', '#009179', '#f7c81e', '#8506b8']
    line_width = []
    for model in physical_models:
        if legacy:
            file_name_1 = "debug_legacy_result_{}_exp_{}_ndep_{}_att_physical_v".format(space_name, exp, ndep)

        else:
            file_name_1 = "result_{}v{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v".format(interlink_type_name, interlink_version, logic_net_version, space_name, exp, ndep)
        file_name_2 = "_m_{}.csv".format(model)
        file_name = file_name_1 + "{}" + file_name_2
        all_model_data[model] = dp.get_all_data_for("", space_name, 2.5, ndep, attack, model, data_paths, recv_file_name=file_name)
        line_name = "{} {} {} v{}".format(model, fig_space_name, strategy, version)

        lines[line_name] = all_model_data[model][strategy][version]

        line_width.append(0.3)

    plot.n_line_plot(lines, all_model_data[model]["x_axis"], "", c_list=colors, line_size=line_width)


def show_all_logic_versions_for_model_version(version, interlink_type, interlink_version, physical_model, ndep, space, strategy, legacy=False, compare_with=None):
    # get all data (10 lines)
    all_data = dp.run_data()
    attack = all_data["attack"]
    exp = all_data["exp"]
    versions = all_data["versions"]
    interlink_type_name = all_data["interlink_types"][interlink_type]
    data_paths = {strategy: all_data["results_paths"]["RA"][strategy]}
    space_name = all_data["file_space_names"][space]
    fig_space_name = all_data["figure_space_names"][space]
    all_model_data = {}
    lines = {}

    lversions = [2,3,4,5,6,7,8,9,10]
    colors = ['#7aa711', '#ec7014', '#ae017e', '#009179', '#f7c81e', '#8506b8','#000000', '#ff0000', '#0800ff',
              '#158280', '#5c6363', '#8506b8']
    if compare_with:
        all_model_data2 = {}
        title = "compare with"
        colors = []
    else:
        title = "ndep {}".format(ndep)
    line_width = []
    for lv in lversions:
        if lv not in [7]:
            continue
        if legacy:
            file_name_1 = "debug_legacy_result_{}_exp_{}_ndep_{}_att_physical_v".format(space_name, exp, ndep)

        else:
            file_name_1 = "result_{}v{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v".format(interlink_type_name, interlink_version, lv, space_name, exp, ndep)
            if compare_with:
                file_name_1b = "m_result_{}v{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v".format(interlink_type_name, interlink_version, lv, space_name, exp, compare_with)
        file_name_2 = "_m_{}.csv".format(physical_model)
        file_name = file_name_1 + "{}" + file_name_2

        all_model_data[lv] = dp.get_all_data_for("", space_name, 2.5, ndep, attack, physical_model, data_paths,
                                                 recv_file_name=file_name)
        if compare_with:
            file_nameb = file_name_1b + "{}" + file_name_2
            all_model_data2[lv] = dp.get_all_data_for("", space_name, 2.5, compare_with, attack, physical_model,  data_paths, recv_file_name=file_nameb)
            line_name = "{} {}v{} lv{} ndep{} ppv{}".format(physical_model, fig_space_name, version, lv, ndep, interlink_version)
            line_nameb = "m {} {}v{} lv{} ndep{} ppv{}".format(physical_model, fig_space_name, version, lv, compare_with, interlink_version)

            lines[line_name] = all_model_data[lv][strategy][version]
            lines[line_nameb] = all_model_data2[lv][strategy][version]
            line_width.append(0.7)
            line_width.append(0.7)
            colors.append('#000000')
            colors.append('#8506b8')
        else:
            line_name = "{} {}v{} lv{}".format(physical_model, fig_space_name, version, lv)

            lines[line_name] = all_model_data[lv][strategy][version]
            line_width.append(0.7)
        x_axis = all_model_data[lv]["x_axis"]

    plot.n_line_plot(lines, x_axis, title, c_list=colors, line_size=line_width)


def show_average_for_logic_version(logic_net_version, interlink_type, interlink_version, physical_model, ndep, space, strategy, legacy=False, show=True, m_results=False):
    # get all data (10 lines)
    all_data = dp.run_data()
    attack = all_data["attack"]
    exp = all_data["exp"]
    versions = all_data["versions"]
    interlink_type_name = all_data["interlink_types"][interlink_type]
    data_paths = {strategy: all_data["results_paths"]["RA"][strategy]}
    space_name = all_data["file_space_names"][space]
    fig_space_name = all_data["figure_space_names"][space]
    if legacy:
        file_name_1 = "debug_legacy_result_{}_exp_{}_ndep_{}_att_physical_v".format(space_name, exp, ndep)
        file_name_2 = "_m_{}.csv".format(physical_model)
    else:
        file_name_1 = "result_{}v{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v".format(interlink_type_name, interlink_version, logic_net_version, space_name, exp, ndep)
        file_name_2 = "_m_{}.csv".format(physical_model)
    file_name = file_name_1 + "{}" + file_name_2
    if m_results:
        file_name = "m_{}".format(file_name)

    data = dp.get_all_data_for("", space_name, 2.5, ndep, attack, physical_model, data_paths, recv_file_name=file_name)
    lines = {}
    colors = ['#7aa711', '#ec7014', '#ae017e', '#009179', '#f7c81e', '#8506b8','#000000', '#ff0000', '#0800ff',
              '#158280', '#5c6363', '#8506b8']
    line_width = []
    full_gl_values = [[] for i in range(1999)]

    for v in versions:
        this_data = data[strategy][v]
        for i in range(len(data[strategy][v])):
            value = this_data[i]
            full_gl_values[i].append(value)
    average_values = []
    for i in range(len(full_gl_values)):
        average_values.append(np.mean(full_gl_values[i]))

    line_name = "{} {} {} mean".format(physical_model, fig_space_name, strategy)
    lines[line_name] = average_values
    line_width.append(0.5)
    if show:
        plot.n_line_plot(lines, data["x_axis"], "ndep {}, lv {}".format(ndep, logic_net_version), c_list=colors, line_size=line_width)
    return data["x_axis"], lines


def show_averages_for_all_imax(logic_net_version, interlink_type, interlink_version, physical_model, space, strategy, m_results=False):
    all_data = dp.run_data()
    space_name = all_data["file_space_names"][space]
    all_lines = {}
    all_imax = list(range(1, 11))
    spaces = [space]
    #all_imax.remove(7)
    colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']
    for ndep in all_imax:
        for space in spaces:
            space_name = all_data["file_space_names"][space]
            x_axis, lines = show_average_for_logic_version(logic_net_version, interlink_type, interlink_version, physical_model, ndep, space, strategy, show=False, m_results=m_results)
            for line_name in lines.keys():
                all_lines["imax {} {}".format(ndep, space)] = lines[line_name]
    plot.n_line_plot(all_lines, x_axis, "All imax, {} {} lv {}".format(physical_model, space_name, logic_net_version), c_list=colors)


def get_curves_as_points(logic_net_version, interlink_type, interlink_version, physical_model, ndep, space, strategy, legacy=False, m_results=False, add_to_title=""):
    # get all data (10 lines)
    all_data = dp.run_data()
    attack = all_data["attack"]
    exp = all_data["exp"]
    versions = all_data["versions"]
    interlink_type_name = all_data["interlink_types"][interlink_type]
    data_paths = {strategy: all_data["results_paths"]["RA"][strategy]}
    space_name = all_data["file_space_names"][space]
    if legacy:
        file_name_1 = "legacy_result_{}_exp_{}_ndep_{}_att_physical_v".format(space_name, exp, ndep)
        file_name_2 = "_m_{}.csv".format(physical_model)
    else:
        file_name_1 = "{}result_{}v{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v".format(add_to_title, interlink_type_name, interlink_version, logic_net_version, space_name, exp, ndep)
        file_name_2 = "_m_{}.csv".format(physical_model)
    file_name = file_name_1 + "{}" + file_name_2
    if m_results:
        file_name = "m_{}".format(file_name)

    data = dp.get_all_data_for("", space_name, 2.5, ndep, attack, physical_model, data_paths, recv_file_name=file_name)

    lvs = []
    curves_as_p = []

    for v in versions:
        this_data = data[strategy][v]
        curve_as_area = sum(this_data)
        curves_as_p.append(curve_as_area)
        lvs.append(logic_net_version)

    return lvs, curves_as_p


def show_curves_as_bar_and_error_by_model_double_plot(interlink_type, interlink_version, ndep, strategy, m_results=False, save_fig=True):
    models = ['GG', 'GPA', 'RNG', '5NN', 'YAO', 'ER']
    all_versions = list(range(1, 11))
    x_axis = [all_versions, all_versions]
    double_values = []
    double_legend = []
    double_yerr_list = []
    bars_shown = len(models)


    spaces = [(100, 100), (20, 500)]
    for space in spaces:
        values = []
        legend = []
        yerr_list = []
        for model in models:
            values_for_current_model = []
            yerr_for_current_model = []
            for lv in all_versions:

                lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, legacy=False, m_results=m_results)
                p_means = np.mean(curves_as_p)
                p_std = np.std(curves_as_p)
                values_for_current_model.append(p_means)
                yerr_for_current_model.append(p_std)
            values.append(values_for_current_model)
            legend.append(model)
            yerr_list.append(yerr_for_current_model)
        double_values.append(values)
        double_legend.append(legend)
        double_yerr_list.append(yerr_list)

    # pt.plot_bar(possible_degrees, bars_shown_per_degree, values_shown, bar_names, y_label, x_label, title)
    title = ["{}={}, {}".format(r'$I_{max}$', ndep, "(1:1)"),
             "{}={}, {}".format(r'$I_{max}$', ndep, "(1:25)")]
    fig_name = "cap3_show_pnet_effect_ndep_{}.png".format(ndep)
    fig_path = '../figures/cap3/{}'.format(fig_name)
    if not save_fig:
        fig_path = None
    plot.double_plot_bar(x_axis, [bars_shown, bars_shown], double_values, double_legend, r'$TG_L$', r'$q$', title, yerr_list=double_yerr_list, savefig_to=fig_path)


def show_curves_as_bar_and_error_by_model(interlink_type, interlink_version, space, ndep, strategy, m_results=False):
    models = ['GG', 'GPA', 'RNG', '5NN', 'YAO', 'ER']
    all_versions = list(range(1, 11))
    x_axis = all_versions
    values = []
    bars_shown = len(models)
    legend = []
    yerr_list = []
    for model in models:
        values_for_current_model = []
        yerr_for_current_model = []
        for lv in all_versions:

            lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, legacy=False, m_results=m_results)
            p_means = np.mean(curves_as_p)
            p_std = np.std(curves_as_p)
            values_for_current_model.append(p_means)
            yerr_for_current_model.append(p_std)
        values.append(values_for_current_model)
        legend.append(model)
        yerr_list.append(yerr_for_current_model)

    # pt.plot_bar(possible_degrees, bars_shown_per_degree, values_shown, bar_names, y_label, x_label, title)
    title = "{}, ndep {}".format(space, ndep)
    plot.plot_bar(x_axis, bars_shown, values, legend, "TG_L", "lv", title, yerr_list=yerr_list)


def show_imaxes_as_lines_with_error_tgl(lv, interlink_type, interlink_version, space, strategy, m_results=False, check_u_q=False, save_fig=True, strategies_comp=None, name_mod=""):
    models = ['RNG', 'GPA', 'GG', '5NN', 'YAO', 'ER']

    x_axis = list(range(1, 11))
    max_y = 0
    miaux = []
    lines = {}
    errors = {}

    values_per_imax_with_extra = {}
    values_per_imax_original = {}
    error_colors = None
    if check_u_q:
        print("--------- q = {} --- Contents\n [".format(lv))
    if type(m_results) == list:
        for model in models:

            for res_type in m_results:
                current_line = []
                current_error = []
                for ndep in x_axis:

                    lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, legacy=False, m_results=res_type)
                    p_means = np.mean(curves_as_p)
                    if p_means > max_y:
                        max_y = int(p_means)
                    p_std = np.std(curves_as_p)
                    current_line.append(p_means)
                    current_error.append(p_std)
                if res_type:
                    space_aux = (20,500)
                else:
                    space_aux = (100,100)
                lines["{} {}".format(model, space_aux)] = current_line
                errors["{} {}".format(model, space_aux)] = current_error

                if check_u_q:
                    str_ver_list = []
                    for i in range(len(current_line)):
                        this_mean = np.round(current_line[i], 2)
                        this_std = np.round(current_error[i], 2)
                        str_ver = "{} ({})".format(this_mean, this_std)
                        str_ver_list.append(str_ver)
                    if res_type:
                        values_per_imax_with_extra[model] = str_ver_list
                    else:
                        values_per_imax_original[model] = str_ver_list
                    u_q = set()
                    for i in range(len(current_line)):
                        if i > 0:
                            if current_line[i] < current_line[i-1]:
                                u_q.add(i+1)
                                continue
                    aux_str = "                "
                    if res_type:
                        aux_str = "extra interlinks"
                        for i in range(len(miaux)):
                            miaux[i] = current_line[i]-miaux[i]
                    else:
                        miaux = current_line.copy()
                    round_line = []
                    for e in miaux:
                        round_line.append(np.round(e,3))
                    if res_type:
                        print("{},".format(round_line))
        write_table = False
        if check_u_q and write_table:
            print("\\begin{table}[]")
            print("\\makebox[1 \\textwidth][c]{")
            print("\\small")
            print("\\tabcolsep=0.11cm")
            print("\\begin{tabular}{|c|l|l|l|l|l|l|l|}")
            print("\\hline")
            print("\\multicolumn{8}{|c|}{$q = " + str(lv) + "$}                            \\\\ \\hline")
            print("$I_{max}$ & $+I$ & RNG & GG & GPA & 5-NNG & Yao & ER \\\\ \\hline")
            for imax in range(0, 10):
                line_2 = "\\multirow{2}{*}{" + str(imax+1) + "}  & $\\times$ "
                line_1 = "                    & $\\checkmark$ "
                for model in ['RNG', 'GG', 'GPA', '5NN', 'YAO', 'ER']:
                    line_1 += "& {} ".format(values_per_imax_with_extra[model][imax])
                    line_2 += "& {} ".format(values_per_imax_original[model][imax])
                line_2 += "\\\\ \\cline{2-8}"
                line_1 += "\\\\ \\hline"
                print(line_2)
                print(line_1)
            print("\\end{tabular}")
            print("}")
            print("\\caption{Average robustness $\\overline{TG_L}$ of systems with $q=" + str(lv) + "$, and $s=(1:25)$ with and without interlinks added to bridge nodes in $B_{h}^{(q,u)}$.}")
            #print("\\label{tab:tgl_original_and_m_res_q_" + str(lv) + "}")
            print("\\end{table}")
        fig_name = 'cap4_show_imax_lv_{}_m_results.png'.format(lv)
        fig_path = '../figures/cap4/{}'.format(fig_name)
        y_lim = [150, max_y + 100]
        x_lim = [0.5, 10.5]
        use_title = True
    elif strategies_comp:
        model_colors = {"RNG":  '#7aa711',
                        "GPA": '#807dba',
                        "5NN": '#dd3497',
                        "YAO": '#6baed6',
                        "GG": '#ec7014',
                        "ER": '#B99D22'}
        model = strategies_comp
        lv = 1
        error_colors = ['#025c03', '#1321bd', '#6e13bd', '#00a9b5', '#120104']
        strategies = ['simple graphs', 'distance_aux', 'local_hubs', 'degree_aux', 'random']
        x_axis = [3, 5, 7, 10]
        for strategy in strategies:
            for space in [(100, 100), (20, 500)]:
                current_line = []
                current_error = []
                for ndep in x_axis:

                    lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, legacy=False, m_results=m_results)
                    p_means = np.mean(curves_as_p)
                    if p_means > max_y:
                        max_y = int(p_means)
                    p_std = np.std(curves_as_p)
                    current_line.append(p_means)
                    current_error.append(p_std)
                lines["{} {} {}".format(strategy, space, model)] = current_line
                errors["{} {} {}".format(strategy, space, model)] = current_error
        fig_name = 'cap5_st_comp_{}.png'.format(model)
        if len(name_mod) > 0:
            fig_name = 'cap5_st_comp_{}_d1250.png'.format(model)
            error_colors.append('#f50025')
            strategy = "distance_aux"
            strategy_name = "distance 2"
            for space in [(100, 100), (20, 500)]:
                current_line = []
                current_error = []
                for ndep in x_axis:
                    mod_title = "d{}_".format(name_mod)
                    lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, legacy=False, m_results=m_results, add_to_title=mod_title)
                    p_means = np.mean(curves_as_p)
                    if p_means > max_y:
                        max_y = int(p_means)
                    p_std = np.std(curves_as_p)
                    current_line.append(p_means)
                    current_error.append(p_std)
                lines["{} {} {}".format(strategy_name, space, model)] = current_line
                errors["{} {} {}".format(strategy_name, space, model)] = current_error


        fig_path = '../figures/cap5/{}'.format(fig_name)
        y_lim = [150, max_y + 100]
        x_lim = [2.7, 10.3]
        use_title = False
    else:
        for model in models:
            for space in [(100, 100), (20, 500)]:
                current_line = []
                current_error = []
                for ndep in x_axis:

                    lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, legacy=False, m_results=m_results)
                    p_means = np.mean(curves_as_p)
                    if p_means > max_y:
                        max_y = int(p_means)
                    p_std = np.std(curves_as_p)
                    current_line.append(p_means)
                    current_error.append(p_std)
                lines["{} {}".format(model, space)] = current_line
                errors["{} {}".format(model, space)] = current_error
                if check_u_q:
                    u_q = set()
                    for i in range(len(current_line)):
                        if i > 0:
                            if current_line[i] < current_line[i-1]:
                                u_q.add(i+1)
                                continue
                    print("{}: U_q = {}".format("{} {}".format(model, space), u_q))
        fig_name = 'cap3_show_imax_lv_{}.png'.format(lv)
        fig_path = '../figures/cap3/{}'.format(fig_name)
        y_lim = [150, max_y+100]
        x_lim = [0.5, 10.5]
        use_title = False
    if not save_fig:
        fig_path = None
    plot.n_line_plot(lines, x_axis, "lv {} {}".format(lv, space), ylim=y_lim, xlim=x_lim, errors=errors, color_pairs=True, savefig_to=fig_path, xlabel=r'$I_{max}$', ylabel=r'$TG_L$',
                     use_titles=use_title, err_c=error_colors)


def show_curves_as_points_by_space(interlink_type, interlink_version, physical_model, strategy, ndep, m_results=False, strategy_2=None, space=None, save_fig=True):
    all_data = dp.run_data()
    fig, ax = plt.subplots()
    size = 10
    all_lines = {}
    all_versions = list(range(1, 11))
    markers = {(100, 100): 'x', (20, 500): 'x'}
    spaces = [(100, 100), (20, 500)]
    colors = {(100, 100): '#1d91c0', (20, 500): '#ae017e'}
    median_colors = {(100, 100): 'black', (20, 500): 'white'}
    i = 0
    data = []
    axes = []
    legend_aux = {}

    if strategy_2 != None and space != None:
        legend_dict = {"simple graphs": "Original {}".format(r'$P_j$'),
                       "local_hubs": "Local hubs {}".format(r'$st$'),
                       "distance_aux": "Distance {}".format(r'$st$'),
                       "degree_aux": "Degree {}".format(r'$st$'),
                       "random": "Random {}".format(r'$st$')}
        lv = 1
        strategies = [strategy, strategy_2]
        physical_models = ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]
        for st in strategies:
            for physical_model in physical_models:
                lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, physical_model, ndep, space, st)
                current_marker = markers[space]
                i = (i + 1) % 2
                data.append(curves_as_p)
                axes.append(physical_model)
                bp = ax.boxplot(curves_as_p, positions=[(physical_models.index(physical_model))], patch_artist=True)
                for patch in bp['boxes']:

                    patch.set_edgecolor(colors[spaces[strategies.index(st)]])
                    patch.set_facecolor(colors[spaces[strategies.index(st)]])
                for whisker in bp['whiskers']:
                    whisker.set(color=colors[spaces[strategies.index(st)]],
                                linewidth=1.5)
                for cap in bp['caps']:
                    cap.set(color=colors[spaces[strategies.index(st)]],
                            linewidth=2)
                for flier in bp['fliers']:
                    flier.set(marker=current_marker,
                              markerfacecolor=colors[spaces[strategies.index(st)]],
                              markeredgecolor=colors[spaces[strategies.index(st)]],
                              alpha=1)
                for med in bp['medians']:
                    med.set(color=median_colors[space])
                legend_aux[st] = bp
        ax.legend([legend_aux[strategy_2]["boxes"][0], legend_aux[strategy]["boxes"][0]], [legend_dict[strategy_2], legend_dict[strategy]], loc="upper left")
        plt.ylabel(r'$TG_{L}$', fontsize=15)
        plt.xticks([0, 1, 2, 3, 4, 5], physical_models)
        space_name = {(20, 500): "ln", (100, 100): "sq"}
        fig_name = 'cap5_show_before_after_ndep_{}_{}_{}.png'.format(ndep, space_name[space], strategy_2)
        fig_path = '../figures/cap5/{}'.format(fig_name)
        print(fig_path)
        if save_fig:
            plt.savefig(fig_path, dpi=300, bbox_inches='tight', pad_inches=0.002)
    else:
        for lv in all_versions:
            for space in spaces:

                space_name = all_data["file_space_names"][space]
                lvs, curves_as_p = get_curves_as_points(lv, interlink_type, interlink_version, physical_model, ndep, space, strategy, legacy=False, m_results=m_results)

                current_marker = markers[space]
                i = (i+1) % 2
                data.append(curves_as_p)
                axes.append(lv)
                bp = ax.boxplot(curves_as_p, positions=[lv], patch_artist=True)
                for patch in bp['boxes']:
                    patch.set_edgecolor(colors[space])
                    patch.set_facecolor(colors[space])
                for whisker in bp['whiskers']:
                    whisker.set(color=colors[space],
                                linewidth=1.5)
                for cap in bp['caps']:
                    cap.set(color=colors[space],
                            linewidth=2)
                for flier in bp['fliers']:
                    flier.set(marker=current_marker,
                              markerfacecolor=colors[space],
                              markeredgecolor=colors[space],
                              alpha=1)
                for med in bp['medians']:
                    med.set(color=median_colors[space])
                legend_aux[space] = bp
        model = physical_model
        ax.legend([legend_aux[(100, 100)]["boxes"][0], legend_aux[(20, 500)]["boxes"][0]], ['{} (1:1)'.format(model), '{} (1:25)'.format(model)], loc="upper left")
        plt.xlabel(r'$q$', fontsize=12)
        plt.ylabel(r'$TG_{L}$', fontsize=15)
        fig_name = 'cap3_show_space_{}_ndep_{}.png'.format(model, ndep)
        fig_path = '../figures/cap3/{}'.format(fig_name)
        if save_fig:
            plt.savefig(fig_path, dpi=300, bbox_inches='tight', pad_inches=0.002)
    plt.show()


def show_legacy_tgl_vs_max_link_length(space, ndep=3, save_figure=False):
    model_colors = {"RNG": {"light": '#7aa711', "dark": '#006837', "st": '#556a4d'},
                    "GG": {"light": '#ec7014', "dark": '#cc4c02', "st": '#695442'},
                    "5NN": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'}}
    models = ["RNG", "GG", "5NN"]#
    strategies = ["distance_aux", "local_hubs", "degree_aux", "random"]
    spaces = [space]#[(100, 100)]#,
    coord_dir = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/node_locations/"
    cm = 1 / 2.54
    fig, ax = plt.subplots(figsize=(19 * cm, 12.5 * cm))

    markers_dict = {"distance_aux": "^", "local_hubs": "*", "degree_aux": "s", "random": "o"}
    st_name = {"distance_aux": "distance", "local_hubs": "local hubs", "degree_aux": "degree", "random": "random"}
    x = 0
    y = 1
    for s in spaces:
        for m in models:
            point_1 = (0, 0)
            point_2 = (0, 0)
            for st in strategies:
                print("s: {}, m: {}, st: {}".format(s, m, st))
                cost_list = []
                lvs, curves_as_p = get_curves_as_points("", "full_random", "", m, ndep, s, st, legacy=True)
                z = np.ones(len(curves_as_p))
                for v in range(1, 11):
                    strategy_path = "/Users/ivana/PycharmProjects/thesis_experiments/networks/physical_networks/extra_edges/{}/candidates_{}x{}_exp_2.5_v{}_m_{}.csv".format(st, s[0], s[1], v, m)
                    edge_list = load_edges_as_list(strategy_path)
                    cord_name = "nodes_{}x{}_exp_2.5_v{}.csv".format(s[0], s[1], v)
                    coord_dict = get_list_of_coordinates_from_csv(coord_dir + cord_name)
                    lengths = all_link_lengths(coord_dict, edge_list)
                    max_link_length = max(lengths)

                    cost_list.append(float(max_link_length))

                point_size = 60
                if st == "local_hubs":
                    point_size = 150
                if st == "random":
                    print(3)
                    point_size = 40
                ax.scatter(cost_list, curves_as_p,   s=[x*point_size for x in z], alpha=1, marker=markers_dict[st], edgecolors=model_colors[m]["light"], color='white', linewidth=1.1
                           , label="{} + {}".format(m, st_name[st]))
                if st == "distance_aux":
                    point_1 = (np.mean(curves_as_p), np.mean(cost_list))
                if st == "degree_aux":
                    point_2 = (np.mean(curves_as_p), np.mean(cost_list))
            ax.plot([point_1[y], point_2[y]], [point_1[x], point_2[x]], linestyle=":", c=model_colors[m]["st"])
    ax.legend()
    ax.set_ylabel(r'$\overline{TG}_L$', fontsize=17)
    ax.set_xlabel(r'$\rho$', fontsize=16)
    if space == (20, 500):
        plt.ylim(310, 930)
    else:
        plt.ylim(310, 930)
    legend = ax.legend(ncol=3, bbox_to_anchor=(-0.01, 1.17), loc='upper left',  prop={'size': 10.7}, edgecolor="black")
    legend.get_frame().set_alpha(None)
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.xscale("log")
    if save_figure:
        s_name = {(20, 500): "ln", (100, 100): "sq"}
        path = "../figures/paper"
        name = "tgl_vs_max_link_length_{}.png".format(s_name[space])
        plt.savefig(os.path.join(path, name), dpi=300, bbox_inches='tight', pad_inches=0.01)

    plt.show()


def show_legacy_tgl_boxplot(model, ndep=3, mod_random=False, save_figure=False):
    spaces = [(20, 500), (100, 100)]
    space_name = {(20, 500): "(1:25)", (100, 100): "(1:1)"}

    cm = 1 / 2.54
    fig, ax = plt.subplots(figsize=(20 * cm, 14 * cm))

    #fig, ax = plt.subplots()

    if mod_random:
        #strategies = ["simple graphs", "random_distance", "distance_aux", "local_hubs", "random_local_hubs", "degree_aux", "random"]
        #st_name = {"simple graphs": "Simple graphs", "random_distance": "RD", "distance_aux": "Distance", "local_hubs": "Local hubs", "random_local_hubs": "RLH", "degree_aux": "Degree",
        #           "random": "Random"}
        strategies = ["random_cap0.01", "random_cap0.05", "random_cap0.25", "random_cap0.5", "random_cap0.75", #"random_cap1.0",
                      "random"]
        st_name = {"random_cap0.01": r'$\rho($'+"distance"+r'$)$', "random_cap0.05": r'$\rho($'+"local hubs"+r'$)$',  "random_cap0.25": r'$0.25\times\rho_{rand}$', "random_cap0.5": r'$0.5\times\rho_{rand}$',
                   "random_cap0.75": r'$0.75\times\rho_{rand}$',# "random_cap1.0": r'$1\times\rho_{rand}$',
                   "random": r'$\rho_{rand}$'}
    else:
        strategies = ["simple graphs", "distance_aux", "local_hubs", "degree_aux", "random"]
        st_name = {"simple graphs": "Simple graphs", "distance_aux": "Distance", "local_hubs": "Local hubs", "degree_aux": "Degree", "random": "Random"}

    # dataframe things
    space_col = []
    strategy_values = {}
    min_val = 1000000
    max_val = 0
    for space in spaces:
        space_col += [space_name[space] for e in range(10)]
        for st in strategies:

            lvs, curves_as_p = get_curves_as_points("", "full_random", "", model, ndep, space, st, legacy=True)
            if min_val > min(curves_as_p):
                min_val = min(curves_as_p)
            if max_val < max(curves_as_p):
                max_val = max(curves_as_p)

            if st not in strategy_values.keys():
                strategy_values[st] = curves_as_p
            else:
                strategy_values[st] += curves_as_p
    data = {}
    for st in strategies:
        data[st_name[st]] = strategy_values[st]
    data["Space"] = space_col

    df = pd.DataFrame(data)

    df_melt = df.melt(id_vars='Space',
                      value_vars=list(st_name.values()),
                      var_name='columns')

    ax1 = sns.stripplot(data=df_melt,
                        hue='Space',  # different colors for different 'cls'
                        x='columns',
                        y='value',
                        order=list(st_name.values()),
                        palette={"(1:25)": '#1d91c0', "(1:1)": '#ae017e'}, jitter=.25, edgecolor='black',
                        dodge=True, linewidth=1, size=4, alpha=0.4)
    b = sns.boxplot(data=df_melt,
                    hue='Space',  # different colors for different 'cls'
                    x='columns',
                    y='value',
                    order=list(st_name.values()),
                    palette={"(1:25)": '#0c06c2', "(1:1)": '#d10845'},
                    showfliers=False,
                    ax=ax, width=0.9)
    ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax.xaxis.grid(True, which='minor', color='grey', lw=1)

    for i, artist in enumerate(ax.artists):
        # Set the linecolor on the artist to the facecolor, and set the facecolor to None
        col = artist.get_facecolor()
        artist.set_edgecolor(col)
        artist.set_facecolor('None')
        # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same colour as above
        n = 5
        for j in range(i * n, i * n + n):
            line = ax.lines[j]
            line.set_color(col)
            line.set_mfc(col)
            line.set_mec(col)

    #plt.title('Boxplot grouped by cls')  # You can change the title here
    plt.ylim(min_val - 5, max_val + 5)
    handles, labels = ax.get_legend_handles_labels()
    new_handles = [handles[0], handles[1]]
    new_labels = ["{} {}".format(model, labels[0]), "{} {}".format(model, labels[1])]
    ax.legend(new_handles, new_labels, prop={'size': 12})

    plt.ylabel(r'$\overline{TG}_{L}$', fontsize=18)
    if mod_random:
        ax.tick_params(axis='both', which='major', labelsize=11)
    else:
        ax.tick_params(axis='both', which='major', labelsize=12)
    if mod_random:
        plt.xlabel("Maximum link length", fontsize=12)
    else:
        plt.xlabel("")
    if save_figure:
        path = "../figures/paper"
        name = "tgl_boxplot_{}.png".format(model)
        if mod_random:
            name = "mod_random_{}".format(name)
        plt.savefig(os.path.join(path, name), dpi=300, bbox_inches='tight', pad_inches=0.002)
    plt.show()


def cost_by_length(coord_dict, edges):
    cost = 0
    x = 0
    y = 1

    for edge in edges:
        node_1 = edge[0]
        node_2 = edge[1]
        x1 = coord_dict[node_1][x]
        y1 = coord_dict[node_1][y]
        x2 = coord_dict[node_2][x]
        y2 = coord_dict[node_2][y]
        cost += math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

    return cost


def all_link_lengths(coord_dict, edges):
    lengths = []
    x = 0
    y = 1

    for edge in edges:
        node_1 = edge[0]
        node_2 = edge[1]
        x1 = coord_dict[node_1][x]
        y1 = coord_dict[node_1][y]
        x2 = coord_dict[node_2][x]
        y2 = coord_dict[node_2][y]
        lengths.append(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)))

    return lengths


def get_list_of_coordinates_from_csv(csv_file):
    coord_dict = {}

    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            x = float(row[1])
            y = float(row[2])
            coord_dict[row[0]] = [x, y]

    return coord_dict


def load_edges_as_list(edges_path):
    edge_list = []
    with open(edges_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')
        for row in reader:
            u = row[0]
            v = row[1]
            edge_list.append((u, v))

    return edge_list


def get_averages_for_gl_line(lv, space, model, ndep, strategy="simple graphs", ppv=3, debug=False):
    all_data = dp.run_data()
    # Base data
    data_paths = all_data["results_paths"]
    all_data = dp.run_data()
    exp = all_data["exp"]
    versions = all_data["versions"]
    all_data = {}
    geometry = "{}x{}".format(space[0], space[1])
    path = data_paths["RA"][strategy]
    for version in versions:
        file_name = "result_ppv{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v{}_m_{}.csv".format(ppv, lv, geometry, exp, ndep, version, model)
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
    stds = []
    for key in all_data:
        mean = np.mean(all_data[key])
        stds.append(np.std(all_data[key]))
        all_data[key] = mean
    if debug:
        print("max std: {}".format(max(stds)))
    x_axis = []
    y_axis = []
    for key in all_data:
        x_axis.append(float(key))
        y_axis.append(all_data[key])
    return x_axis, y_axis


def gl_compare_strategies(lv, space, model, imax, debug=False, save_fig=True):
    model_colors_1 = {"RNG": {"light": '#7aa711', "dark": '#006837', "st": '#556a4d'},
                    "GG": {"light": '#ec7014', "dark": '#cc4c02', "st": '#695442'},
                    "5NN": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'},
                    "YAO": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'},
                    "GPA": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'},
                    "ER": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'}}

    model_colors = {"RNG": {"light": '#7aa711', "dark": '#348008', "st": '#858585'},
                      "GPA": {"light": '#807dba', "dark": '#574078', "st": '#858585'},
                      "5NN": {"light": '#dd3497', "dark": '#8a0e56', "st": '#858585'},
                      "YAO": {"light": '#6baed6', "dark": '#2e528c', "st": '#858585'},
                      "GG": {"light": '#ec7014', "dark": '#75390b', "st": '#858585'},
                      "ER": {"light": '#B99D22', "dark": '#ab7e32', "st": '#858585'}}

    shape = ""
    c_mode = ""
    if space == (100, 100):
        shape = "(1:1)"
        c_mode = "dark"
    elif space == (20, 500):
        shape = "(1:25)"
        c_mode = "light"

    x, y_simple = get_averages_for_gl_line(lv, space, model, imax, strategy="simple graphs", debug=debug)
    _, y_distance = get_averages_for_gl_line(lv, space, model, imax, strategy="distance_aux", debug=debug)
    _, y_local_hubs = get_averages_for_gl_line(lv, space, model, imax, strategy="local_hubs", debug=debug)
    _, y_degree = get_averages_for_gl_line(lv, space, model, imax, strategy="degree_aux", debug=debug)
    _, y_random = get_averages_for_gl_line(lv, space, model, imax, strategy="random", debug=debug)
    lines = {"{} {}".format(model, shape): y_simple,
             "{} {} + distance".format(model, shape): y_distance,
             "{} {} + local hubs".format(model, shape): y_local_hubs,
             "{} {} + degree".format(model, shape): y_degree,
             "{} {} + random".format(model, shape): y_random}

    color_list = [model_colors[model][c_mode],
                  model_colors[model]["st"],
                  model_colors[model]["st"],
                  model_colors[model]["st"],
                  model_colors[model]["st"]]
    mark_size = [0, 8.5, 13, 8, 8]
    markers = ["", "^", "*", "s", "o"]
    l_width = [2, 0.7, 0.7, 0.7, 0.7]
    if space == (100, 100):
        space_name = "sq"
    else:
        space_name = "ln"
    fig_name = 'cap5_compare_st_ndep_{}_{}_{}.png'.format(imax, space_name, model)
    fig_path = '../figures/cap5/{}'.format(fig_name)
    if not save_fig:
        fig_path = None

    plot.n_line_plot(lines, x, "", c_list=color_list, markers=markers, marker_size=mark_size, line_size=l_width, savefig_to=fig_path)


def seaborn_test_boxplot():
    data = {'sensitivity': np.random.normal(loc=0, size=10),
            'specificity': np.random.normal(loc=0, size=10),
            'accuracy': np.random.normal(loc=0, size=10),
            'ppv': np.random.normal(loc=0, size=10),
            'auc': np.random.normal(loc=0, size=10),
            'cls': ['sig', 'sig', 'sig', 'sig', 'sig', 'baseline', 'baseline', 'baseline', 'baseline', 'baseline']}

    df = pd.DataFrame(data)
    print(df)
    df_melt = df.melt(id_vars='cls',
                      value_vars=['accuracy',
                                  'auc',
                                  'ppv',
                                  'sensitivity',
                                  'specificity'],
                      var_name='columns')
    b = sns.boxplot(data=df_melt,
                    hue='cls',  # different colors for different 'cls'
                    x='columns',
                    y='value',
                    order=['sensitivity',  # custom order of boxplots
                           'specificity',
                           'accuracy',
                           'ppv',
                           'auc'])

    plt.title('Boxplot grouped by cls')  # You can change the title here
    plt.show()


