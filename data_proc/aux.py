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
version = 2
number_of_iterations = 100

data_dict_100 = dp.get_complete_decay_data(physical_model, space, ndep, version, number_of_iterations)
zero_dict_100 = dp.check_zeros(data_dict_100)

number_of_iterations = 100
data_dict_50 = dp.get_complete_decay_data(physical_model, space, ndep, version, number_of_iterations)
zero_dict_50 = dp.check_zeros(data_dict_50)

number_of_iterations = 100
data_dict_10 = dp.get_complete_decay_data(physical_model, space, ndep, version, number_of_iterations)
zero_dict_10 = dp.check_zeros(data_dict_10)

total_zeros_100 = 0
total_zeros_50 = 0
total_zeros_10 = 0
for key in zero_dict_100.keys():
    zeros_100 = zero_dict_100[key]
    zeros_50 = zero_dict_50[key]
    zeros_10 = zero_dict_10[key]

    if numpy.mean(data_dict_100[key]) != 0.0:
        total_zeros_100 += zeros_100 * 100
    if numpy.mean(data_dict_50[key]) != 0.0:
        total_zeros_50 += zeros_50 * 50
    if numpy.mean(data_dict_10[key]) != 0.0:
        total_zeros_10 += zeros_10 * 10

    if (zeros_10 != 1.0 or zeros_100 != 1.0 or zeros_50 != 1.0) and zeros_10 >= zeros_100 >= zeros_50 > 0.0:
        print("{}:  {}   |   {}  |   {}".format(key, zeros_100, zeros_50, zeros_10))

print("100:", total_zeros_100/(1999*100), "50:", total_zeros_50/(1999*50), "10:", total_zeros_10/(1999*10))

# deberia ver los ceros pero en casos donde el promedio no es tan cercano a 0, creo??
