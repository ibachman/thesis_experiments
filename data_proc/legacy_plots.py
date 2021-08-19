from data_proc.common_plots import *
import data_proc.data_processing as dp

USE_INTERNAL = False

# Base data
all_data = dp.run_data()

# Base data
data_paths = all_data["results_paths"]

average_data_paths = all_data["average_results_path"]

data_types = all_data["strategies"]
plot_types = ["fixed damage", "fixed I_max", "compare strategies", "all imax", "shape comparison",
              "all simple shape comparison"]
geometry_types = all_data["geometry"]
# Graph parameters
exp = all_data["exp"]
attack = all_data["attack"]
amount_of_physical_nodes = 2000
systems = all_data["models"]
versions = all_data["versions"]

get_damage_at_x_percent = False
show_all_data_for_imax = False
show_all_data_for_model = False
show_all_strategies_for_imax_and_network = False
generate_average_files = False
shape_comparison = False
all_shape_comparison = False
show_imax = None
show_network = None
geometry_type = None
data_type = None
use_legacy = True


# Auxiliary function to transform lists into a set of options for the user
def list_to_input_str(input_list):
    input_str = "("
    number = 1
    for name in input_list:
        input_str += "{0} = {1}, ".format(str(number), str(name))
        number += 1
    return input_str[:-2] + ")"


def generate_lists_for_all_fixed_imax_graphs(imax, create_average_files=False):
    # (1 = fixed damage, 2 = fixed I_max, 3 = compare strategies,
    # 4 = all imax, 5 = shape comparison, 6 = all simple shape comparison)
    fixed_imax_option = 2
    if create_average_files:
        average_files = 'y'
    else:
        average_files = 'n'
    final_list = []
    # (1 = (20, 500), 2 = (100, 100))
    geometries = [1, 2]
    # (1 = simple graphs, 2 = random, 3 = degree, 4 = distance)
    strategies = [1, 2, 3, 4]
    for geometry in geometries:
        for strategy in strategies:
            current_list = [fixed_imax_option, geometry, imax, strategy, average_files]
            final_list.append(current_list)
    return final_list


def generate_lists_for_all_compare_strategies(imax):
    # (1 = fixed damage, 2 = fixed I_max, 3 = compare strategies,
    # 4 = all imax, 5 = shape comparison, 6 = all simple shape comparison)
    fixed_imax_option = 3
    final_list = []
    # (1 = (20, 500), 2 = (100, 100))
    geometries = [1, 2]
    # (1 = 5NN, 2 = GG, 3 = RNG)
    models = [1, 2, 3]
    for geometry in geometries:
        for model in models:
            current_list = [fixed_imax_option, geometry, imax, model]
            final_list.append(current_list)
    return final_list


def generate_lists_for_all_allimax():
    final_list = []
    # all imax = 4
    # (1 = (20, 500), 2 = (100, 100))
    # (1 = 5NN, 2 = GG, 3 = RNG)
    # (1 = simple graphs, 2 = random, 3 = distance, 4 = distance_aux, 5 = degree_aux)

    for geometry in [1, 2]:
        for model in [1, 2, 3]:
            for strategy in [1, 2, 3, 4, 5]:
                final_list.append([4, geometry, model, strategy])

    return final_list


if generate_average_files:
    print("chirp0")
    for geometry_type in geometry_types:
        print("chirp")
        generate_all_averages(geometry_type, ndep=3, legacy=True)

