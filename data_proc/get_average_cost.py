import data_proc.data_processing as dp
import numpy as np
import os


def check_cost_efficiency(imax, debug=False, prefix=""):

    # la idea es sacar el promedio y stdev de los arcos agregados
    all_data = dp.run_data()
    exp = all_data["exp"]

    nodes_allocations = all_data["nodes_allocations"]
    geometries = all_data["geometry"]

    addition_strategies = all_data["extra_edges_path"]
    versions = all_data["versions"]
    models = all_data["models"]

    average_costs = {}
    average_efficiency = {}
    x_axis = [imax]
    lv = 1
    interlink_version = 3
    interlink_type = "provider_priority"

    all_strategies = ['distance_aux', 'local_hubs', 'degree_aux', 'random']#addition_strategies.keys()
    if debug:
        print(all_strategies)
    for geometry in geometries:
        average_efficiency[geometry] = {}
        average_costs[geometry] = {}

        for addition_strategy in all_strategies:
            path = addition_strategies[addition_strategy]
            average_costs[geometry][addition_strategy] = {}
            average_efficiency[geometry][addition_strategy] = {}

            for model in models:
                average_efficiency[geometry][addition_strategy][model] = {}
                # auxiliary array of costs
                costs_lists = []
                for i in versions:
                    gname = dp.tuple_to_gname(geometry)
                    file_name = dp.generate_csv_file_name(gname, exp, "", "", i, model,
                                                          other="candidates")
                    # get cost for each version
                    cost = dp.get_cost_of_added_edges(path, dp.cost_by_length, nodes_allocations[geometry][i],
                                                      file_name)

                    costs_lists.append(cost)
                if debug:
                    print(addition_strategy)
                    print(model)
                    print(costs_lists)

                mean_cost = (np.mean(costs_lists)).round(decimals=2)
                standard_deviation_cost = (np.std(costs_lists)).round(decimals=2)
                average_costs[geometry][addition_strategy][model] = {"mean": mean_cost,
                                                          "std": standard_deviation_cost,
                                                          "all cost": costs_lists}

                for ndep in x_axis:

                    o_lvs, o_curves_as_p = dp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, geometry, "simple graphs")
                    o_p_means = np.mean(o_curves_as_p)
                    o_p_std = (np.std(o_curves_as_p)).round(decimals=2)

                    st_lvs, st_curves_as_p = dp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, geometry, addition_strategy, add_to_title=prefix)
                    st_p_means = np.mean(st_curves_as_p)
                    st_p_std = (np.std(st_curves_as_p)).round(decimals=2)

                    delta_tgl = st_p_means - o_p_means

                    average_efficiency[geometry][addition_strategy][model][ndep] = (((delta_tgl / average_costs[geometry][addition_strategy][model]["mean"]) * 1000)).round(decimals=2)

                    #if model == 'RNG' and addition_strategy == 'distance_aux':
                    #    print("Imax = {}, s = {}, st = {}".format(ndep, geometry, addition_strategy))
                    #    #print("Model: {}, base tgl: {} ({})".format(model, (o_p_means).round(decimals=2), o_p_std))
                    #    print("Model: {}, tgl: : {} ({})".format(model, (st_p_means).round(decimals=2), st_p_std))

    for imax in x_axis:
        head_on = False
        print("\\begin{table}[]")
        print("\\centering")

        print("\\begin{tabular}{|l|l|l|l|l|}")
        print("\\hline")
        print("\\multicolumn{5}{|c|}{$I_{max}=" + str(imax) + "$}                                                                    \\\\ \\hline")
        for geometry in [(20, 500), (100, 100)]:
            if geometry == (100, 100):
                gname = "(1:1)"
            else:
                gname = "(1:25)"

            print("\\multicolumn{5}{|c|}{" + gname + "}                                                                    \\\\ \\hline")
            if not head_on:
                head_on = True
                print("$m$/$st$ & Distance         & Local hubs        & Degree                & Random                \\\\ \\hline")
            for model in models:
                model_line = "{} ".format(model)
                for addition_strategy in all_strategies:
                    model_line += " & {}".format(average_efficiency[geometry][addition_strategy][model][imax])
                model_line += " \\\\ \\hline"
                print(model_line)
        print("\\end{tabular}")
        print("\\caption[Average cost efficiency of each link addition strategy ($I_{max}=" + str(imax) + "$)]{Cost efficiency $Cost_E^{(m,s)}$ of each link addition strategy, for interdependent "
                                                                                                      "networks built using $I_{max}=" + str(imax) + "$. Cost efficiency values have been amplified by "
                                                                                                                                                     "a factor of $10^3$ to improve its "
                                                                                                                                                       "readability.}")

        print("\\label{tab:cost_eff_st}")
        print("\\end{table}")
        print("")


