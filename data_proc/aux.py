#import data_proc.thesis_figures as tf
import data_proc.common_plots as cp
import data_proc.plotting as ptng
import data_proc.data_processing as dp
import numpy



physical_model = "RNG"
space = (20, 500)
ndep = 5
version = 1
number_of_iterations = 100

min_d_list = [[0, 0, 0, 0, 0, 0, 0.05, 0, 0, 0],
              [0.1, 0.0, 0.1, 0.1, 0.1, 0, 0, 0.05, 0.1, 0.05],
              [0.1, 0.1, 0, 0.1, 0, 0.1, 0, 0, 0, 0],
              [0.2, 0.15, 0, 0.25, 0.15, 0.15, 0.1, 0, 0, 0],
              [0.4, 0.1, 0.2, 0.15, 0.2, 0.2, 0.15, 0.3, 0.2, 0.15],
              [0.15, 0.15, 0.25, 0, 0, 0.35, 0.15, 0.15, 0.15, 0],
              [0.2, 0.25, 0.25, 0, 0, 0.25, 0.1, 0.2, 0, 0],
              [0, 0, 0, 0.15, 0, 0, 0, 0.25, 0, 0.25],
              [0.5, 0.1, 0.2, 0.15, 0.25, 0, 0.2, 0, 0.2, 0],
              [0.25, 0.25, 0, 0.3, 0, 0.15, 0.2, 0.15, 0.25, 0.2]]

for ndep in range(1, 2):
    print("++---------- {}".format(ndep))
    for version in range(1, 2):
        #line_dict = dp.get_all_iterartions_as_lines(physical_model, space, ndep, version, number_of_iterations)
        #ml = dp.get_gl_at_pc(line_dict)

        #ml = dp.get_gl_at_pc_using_NOI(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, close_to_max_noi=0.0)


        #ml.sort(reverse=True)

        #line_dict = dp.get_all_iterartions_as_lines(physical_model, space, ndep, version, 99)

        #ml5 = dp.get_gl_at_pc(line_dict)
        #ml5.sort(reverse=True)

        d = min_d_list[ndep - 1][version - 1]
        ml_min = dp.get_gl_at_pc_using_NOI(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, close_to_max_noi=d)
        ml_1 = dp.get_gl_at_pc_using_NOI(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, close_to_max_noi=0.05)
        ml_2 = dp.get_gl_at_pc_using_NOI(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, close_to_max_noi=0.1)
        ml_3 = dp.get_gl_at_pc_using_NOI(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, close_to_max_noi=0.15)

        std_min = numpy.std(ml_min)
        std_1 = numpy.std(ml_1)
        std_2 = numpy.std(ml_2)
        std_3 = numpy.std(ml_3)
        print("  -------- {} -- delta(0.05): {}".format(version, (std_1 - std_min)))
        print("              -- delta(0.10): {}".format((std_2 - std_min)))
        print("              -- delta(0.15): {}".format((std_3 - std_min)))


        #i = ml2.index(0.3333)
        # quizas debería combinar las técnicas? onda comparar yendo desde la derecha a la izquierda y viendo los peaks de noi? o quizas ocupar el peak de noi tal que tenga el delta más largo?
        #print(i)


        #print(ml2)

        #print(dp.get_gl_at_pc_using_NOI(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, close_to_max_noi=0.1))

        #print(ml[i])
        #print(ml2[i])
        #print("---------- {}".format(version))
        #cp.plot_GL_and_NOI(physical_model, space, ndep, version=version, number_of_iterations=100, strategy="simple graphs", lv=1, autoclose=False, save_fig=False, show=[i],
        #                   use_compressed=True)






#cp.plot_gl_at_pc_for_imax(physical_model, space, number_of_iterations=99, strategy="simple graphs", lv=1)
cp.plot_gl_at_pc_for_imax(physical_model, space, number_of_iterations=99, strategy="simple graphs", lv=1)

exit(4)

cp.plot_all_iterations(physical_model, space, ndep, version=version, number_of_iterations=99, strategy="simple graphs", autoclose=False, save_fig=False)
cp.plot_all_iterations(physical_model, space, ndep, version=version, number_of_iterations=100, strategy="simple graphs", autoclose=False, save_fig=False)

#cp.plot_gl_at_pc_for_imax(physical_model, space, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1)
i = 3
#dp.get_gl_at_pc_using_NOI(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1)
#cp.plot_GL_and_NOI(physical_model, space, ndep, version=version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, autoclose=False, save_fig=False, show=[i],
                       #use_compressed=True)

