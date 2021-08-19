import data_proc.data_processing as dp
import numpy as np
import os
import data_proc.common_plots as cp


def check_cost_efficiency(add_to_title=""):

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
    if add_to_title == '3000':
        models = ['RNG']
    if len(add_to_title) > 0:
        add_1 = "_{}".format(add_to_title)
        add_2 = "d{}_".format(add_to_title)
        all_strategies = ["distance_aux"]
    else:
        add_1 = add_2 = ""
        all_strategies = ['distance_aux', 'local_hubs', 'degree_aux', 'random']#addition_strategies.keys()
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
                                                          other="candidates{}".format(add_1))
                    # get cost for each version
                    cost = dp.get_cost_of_added_edges(path, dp.cost_by_length, nodes_allocations[geometry][i],
                                                      file_name)

                    costs_lists.append(cost)
                mean_cost = (np.mean(costs_lists)).round(decimals=2)
                standard_deviation_cost = (np.std(costs_lists)).round(decimals=2)
                average_costs[geometry][addition_strategy][model] = {"mean": mean_cost,
                                                          "std": standard_deviation_cost,
                                                          "all cost": costs_lists}

                for ndep in x_axis:

                    o_lvs, o_curves_as_p = cp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, geometry, "simple graphs")
                    o_p_means = np.mean(o_curves_as_p)
                    o_p_std = (np.std(o_curves_as_p)).round(decimals=2)

                    st_lvs, st_curves_as_p = cp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, geometry, addition_strategy, add_to_title=add_2)
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
        if len(add_to_title) > 0:
            print("\\begin{tabular}{|l|l|}")
            print("\\hline")
            print("\\multicolumn{2}{|c|}{$I_{max}=" + str(imax) + "$}                                                                    \\\\ \\hline")
        else:
            print("\\begin{tabular}{|l|l|l|l|l|}")
            print("\\hline")
            print("\\multicolumn{5}{|c|}{$I_{max}=" + str(imax) + "$}                                                                    \\\\ \\hline")
        for geometry in [(20, 500), (100, 100)]:
            if geometry == (100, 100):
                gname = "(1:1)"
            else:
                gname = "(1:25)"
            if len(add_to_title) > 0:
                print("\\multicolumn{2}{|c|}{" + gname + "}                                                                    \\\\ \\hline")
            else:
                print("\\multicolumn{5}{|c|}{" + gname + "}                                                                    \\\\ \\hline")
            if not head_on:
                head_on = True
                if len(add_to_title) > 0:
                    print("$m$/$st$ & Distance         \\\\ \\hline")
                else:
                    print("$m$/$st$ & Distance         & Local hubs        & Degree                & Random                \\\\ \\hline")
            for model in models:
                model_line = "{} ".format(model)
                for addition_strategy in all_strategies:
                    model_line += "& {}".format(average_efficiency[geometry][addition_strategy][model][imax])
                model_line += " \\\\ \\hline"
                print(model_line)
        print("\\end{tabular}")
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
            with open(file_name, 'w') as save_file:
                save_file.write("\\begin{table}[]\n")
                save_file.write("\\begin{tabular}{|l|l|l|l|}\n")
                save_file.write("\\hline\n")

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
                save_file.write(line_0)

                for row in line_list:
                    save_file.write(row)


                save_file.write("\\end{tabular}\n")
                save_file.write("\\end{table}\n")
                save_file.close()

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
            file_name = os.path.join(save_average_cost_data_path, f_name)
            with open(file_name, 'w') as save_file:
                save_file.write("\\begin{table}[]\n")
                save_file.write("\\begin{tabular}{|l|l|l|l|}\n")
                save_file.write("\\hline\n")

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
                save_file.write(line_0)

                for line in line_list:
                    save_file.write(line)

                save_file.write("\\end{tabular}\n")
                save_file.write("\\end{table}\n")
                save_file.close()


#check_cost_efficiency()
make_cost_table(check_strategies=True, title_mod="cl_", legacy=True)