def check_cost_efficiency_distance_plus(add_to_title="1250", prefix=""):
    if len(prefix) > 0:
        if prefix[-1] != "_":
            prefix += "_"

    # la idea es sacar el promedio y stdev de los arcos agregados
    all_data = dp.run_data()
    exp = all_data["exp"]

    nodes_allocations = all_data["nodes_allocations"]
    geometries = all_data["geometry"]

    addition_strategies = all_data["extra_edges_path"]
    versions = all_data["versions"]
    models = all_data["models"]

    average_costs = {}
    average_efficiency = {}
    x_axis = [3, 5, 7, 10]
    lv = 1
    interlink_version = 3
    interlink_type = "provider_priority"

    add_1 = "_{}".format(add_to_title)
    add_2 = "d{}_{}".format(add_to_title, prefix)
    all_strategies = ["distance_aux"]

    for geometry in geometries:
        average_efficiency[geometry] = {}
        average_costs[geometry] = {}

        for addition_strategy in all_strategies:
            path = addition_strategies[addition_strategy]
            average_costs[geometry][addition_strategy] = {}
            average_efficiency[geometry][addition_strategy] = {}

            for model in models:
                average_efficiency[geometry][addition_strategy][model] = {}
                # auxiliary array of costs
                costs_lists = []
                for i in versions:
                    gname = dp.tuple_to_gname(geometry)
                    file_name = dp.generate_csv_file_name(gname, exp, "", "", i, model,
                                                          other="candidates{}".format(add_1))
                    # get cost for each version
                    cost = dp.get_cost_of_added_edges(path, dp.cost_by_length, nodes_allocations[geometry][i], file_name)

                    costs_lists.append(cost)

                mean_cost = (np.mean(costs_lists)).round(decimals=2)
                standard_deviation_cost = (np.std(costs_lists)).round(decimals=2)
                average_costs[geometry][addition_strategy][model] = {"mean": mean_cost,
                                                                     "std": standard_deviation_cost,
                                                                     "all cost": costs_lists}

                for ndep in x_axis:

                    o_lvs, o_curves_as_p = dp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, geometry, "simple graphs")
                    o_p_means = np.mean(o_curves_as_p)
                    o_p_std = (np.std(o_curves_as_p)).round(decimals=2)

                    st_lvs, st_curves_as_p = dp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, geometry, addition_strategy, add_to_title=add_2)
                    st_p_means = np.mean(st_curves_as_p)
                    st_p_std = (np.std(st_curves_as_p)).round(decimals=2)

                    delta_tgl = st_p_means - o_p_means

                    average_efficiency[geometry][addition_strategy][model][ndep] = (((delta_tgl / average_costs[geometry][addition_strategy][model]["mean"]) * 1000)).round(decimals=2)

    print("\\begin{table}[]")
    print("\\centering")
    print("\\makebox[\\linewidth]{")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    print("$s$                     & $I_{max}$ & RNG   & GG    & GPA   & 5NN   & YAO   & ER    \\\\ \\hline")
    for geometry in [(20, 500), (100, 100)]:
        first_line_for_space = True
        for imax in x_axis:

            if geometry == (100, 100):
                gname = "(1:1)"
            else:
                gname = "(1:25)"

            if first_line_for_space:
                line_part_1 = "\multirow{4}{*}{" + gname + "}" + " & {}         ".format(imax)
                line_part_2 = " \\\\ \\hline"
                first_line_for_space = False
            else:
                if imax != 10:
                    line_part_1 = "                        & {}         ".format(imax)
                else:
                    line_part_1 = "                        & {}        ".format(imax)
                line_part_2 = " \\\\ \\cline{2-8} "
            line = ""
            for model in ['RNG', 'GG', 'GPA', '5NN', 'YAO', 'ER']:

                for addition_strategy in all_strategies:
                    line += " & {}".format(average_efficiency[geometry][addition_strategy][model][imax])

            print(line_part_1 + line + line_part_2)
    print("\\end{tabular}")
    print("\\caption[Cost efficiency of Distance+ strategy]{Cost efficiency $Cost_E^{(m,s)}$ of Distance+. Cost efficiency values have been amplified by a factor of $10^3$ to improve its "
              "readability.}")
    print("\\label{tab:cost_eff_d1250}")
    print("\\end{table}")
    print("")


