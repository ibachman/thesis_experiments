#import data_proc.thesis_figures as tf
import data_proc.common_plots as cp
import data_proc.plotting as ptng


#ptng.write_stuff("20x500", "distance_aux", use_model=["GG"], is_seismic=True)

for imax in [5, 7, 10]:
    for strategy in ["simple_graphs", "distance_aux", "local_hubs", "degree_aux", "random"]:
        for model in ["RNG", "GG", "GPA", "5NN", "YAO", "ER"]:
            print("{} {} {}".format(model, strategy, imax))




