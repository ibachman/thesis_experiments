#import data_proc.thesis_figures as tf
import data_proc.common_plots as cp
import data_proc.plotting as ptng
import data_proc.data_processing as dp
import numpy


#ptng.write_stuff("20x500", "distance_aux", use_model=["GG"], is_seismic=True)

#for imax in [5, 7, 10]:
#    for strategy in ["simple_graphs", "distance_aux", "local_hubs", "degree_aux", "random"]:
#        for model in ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]:
#            print("{} {} {}".format(model, strategy, imax))

physical_model = "RNG"
space = (20, 500)
ndep = 3
version = 4
number_of_iterations = 100

data_dict_100 = dp.get_complete_decay_data(physical_model, space, ndep, version, number_of_iterations)
zero_dict_100 = dp.check_zeros(data_dict_100)
close_v_dict = dp.check_close_to_expected_value(data_dict_100, wigle=0.1)


x = []
zeros = []
close_l = []
rest = []
for key in zero_dict_100.keys():
    x.append(key)
    zeros.append(zero_dict_100[key])
    close_l.append(close_v_dict[key])
    rest.append(max((1-close_v_dict[key]-zero_dict_100[key]),0.0))

# deberia ver los ceros pero en casos donde el promedio no es tan cercano a 0, creo??
y_list = [zeros, rest, close_l]

all_data = dp.run_data()
strategy = "simple graphs"
attack = all_data["attack"]
exp = all_data["exp"]
versions = all_data["versions"]
interlink_type = "provider_priority"
interlink_type_name = all_data["interlink_types"][interlink_type]
data_paths = {strategy: all_data["results_paths"]["RA"][strategy]}
space_name = all_data["file_space_names"][space]
fig_space_name = all_data["figure_space_names"][space]
interlink_version = 3
logic_net_version = 1
file_name_1 = "result_{}v{}_lv{}_{}_exp_{}_ndep_{}_att_physical_v".format(interlink_type_name,
                                                                                  interlink_version, logic_net_version,
                                                                                  space_name, exp, ndep)
file_name_2 = "_m_{}.csv".format(physical_model)
file_name = file_name_1 + "{}" + file_name_2
data = dp.get_all_data_for("", space_name, 2.5, ndep, attack, physical_model, data_paths, recv_file_name=file_name)

cp.stacked_plot(x, y_list, labels=[r'$G_{L} = 0$',  r'$(p - 0.05) > G_{L} > 0$', r'$G_{L} \geq (p - 0.05)$'], plot_line=data[strategy][version])
# [r'$Z_{G_{L}}$', r'$O_{G_{L}}$', r'$E_{G_{L}}$']

exit(3)
space = (20, 500)
logic_net_version = 1
interlink_type = "provider_priority"
interlink_version = 3
ndep = 7
strategy = "simple graphs"
for physical_model in ["RNG", "GG","GPA","ER","YAO","5NN"]:
    cp.show_each_physical_version(logic_net_version, interlink_type, interlink_version, physical_model, ndep, space, strategy, legacy=False)