def check_cost_efficiency_distance_bs(add_to_title="3000", prefix=""):
    if len(prefix) > 0:
        if prefix[-1] != "_":
            prefix += "_"

    # la idea es sacar el promedio y stdev de los arcos agregados
    all_data = dp.run_data()
    exp = all_data["exp"]

    nodes_allocations = all_data["nodes_allocations"]
    geometries = all_data["geometry"]

    addition_strategies = all_data["extra_edges_path"]
    versions = all_data["versions"]
    models = ['RNG']

    average_costs = {}
    average_efficiency = {}
    x_axis = [3, 5, 7, 10]
    lv = 1
    interlink_version = 3
    interlink_type = "provider_priority"

    add_1 = "_{}".format(add_to_title)
    add_2 = "d{}_{}".format(add_to_title, prefix)
    all_strategies = ["distance_aux", "local_hubs"]

    for geometry in geometries:
        average_efficiency[geometry] = {}
        average_costs[geometry] = {}

        for addition_strategy in all_strategies:
            path = addition_strategies[addition_strategy]
            average_costs[geometry][addition_strategy] = {}
            average_efficiency[geometry][addition_strategy] = {}

            for model in models:
                average_efficiency[geometry][addition_strategy]['GG'] = {}
                average_efficiency[geometry][addition_strategy][model] = {}
                # auxiliary array of costs
                costs_lists = []
                for i in versions:
                    gname = dp.tuple_to_gname(geometry)
                    if addition_strategy == "local_hubs":
                        add_1 = add_2 = ""
                    if addition_strategy == "distance_aux":
                        add_1 = "_{}".format(add_to_title)
                        add_2 = "d{}_{}".format(add_to_title, prefix)
                    file_name = dp.generate_csv_file_name(gname, exp, "", "", i, model,
                                                          other="candidates{}".format(add_1))
                    # get cost for each version
                    cost = dp.get_cost_of_added_edges(path, dp.cost_by_length, nodes_allocations[geometry][i], file_name)

                    costs_lists.append(cost)

                mean_cost = (np.mean(costs_lists)).round(decimals=2)
                standard_deviation_cost = (np.std(costs_lists)).round(decimals=2)
                average_costs[geometry][addition_strategy][model] = {"mean": mean_cost,
                                                                     "std": standard_deviation_cost,
                                                                     "all cost": costs_lists}

                for ndep in x_axis:

                    o_lvs, o_curves_as_p = dp.get_curves_as_points(lv, interlink_type, interlink_version, 'GG', ndep, geometry, "simple graphs")
                    o_p_means = np.mean(o_curves_as_p)
                    o_p_std = (np.std(o_curves_as_p)).round(decimals=2)

                    st_lvs, st_curves_as_p = dp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, geometry, addition_strategy, add_to_title=add_2)
                    st_p_means = np.mean(st_curves_as_p)
                    st_p_std = (np.std(st_curves_as_p)).round(decimals=2)


                    average_efficiency[geometry][addition_strategy][model][ndep] = "{} ({})".format(np.round(st_p_means, 2), np.round(st_p_std, 2))#(((delta_tgl / average_costs[geometry][
                    average_efficiency[geometry][addition_strategy]['GG'][ndep] = "{} ({})".format(np.round(o_p_means, 2), np.round(o_p_std, 2))  # (((delta_tgl / average_costs[geometry][



    print("\\begin{table}[]")
    print("\\centering")
    print("\\makebox[\\linewidth]{")
    print("\\begin{tabular}{|l|l|l|l|l|l|l|l|}")
    print("\\hline")
    print("$s$                     & $I_{max}$ & RNG + Distance($B^s$) & RNG + Local hubs & GG    \\\\ \\hline")
    for geometry in [(20, 500), (100, 100)]:
        first_line_for_space = True
        for imax in x_axis:

            if geometry == (100, 100):
                gname = "(1:1)"
            else:
                gname = "(1:25)"

            if first_line_for_space:
                line_part_1 = "\multirow{4}{*}{" + gname + "}" + " & {}         ".format(imax)
                line_part_2 = " \\\\ \\hline"
                first_line_for_space = False
            else:
                if imax != 10:
                    line_part_1 = "                        & {}         ".format(imax)
                else:
                    line_part_1 = "                        & {}        ".format(imax)
                line_part_2 = " \\\\ \\cline{2-5} "
            line = ""
            for model in ['RNG', 'GG']:

                for addition_strategy in all_strategies:
                    if model == "GG" and addition_strategy == "distance_aux":
                        continue
                    line += " & {}".format(average_efficiency[geometry][addition_strategy][model][imax])

            print(line_part_1 + line + line_part_2)
    print("\\end{tabular}")
    print("\\caption[Average $\\overline{TG}_L$ of RNG + Distance($B^s$), GG, and RNG + Local hubs]{Average $\\overline{TG}_L$ comparison of RNG + Distance($B^s$) systems, GG systems, "
          "and RNG + Local hubs systems.}")
    print("\\label{tab:RNG_budget}")
    print("\\end{table}")
    print("")