#cp.plot_average_noi(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1)
for i in range(number_of_iterations):
    #cp.plot_GL_and_NOI(physical_model, space, ndep, version=version, number_of_iterations=number_of_iterations, strategy="simple graphs",lv=1, autoclose=False, save_fig=False, show=[i],
    # use_compressed=False)

    #cp.plot_GL_and_NOI(physical_model, space, ndep, version=version, number_of_iterations=99, strategy="simple graphs", lv=1, autoclose=False, save_fig=False, show=[i],
    #                   use_compressed=False)
    #print("------1")
    #cp.plot_GL_and_NOI(physical_model, space, ndep, version=version, number_of_iterations=100, strategy="simple graphs", lv=1, autoclose=False, save_fig=False, show=[i],
    #                   use_compressed=False)
    #print("------2")
    cp.plot_GL_per_iteration(physical_model, space, ndep, version, number_of_iterations=100, strategy="simple graphs", lv=1, show=[i])

    #cp.plot_noi(physical_model, space, ndep, version, number_of_iterations=number_of_iterations, strategy="simple graphs", lv=1, show=[i])


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
file_name = "comp_it{}_result_ppv3_{}_exp_2.5_ndep_{}_att_physical_v{}_m_{}.csv".format(number_of_iterations,space_name, ndep, version, physical_model)

#data = dp.get_all_data_for("", space_name, 2.5, ndep, attack, physical_model, data_paths, recv_file_name=file_name)

#cp.stacked_plot(x, y_list, labels=[r'$G_{L} = 0$',  r'$(p - 0.05) > G_{L} > 0$', r'$G_{L} \geq (p - 0.05)$'], plot_line=data[strategy][version])
# [r'$Z_{G_{L}}$', r'$O_{G_{L}}$', r'$E_{G_{L}}$']

# NEW LINES CAP 3
cp.show_averages_for_all_imax(logic_net_version, interlink_type, 3, "RNG", (20, 500), "simple graphs", m_results=False, save_fig=False, autoclose=False, save_to="",
                              all_imax=None, prefix="seq_comp_it100")

cp.plot_gl_at_pc_for_imax(physical_model, space, number_of_iterations=100, strategy="simple graphs", lv=1)


for ndep in range(1,11):
    #cp.stacked_plot_and_avg_gl_line(physical_model, space, ndep, version=i, number_of_iterations=100, wigle=0.05, strategy=strategy, autoclose=False, save_fig=False)
    cp.plot_all_iterations(physical_model, space, ndep, version=5, number_of_iterations=100, strategy="simple graphs", autoclose=False, save_fig=False)

wigle = 0.05
show_stacked = False
#cp.plot_all_iterations("ER", space, ndep, version=4, number_of_iterations=100, strategy="simple graphs", autoclose=False, save_fig=False)
cp.stacked_plot_and_avg_gl_line(physical_model, space, ndep, version=4, number_of_iterations=100, wigle=wigle, strategy=strategy, autoclose=False, save_fig=False)
#cp.stacked_plot_and_avg_gl_line("ER", space, ndep, version=4, number_of_iterations=100, wigle=wigle, strategy=strategy, autoclose=False, save_fig=False)

if show_stacked:
    cp.stacked_plot_and_avg_gl_line(physical_model, space, ndep, version=4, number_of_iterations=100, wigle=wigle, strategy=strategy, autoclose=False, save_fig=False)
    cp.stacked_plot_and_avg_gl_line(physical_model, space, ndep, version=4, number_of_iterations=100, wigle=wigle, strategy="distance_aux", autoclose=False, save_fig=False)
    cp.stacked_plot_and_avg_gl_line(physical_model, space, ndep, version=4, number_of_iterations=100, wigle=wigle, strategy="local_hubs", autoclose=False, save_fig=False)
    cp.stacked_plot_and_avg_gl_line(physical_model, space, ndep, version=4, number_of_iterations=100, wigle=wigle, strategy="degree_aux", autoclose=False, save_fig=False)
    cp.stacked_plot_and_avg_gl_line(physical_model, space, ndep, version=4, number_of_iterations=100, wigle=wigle, strategy="random", autoclose=False, save_fig=False)

exit(4)
space = (20, 500)
logic_net_version = 1
interlink_type = "provider_priority"
interlink_version = 3
ndep = 10
strategy = "simple graphs"
for physical_model in ["ER","RNG", "GG","GPA","YAO","5NN"]:
    cp.show_each_physical_version(logic_net_version, interlink_type, interlink_version, physical_model, ndep, space, strategy, legacy=False)

