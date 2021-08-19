import data_proc.data_processing as dp
import data_proc.plotting as pt
import os
x = 0
y = 1


def get_aggregated_degree_distribution(model, spaces, show="bar"):
    all_data = dp.run_data()
    versions = all_data["versions"]
    link_path = all_data["model_links_path"]
    absolute_max_degree = 0
    bar_names = []

    aggregated_degrees_dict = {}
    for space in spaces:
        aggregated_degrees_dict[space] = {}
        if space == (20, 500):
            bar_names.append("{} (1:25)".format(model))
        if space == (100, 100):
            bar_names.append("{} (1:1)".format(model))

        for version in versions:
            file_name = "physic_{}x{}_exp_{}_v{}_m_{}.csv".format(space[x], space[y], all_data["exp"], version, model)
            print(file_name)
            degrees, max_degree = dp.get_degrees_from_file(os.path.join(link_path, file_name))
            if max_degree > absolute_max_degree:
                absolute_max_degree = max_degree
            for node in degrees:
                current_node_degree = degrees[node]

                if current_node_degree in aggregated_degrees_dict[space].keys():
                    aggregated_degrees_dict[space][current_node_degree] += 1
                else:
                    aggregated_degrees_dict[space][current_node_degree] = 1
    if show == "bar":
        possible_degrees = list(range(1, absolute_max_degree + 1))
        bars_shown_per_degree = len(spaces)
        values_shown = []
        for space in spaces:
            current_space_values_per_degree = []
            print(space)
            sum = 0
            for i in possible_degrees:
                if i not in aggregated_degrees_dict[space].keys():
                    aggregated_degrees_dict[space][i] = 0
                current_space_values_per_degree.append(aggregated_degrees_dict[space][i]/10)
                sum += aggregated_degrees_dict[space][i]
                print("({}): {}".format(i, aggregated_degrees_dict[space][i]/10))
            print(sum)
            values_shown.append(current_space_values_per_degree)

        return possible_degrees, bars_shown_per_degree, values_shown, bar_names
    else:
        x_axis = list(range(1, absolute_max_degree + 1))
        lines = {}
        for space in spaces:
            if space == (20, 500):
                key = "{} (1:25)".format(model)
            if space == (100, 100):
                key = "{} (1:1)".format(model)
            lines[key] = []
            for i in x_axis:
                if i not in aggregated_degrees_dict[space].keys():
                    aggregated_degrees_dict[space][i] = 0
                lines[key].append(aggregated_degrees_dict[space][i]/10)
        return lines, x_axis

# uso
possible_degrees1 = ["a", "b", "c"]
bars_shown_per_degree1 = 2
bar_names1 = ["aa", "bb"]
values_shown1 = [[3, 6, 1],  # all 3 values for bar_names[0]
                 [2, 4, 1]]  # all 3 values for bar_names[1]

y_label = "Number of nodes"
x_label = "Node degree"
title = ""

possible_degrees, bars_shown_per_degree, values_shown, bar_names = get_aggregated_degree_distribution("GG",
                                                                                                      [(20, 500),
                                                                                                       (100, 100)])
print((possible_degrees, bars_shown_per_degree, values_shown, bar_names))
# pt.plot_bar(possible_degrees, bars_shown_per_degree, values_shown, bar_names, y_label, x_label, title)

#lines, x_axis = get_aggregated_degree_distribution("RNG", [(20, 500), (100, 100)], show="lines")

#pt.n_line_plot(lines, x_axis, title, xlabel=x_label, ylabel=y_label,ylim=[0, 1001], xlim=[0.8,5.1],deg_dist=True)

geometries = ["20x500", "100x100"]
exp = "2.5"
system_names = ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]

for geometry in geometries:
    for model in system_names:

        edges_mean, edges_std = dp.get_total_edges(geometry, exp, model)

        print("{} {} mean: {}, std: {}".format(model, geometry, edges_mean, edges_std))