if USE_INTERNAL:

    all_options_list = generate_lists_for_all_allimax()#[]#generate_lists_for_all_compare_strategies(3)[[3,1,3,3]]#

    for options_list in all_options_list:
        # Gather inputs from user
        i = 0
        plot_type = plot_types[options_list[i]-1]
        print(plot_type)

        if plot_type != "shape comparison" and plot_type != "all simple shape comparison":
            i += 1
            geometry_type = geometry_types[options_list[i]-1]
            print(geometry_type)

        if plot_type == "fixed damage":
            i += 1
            damage = {}
            get_damage_at_x_percent = True
            damage_fraction = float(options_list[i]-1)
            print(damage_fraction)

        elif plot_type == "fixed I_max":
            show_all_data_for_imax = True
            i += 1
            show_imax = options_list[i]
            print(show_imax)

        elif plot_type == "compare strategies":
            show_all_strategies_for_imax_and_network = True
            i += 1
            show_imax = options_list[i]
            print(show_imax)
            i += 1
            print("i: {}".format(i))
            print(systems)
            show_network = systems[options_list[i]-1]

            print(show_network)

        elif plot_type == "all imax":
            show_all_data_for_model = True
            i += 1
            show_network = systems[options_list[i]-1]
        elif plot_type == "shape comparison":
            shape_comparison = True
            i += 1
            show_imax = options_list[i]
            i += 1
            show_network = systems[options_list[i]-1]
        elif plot_type == "all simple shape comparison":
            all_shape_comparison = True
            i += 1
            show_imax = options_list[i]

        if not show_all_strategies_for_imax_and_network and not shape_comparison and not all_shape_comparison:
            i += 1
            data_type = data_types[options_list[i]-1]
            # Run using input data
            data_path = data_paths["RA"][data_type]
            average_data_path = average_data_paths[data_type]
            i += 1
            want_to_create_average_files = 'n'#options_list[i]
            if want_to_create_average_files == 'y':
                generate_average_files = True
            else:
                generate_average_files = False

        show_plot(show_network,
                  geometry_type,
                  show_imax=show_imax,
                  data_type=data_type,
                  get_damage_at_x_percent=get_damage_at_x_percent,
                  show_all_data_for_imax=show_all_data_for_imax,
                  show_all_data_for_model=show_all_data_for_model,
                  shape_comparison=shape_comparison,
                  all_shape_comparison=all_shape_comparison,
                  generate_average_files=generate_average_files,
                  show_all_strategies_for_imax_and_network=show_all_strategies_for_imax_and_network,
                  legacy=use_legacy)

else:
    # Gather inputs from user
    plot_type = plot_types[int(input("What type of plot do you want ? " + list_to_input_str(plot_types) + " : "))-1]

    if plot_type != "shape comparison" and plot_type != "all simple shape comparison":
        geometry_type = geometry_types[int(input("What geometry do you want ? " + list_to_input_str(geometry_types) + " : "))-1]

    if plot_type == "fixed damage":
        damage = {}
        get_damage_at_x_percent = True
        damage_fraction = float(input("Insert damage percent: "))

    elif plot_type == "fixed I_max":
        show_all_data_for_imax = True
        show_imax = input("Choose I_max {0} : ".format(str(dp.get_imax_tested())))

    elif plot_type == "compare strategies":
        show_all_strategies_for_imax_and_network = True
        show_imax = input("Choose I_max {0} : ".format(str(dp.get_imax_tested())))
        show_network = systems[int(input("Choose Network " + list_to_input_str(systems) + " : "))-1]

    elif plot_type == "all imax":
        show_all_data_for_model = True
        show_network = systems[int(input("Choose Network " + list_to_input_str(systems) + " : ")) - 1]
    elif plot_type == "shape comparison":
        shape_comparison = True
        show_imax = input("Choose I_max {0} : ".format(str(dp.get_imax_tested())))
        show_network = systems[int(input("Choose Network " + list_to_input_str(systems) + " : ")) - 1]
    elif plot_type == "all simple shape comparison":
        all_shape_comparison = True
        show_imax = input("Choose I_max {0} : ".format(str(dp.get_imax_tested())))

    if not show_all_strategies_for_imax_and_network and not shape_comparison and not all_shape_comparison:
        data_type = data_types[int(input("Select data type from " + list_to_input_str(data_types) + " : ")) - 1]
        # Run using input data
        data_path = data_paths["RA"][data_type]
        print(data_paths)
        average_data_path = average_data_paths[data_type]
        want_to_create_average_files = input("Do you want to create average files? (y/n) : ")
        if want_to_create_average_files == 'y':
            generate_average_files = True
        else:
            generate_average_files = False

    show_plot(show_network,
              geometry_type,
              show_imax=show_imax,
              data_type=data_type,
              get_damage_at_x_percent=get_damage_at_x_percent,
              show_all_data_for_imax=show_all_data_for_imax,
              show_all_data_for_model=show_all_data_for_model,
              shape_comparison=shape_comparison,
              all_shape_comparison=all_shape_comparison,
              generate_average_files=generate_average_files,
              show_all_strategies_for_imax_and_network=show_all_strategies_for_imax_and_network,
              legacy=use_legacy)