def make_cost_table(check_strategies=False, title_mod="", legacy=False):
    # la idea es sacar el promedio y stdev de los arcos agregados
    all_data = dp.run_data()
    exp = all_data["exp"]
    attack = all_data["attack"]

    nodes_allocations = all_data["nodes_allocations"]
    geometries = all_data["geometry"]

    addition_strategies = all_data["extra_edges_path"]
    if title_mod == "cl_":
        addition_strategies["random_distance"] = addition_strategies["random"]
        addition_strategies["random_local_hubs"] = addition_strategies["random"]
        addition_strategies["random_cap0.75"] = addition_strategies["random"]
        addition_strategies["random_cap0.5"] = addition_strategies["random"]
        addition_strategies["random_cap0.25"] = addition_strategies["random"]
        addition_strategies["random_cap0.15"] = addition_strategies["random"]
    versions = all_data["versions"]
    models = all_data["models"]
    models_path = all_data["model_links_path"]

    save_average_cost_data_path = os.path.join(all_data["root_path"], "test_results", "average_costs")

    average_data = {}
    if legacy:
        models = ["RNG", "GG", "5NN"]

    if check_strategies:
        # get averaged data for every model and every addition strategy
        for geometry in geometries:
            gname = dp.tuple_to_gname(geometry)
            for addition_strategy in addition_strategies.keys():
                path = addition_strategies[addition_strategy]
                average_data[addition_strategy] = {}

                for model in models:
                    # auxiliary array of costs
                    costs_lists = []
                    for i in versions:
                        gname = dp.tuple_to_gname(geometry)
                        file_name = dp.generate_csv_file_name(gname, exp, "", "", i, model,
                                                              other="candidates")
                        if addition_strategy == "random_distance":
                            file_name = file_name.replace("candidates_", "candidates_cl_distance_")
                        if addition_strategy == "random_local_hubs":
                            file_name = file_name.replace("candidates_", "candidates_cl_local_hubs_")
                        if addition_strategy == "random_cap0.75":
                            file_name = file_name.replace("candidates_", "candidates_cl_cap0.75_")
                        if addition_strategy == "random_cap0.5":
                            file_name = file_name.replace("candidates_", "candidates_cl_cap0.5_")
                        if addition_strategy == "random_cap0.25":
                            file_name = file_name.replace("candidates_", "candidates_cl_cap0.25_")
                        if addition_strategy == "random_cap0.15":
                            file_name = file_name.replace("candidates_", "candidates_cl_cap0.15_")
                        # get cost for each version
                        cost = dp.get_cost_of_added_edges(path, dp.cost_by_length, nodes_allocations[geometry][i],
                                                          file_name)

                        costs_lists.append(cost)
                    mean_cost = (np.mean(costs_lists)).round(decimals=2)
                    standard_deviation_cost = (np.std(costs_lists)).round(decimals=2)
                    average_data[addition_strategy][model] = {"mean": mean_cost,
                                                              "std": standard_deviation_cost,
                                                              "all cost": costs_lists}

            # save data
            file_name = "averaged_data_by_strategy_{}.csv".format(gname)
            if legacy:
                file_name = "legacy_{}{}".format(title_mod, file_name)
            file_name = os.path.join(save_average_cost_data_path, file_name)
            print("\\begin{table}[]\n")
            print("\\begin{tabular}{|l|l|l|l|}\n")
            print("\\hline\n")

            # contents
            line_0_ready = False
            line_0 = "strategy/model"
            line_list = []
            for addition_strategy in addition_strategies.keys():
                line = addition_strategy
                for model in models:
                    if not line_0_ready:
                        line_0 += " & " + model
                    line += " & " + str(average_data[addition_strategy][model]["mean"]) + " (" \
                             + str(average_data[addition_strategy][model]["std"]) + ")"

                end_line = "\\\\ \\hline\n"
                if not line_0_ready:
                    line_0 += end_line
                    line_0_ready = True
                line += end_line
                line_list.append(line)

                # write contents
            print(line_0)

            for row in line_list:
                print(row)


            print("\\end{tabular}\n")
            print("\\end{table}\n")

    else:
        for geometry in geometries:
            gname = dp.tuple_to_gname(geometry)
            # get averaged data for every model and every addition strategy
            for model in models:
                costs_lists = []
                for i in versions:
                    file_name = dp.generate_csv_file_name(gname, exp, "", "", i, model,
                                                          other="physic")

                    # get cost for each version
                    cost = dp.get_cost_of_added_edges(models_path, dp.cost_by_length, nodes_allocations[geometry][i], file_name)

                    costs_lists.append(cost)
                mean_cost = (np.mean(costs_lists)).round(decimals=2)
                standard_deviation_cost = (np.std(costs_lists)).round(decimals=2)
                average_data[model] = {"mean": mean_cost, "std": standard_deviation_cost, "all cost": costs_lists}

            # save data
            f_name = "averaged_data_model_only_{}.csv".format(gname)
            if legacy:
                f_name = "legacy_{}".format(f_name)

            print("\\begin{table}[]\n")
            print("\\begin{tabular}{|l|l|l|l|}\n")
            print("\\hline\n")

            # contents
            line_0_ready = False
            line_0 = "model"
            line_list = []
            end_line = "\\\\ \\hline\n"
            for row in ["mean", "std"]:
                line = row
                for model in models:
                    if not line_0_ready:
                        line_0 += " & " + model
                    line += " & " + str(average_data[model][row])

                if not line_0_ready:
                    line_0 += end_line
                    line_0_ready = True
                line += end_line
                line_list.append(line)

            # write contents
            print(line_0)

            for line in line_list:
                print(line)

            print("\\end{tabular}\n")
            print("\\end{table}\n")


#make_cost_table(check_strategies=True, title_mod="cl_", legacy=True)