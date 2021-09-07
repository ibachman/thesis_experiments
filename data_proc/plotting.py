# libraries
import matplotlib.pyplot as plt
import numpy as np
import data_proc.data_processing as dp
#import data_processing as dp
import csv
import os
import datetime
from collections import Counter


def show_localized_attacks(model, geometry, strategy, ndep, version, radius):
    x, y, z, data = dp.get_data_from_localized_attack(model, geometry, strategy, ndep, version, radius)

    colors = ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026']
    min_damage = min(data["g_l"])
    max_damage = max(data["g_l"])
    print(min_damage)
    print(max_damage)
    color_list = []
    for i in range(len(data["g_l"])):
        if data["g_l"][i] <= 0.2:
            color_list.append(colors[4])
        elif 0.2 < data["g_l"][i] <= 0.4:
            color_list.append(colors[3])
        elif 0.4 < data["g_l"][i] <= 0.6:
            color_list.append(colors[2])
        elif 0.6 < data["g_l"][i] <= 0.8:
            color_list.append(colors[1])
        elif 0.8 < data["g_l"][i] <= 1:
            color_list.append(colors[0])
    x_aux = []
    y_aux = []
    z_aux = []
    clist = []
    for i in range(len(data["g_l"])):
        if 0 <= data["g_l"][i] <= 1:
            x_aux.append(x[i])
            y_aux.append(y[i])
            z_aux.append(z[i])
            clist.append(color_list[i])
    x = x_aux
    y = y_aux
    z = z_aux
    color_list = clist

    # create data

    # use the scatter function
    plt.scatter(x, y, s=[x*100 for x in z], c=color_list, alpha=0.5)
    plt.show()


# GL vs ndep (used in netsciX 2020 paper)
def three_line_plot(line_1, line_2, line_3, ndep_series, damage_percentage, ndep=True):
    custom_colors = ['#1b9e77', '#d95f02', '#7570b3']
    custom_marker_color = ['#1b9e77', '#d95f02', '#7570b3']
    custom_linestyle = ['solid', 'solid', 'solid']
    custom_marker = ['o', "^", "X"]
    custom_label = ["MRN", "GG", "5NN"]
    if ndep:
        custom_linewidth = 3
        custom_marker_size = 12
    else:
        custom_linewidth = 1
        custom_marker_size = 0

    fig, ax = plt.subplots()

    # plot line_1
    ax.plot(ndep_series, line_1, label=custom_label[0], color=custom_colors[0], linestyle=custom_linestyle[0], linewidth=custom_linewidth,
            marker=custom_marker[0], markerfacecolor=custom_marker_color[0], markersize=custom_marker_size)

    # plot line_2
    ax.plot(ndep_series, line_2, label=custom_label[1], color=custom_colors[1], linestyle=custom_linestyle[1], linewidth=custom_linewidth,
            marker=custom_marker[1], markerfacecolor=custom_marker_color[1], markersize=custom_marker_size)

    # plot line_3
    ax.plot(ndep_series, line_3, label=custom_label[2], color=custom_colors[2], linestyle=custom_linestyle[2], linewidth=custom_linewidth,
            marker=custom_marker[2], markerfacecolor=custom_marker_color[2], markersize=custom_marker_size)

    if ndep:
        # setting x and y axis range
        plt.ylim(min(min(line_1), min(line_2), min(line_3)) - 0.05, max(max(line_1), max(line_2), max(line_3)) + 0.05)
        plt.xlim(0, 11)
        # naming the x axis
        plt.xlabel(r'$I_{max}$')
        # giving a title to my graph
        plt.title('{0}% nodes removed'.format(str(damage_percentage)))
    else:
        # setting x and y axis range
        plt.ylim(0, 1)
        plt.xlim(0, 1)
        # naming the x axis
        plt.xlabel('(1 - p)')
        # giving a title to my graph
        plt.title('Average results for {} = {} '.format(r'$I_{max}$',str(damage_percentage)))

    # naming the y axis
    plt.ylabel(r'$G_L$')


    if ndep:
        plt.legend(loc="upper left")
        ax.set_xticks([1, 3, 5, 7, 10], minor=False)
        ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.7, 0.8, 0.9, 1], minor=False)
        ax.set_xticks([2, 4, 6, 8, 9], minor=True)
        ax.xaxis.grid(True, which='major')
        ax.xaxis.grid(True, which='minor')
        ax.yaxis.grid(True, which='major')
    else:
        plt.legend(loc="upper right")
        ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.7, 0.8, 0.9, 1], minor=False)
        ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.7, 0.8, 0.9, 1], minor=False)
        ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.7, 0.8, 0.9, 1], minor=True)
        ax.xaxis.grid(True, which='major')
        ax.xaxis.grid(True, which='minor')
        ax.yaxis.grid(True, which='major')

    # function to show the plot
    plt.show()


def double_ax_plot_line(lines_top_ax, lines_bottom_ax, x_axis, x_label="", y_label="", colors=[], ylim=[0,1], xlim=[0,1], line_styles=[], linewidths=[], markers=[], marker_size=[], lv=1,
                        save_fig_to=None, add_zero_line=False, imax=0):

    cm = 1 / 2.54
    fig, ax = plt.subplots(2, sharex=True, figsize=(18 * cm, 12 * cm))
    top = 0
    bottom = 1
    lines = [lines_top_ax, lines_bottom_ax]
    ax_top = ax[0]
    ax_bottom = ax[1]
    if add_zero_line:
        for a in ax:
            zero_line = [0 for i in x_axis] + [0, 0]
            zero_line_x_axis = [x_axis[0] - 1] + x_axis + [x_axis[len(x_axis) - 1] + 1]
            a.plot(zero_line_x_axis, zero_line, color='grey', linestyle='dashed', linewidth=0.8)
    for pos in [top, bottom]:
        custom_colors = ['#1b9e77', '#d95f02', '#7570b3', '#2c7fb8', '#253494', '#dd1c77']
        l_style = "solid"
        custom_linewidth = 1
        #marker_face_color = "white"
        param_index = 0
        mark_every = None
        custom_marker_size = 0
        custom_marker = '.'
        for line_name in lines[pos].keys():
            if len(line_styles) > 0:
                l_style = line_styles[param_index % len(line_styles)]
            if len(linewidths) > 0:
                custom_linewidth = linewidths[param_index % len(linewidths)]
            if len(colors) > 0:
                custom_color = colors[param_index % len(colors)]
            else:
                custom_color = custom_colors[param_index % len(custom_colors)]
            if len(markers) > 0:
                custom_marker = markers[param_index % len(markers)]
            if len(marker_size) > 0:
                custom_marker_size = marker_size[param_index % len(marker_size)]
            marker_face_color = custom_color
            ax[pos].plot(x_axis, lines[pos][line_name], label=line_name, color=custom_color, linestyle=l_style, linewidth=custom_linewidth, marker=custom_marker, markerfacecolor=marker_face_color,
                         markersize=custom_marker_size, markevery=mark_every)
            param_index += 1

    t1 = "{}={}, {}={}, {}".format(r'$I_{max}$', imax, r'$q$', lv, "(1:1)")
    t2 = "{}={}, {}={}, {}".format(r'$I_{max}$', imax, r'$q$', lv, "(1:25)")

    ax_top.set_title(t1)
    ax_bottom.set_title(t2)

    ax_bottom.set_xlabel(x_label, fontsize=14)
    for a in ax:
        a.set_ylabel(y_label, fontsize=14)
        a.set_xlim(xlim[0], xlim[1])
        a.set_ylim(ylim[0], ylim[1])
        a.set_xticks(x_axis, minor=False)

    size = {'size': 11}
    handles, labels = ax[0].get_legend_handles_labels()
    models = ['RNG', 'GPA', 'GG', '5NN', 'YAO', 'ER']
    new_handles = []
    new_labels = []
    anchor = (1.135, 1)
    for model in models:
        for i in range(len(labels)):
            if model in labels[i]:
                model_index = i
                break
        new_labels.append(model)
        new_handles.append(handles[model_index])

    legend = ax_top.legend(new_handles, new_labels, loc='upper right', bbox_to_anchor=anchor, prop=size, edgecolor="black")
    legend.get_frame().set_alpha(None)

    if save_fig_to:
        plt.savefig(save_fig_to, dpi=300, bbox_inches='tight', pad_inches=0.002)
    # function to show the plot
    plt.show()


def n_line_plot(lines, x_axis, title, errors=None, color_pairs=False, double_pair_color=False, ylim=[0,1],
                xlim=[0,1],xlabel="(1 - p)", ylabel=r'$G_L$', c_list=None, line_style=None,
                line_size=None, marker_size=None, markers=None, deg_dist=False, savefig_to=None, use_titles=None, err_c=None):
    custom_colors = ['#1b9e77', '#d95f02', '#7570b3', '#2c7fb8', '#253494','#dd1c77']
    custom_marker_color = ['#1b9e77', '#d95f02', '#7570b3','#1b9e77', '#d95f02', '#7570b3','#1b9e77', '#d95f02', '#7570b3']
    custom_marker = ['o', "^", 'o', "^",'o', "^",'o', "^",'o', "^",'o', "^",]
    custom_linewidth = 1.8
    custom_marker_size = 0
    half = 10000
    marker_face_color = None
    mark_every = None
    if xlim != [0, 1]:
        custom_marker_size = 8
    if color_pairs:
        custom_colors = ['#006837','#7aa711', #RNG
                         '#cc4c02','#ec7014', #GG
                         '#ae017e','#dd3497', #5NN
                         '#3182bd','#6baed6',
                         '#54278f','#807dba',
                         '#b30000','#e34a33'
        ]
        custom_marker_color = ['#d95f0e','#fe9929','#c51b8a','#f768a1','#3182bd','#6baed6','#31a354','#74c476','#54278f','#756bb1','#b30000','#e34a33']
    if double_pair_color:
        model_colors = {"RNG": {"light": '#7aa711', "dark": '#006837', "st": '#556a4d'},
                        "GG": {"light": '#ec7014', "dark": '#cc4c02', "st": '#695442'},
                        "5NN": {"light": '#dd3497', "dark": '#ae017e', "st": '#824a81'}}
        light_colors = ['#7aa711', '#ec7014', '#ae017e']
        dark_colors = ['#009179', '#f7c81e', '#8506b8']
        half = len(lines)/2
        base_colors = light_colors + dark_colors
        custom_marker = []
        custom_colors = []
        for i in range(len(lines)):
            if i < half:
                custom_marker.append('o')
                custom_colors.append(base_colors[i % 6])
            else:
                custom_marker.append("v")
                #custom_colors.append(dark_colors[i % 3])
        custom_colors += custom_colors
        custom_marker_color = custom_colors

        # custom_marker = ['o','o','o','o','o','o',^,"^","^","^","^","^"]
        #custom_colors = ['#d95f0e','#c51b8a','#3182bd','#31a354','#54278f','#b30000',
        #                 '#d95f0e','#c51b8a','#3182bd','#31a354','#54278f','#b30000']
        #custom_marker_color = ['#d95f0e','#c51b8a','#3182bd','#31a354','#54278f','#b30000','#d95f0e','#c51b8a','#3182bd','#31a354','#54278f','#b30000']
    if errors:
        cm = 1 / 2.54
        fig, ax = plt.subplots(2, sharex=True, figsize=(20*cm, 18*cm))
    else:
        fig, ax = plt.subplots()
    i = 0
    if errors:
        j = 0
        color_index = 0
    for line_name in lines:
        l_style = "solid"
        if c_list:
            custom_colors = c_list
        if line_style:
            l_style = line_style[i]
        if line_size:
            custom_linewidth = line_size[i]
        if markers:
            custom_marker = markers
            custom_marker_size = marker_size[i]
            mark_every = 0.2
            marker_face_color = '#ffffff'
        if deg_dist:
            #marker_face_color = '#ffffff'
            custom_marker_size = 10
        if errors:
            if err_c:
                error_colors = err_c
            else:
                error_colors = ['#7aa711', '#807dba', '#ec7014', '#dd3497', '#6baed6', '#B99D22']
            error = errors[line_name]
            custom_marker_size = 7
            custom_linewidth = 1.5
            custom_marker = "."

            color = error_colors[color_index % (len(error_colors))]
            if j == 1:
                color_index += 1

            marker_face_color = color

            ax[j].errorbar(x_axis, lines[line_name], yerr=error, label=line_name, color=color, linestyle=l_style,
                    linewidth=custom_linewidth,
                    marker=custom_marker, markerfacecolor=marker_face_color,
                    markersize=custom_marker_size,
                    markevery=mark_every, capsize=3)

            j = (j+1) % 2

        else:
            ax.plot(x_axis, lines[line_name], label=line_name, color=custom_colors[i % len(custom_colors)], linestyle=l_style,
                    linewidth=custom_linewidth,
                    marker=custom_marker[i], markerfacecolor=marker_face_color,
                    markersize=custom_marker_size,
                    markevery=mark_every)

        i += 1

    if not errors:
        # setting x and y axis range
        plt.ylim(ylim[0], ylim[1])
        plt.xlim(xlim[0], xlim[1])
        # naming the x axis
        plt.xlabel(xlabel, fontsize=15)
        # giving a title to my graph
        plt.title(title)
        # naming the y axis
        plt.ylabel(ylabel, fontsize=18)

        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)
        plt.rc('legend', fontsize=10)

    else:

        plt.ylim(ylim[0], ylim[1])
        plt.xlim(xlim[0], xlim[1])
        title = title.split("(")[0]
        lv = title.split(" ")[1]
        if not use_titles:
            t1 = "{}={}, {}".format(r'$q$', lv, "(1:1)")
            t2 = "{}={}, {}".format(r'$q$', lv, "(1:25)")
        else:
            t1 = "{}={}, {}".format(r'$q$', lv, "(1:25)")
            t2 = "{}={}, {}, bridge nodes with extra interlinks".format(r'$q$', lv, "(1:25)")
        ax[0].set_title(t1)
        ax[1].set_title(t2)

        ax[1].set_xlabel(xlabel, fontsize=14)
        for a in ax:
            a.set_ylabel(ylabel, fontsize=14)
        if err_c:

            anchor = (1.03, 0.485)
            size = {'size': 10.5}
            handles, labels = ax[0].get_legend_handles_labels()
            new_handles = []
            new_labels = []
            model_name = labels[0].split(")")[1]
            model_name = model_name.replace(" ", "")
            strategies_titles = {'Original': 'simple graphs', 'Distance': 'distance_aux', 'Local hubs': 'local_hubs', 'Degree': 'degree_aux', 'Random': 'random', 'Distance+': 'distance 2'}
            t1 = "{}, {}={}, {}".format(model_name, r'$q$', lv, "(1:1)")
            t2 = "{}, {}={}, {}".format(model_name, r'$q$', lv, "(1:25)")
            ax[0].set_title(t1)
            ax[1].set_title(t2)
            for st in strategies_titles.keys():
                new_label_name = "{}".format(st)
                for i in range(len(labels)):
                    if strategies_titles[st] in labels[i]:
                        st_index = i

                        new_labels.append(new_label_name)
                        new_handles.append(handles[st_index])

        else:
            size = {'size': 12}
            handles, labels = ax[0].get_legend_handles_labels()
            models = ['RNG', 'GPA', 'GG', '5NN', 'YAO', 'ER']
            new_handles = []
            new_labels = []
            anchor = (1.135, 1)
            for model in models:
                for i in range(len(labels)):
                    if model in labels[i]:
                        model_index = i
                        break
                new_labels.append(model)
                new_handles.append(handles[model_index])

        legend = ax[0].legend(new_handles, new_labels, loc='upper right', bbox_to_anchor=anchor, prop=size, edgecolor="black")
        legend.get_frame().set_alpha(None)

    if xlim == [0, 1]:
        plt.legend(loc="upper right")
        ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.7, 0.8, 0.9, 1], minor=False)
        ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.7, 0.8, 0.9, 1], minor=False)
        ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.5, 0.7, 0.8, 0.9, 1], minor=True)
    elif ylim[1] < 2:
        plt.legend(loc="lower left")
        if len(lines) > half:
            plt.legend(loc="lower left", ncol=2, prop={'size': 11.8})

        ax.set_xticks(x_axis, minor=False)
        more_y_ticks = [ylim[0]]
        sum = 0.01
        if ylim[0] < 0.89:
            for i in range(int(ylim[0]*100), 89):
                more_y_ticks.append(ylim[0]+sum)
                sum += 0.01

        y_ticks = more_y_ticks + [0.9, 0.91, 0.92, 0.93, 0.94, 0.96, 0.95, 0.97, 0.98, 0.99, 1]
        y_ticks = [x for x in y_ticks if x >= ylim[0]]
        ax.set_yticks(y_ticks, minor=False)
        ax.set_xticks(x_axis, minor=True)
    else:
        if deg_dist:
            plt.legend(loc="upper right")
        else:
            if not errors:
                plt.legend(loc="upper left")
        if errors:

            for a in ax:
                a.set_xticks(x_axis, minor=False)

                # y_ticks = range(ylim[0], ylim[1],10)
                # ax.set_yticks(y_ticks, minor=True)
                y_ticks = range(ylim[0], ylim[1], 200)
                a.set_yticks(y_ticks, minor=False)
                a.set_xticks(x_axis, minor=True)

        else:
            ax.set_xticks(x_axis, minor=False)

            # y_ticks = range(ylim[0], ylim[1],10)
            # ax.set_yticks(y_ticks, minor=True)
            y_ticks = range(ylim[0], ylim[1], 100)
            ax.set_yticks(y_ticks, minor=False)
            ax.set_xticks(x_axis, minor=True)
    if not errors:
        ax.xaxis.grid(True, which='major')
        ax.xaxis.grid(True, which='minor')
        ax.yaxis.grid(True, which='major')
    else:
        for a in ax:
            #a.xaxis.grid(True, which='major')
            a.xaxis.grid(True, which='minor')
            #a.yaxis.grid(True, which='major')
    if savefig_to:
        plt.savefig(savefig_to, dpi=300, bbox_inches='tight', pad_inches=0.002)
    # function to show the plot
    plt.show()


def plot_bar(labels, n_bars, plot_list, data_labels, ylabel, xlabel, title, yerr_list=None, colors=None, ax=None):

    x = np.arange(len(labels))  # the label locations
    width = 1*0.9/n_bars  # the width of the bars
    if not colors:
        colors = ['#dfc27d', '#8c510a','#bf812d',
                  '#35978f','#80cdc1',  '#01665e']
        #colors = ['#ec7014', '#807dba','#7aa711', '#dd3497', '#6baed6', '#B99D22']
    if ax:
        received_ax = True
    else:
        received_ax = False
    if not received_ax:
        fig, ax = plt.subplots()

    rects = []
    first_half = int(n_bars/2)

    error = 0
    if n_bars % 2 != 0:
        error = 0
    e2 = 0.5
    for i in range(first_half):
        if yerr_list:
            rects.append(ax.bar(x - width * (i + error + e2), plot_list[i], width, label=data_labels[i], yerr=yerr_list[i], color=colors[i]))
        else:
            rects.append(ax.bar(x - width*(i+error+e2), plot_list[i], width, label=data_labels[i], color=colors[i]))
    second_half = first_half
    if n_bars % 2 != 0:
        if yerr_list:
            rects.append(ax.bar(x, plot_list[first_half], width, label=data_labels[first_half], yerr=yerr_list[first_half], color=colors[i]))
        else:
            rects.append(ax.bar(x, plot_list[first_half], width, label=data_labels[first_half], color=colors[i]))
        second_half += 1
    for i in range(second_half, n_bars):
        j = i - second_half
        if yerr_list:
            rects.append(ax.bar(x + width * (j + error + e2), plot_list[i], width, label=data_labels[i], yerr=yerr_list[i], color=colors[i]))
        else:
            rects.append(ax.bar(x + width * (j+error+e2), plot_list[i], width, label=data_labels[i], color=colors[i]))

    if not received_ax:
        # Add some text for labels, title and custom x-axis tick labels, etc.
        plt.xlabel(xlabel, fontsize=15)

        # naming the y axis
        plt.ylabel(ylabel, fontsize=18)

        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)

        plt.rc('legend', fontsize=13)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        ax.legend()

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            note = ""#'{}'.format(height)

            ax.annotate(note,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    for rect in rects:
        autolabel(rect)
    if not received_ax:
        fig.tight_layout()

        plt.show()
    else:
        return ax


def double_plot_bar(labels, n_bars, plot_list, data_labels, ylabel, xlabel, title, yerr_list=None, colors=None, savefig_to=None):
    cm = 1 / 2.54
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(20*cm, 15*cm))
    labels_1 = labels[0]
    labels_2 = labels[1]
    n_bars1 = n_bars[0]
    n_bars2 = n_bars[1]
    plot_list1 = plot_list[0]
    plot_list2 = plot_list[1]
    data_labels1 = data_labels[0]
    data_labels2 = data_labels[1]
    title1 = title[0]
    title2 = title[1]
    yerr_1 = yerr_list[0]
    yerr_2 = yerr_list[1]

    ax1 = plot_bar(labels_1, n_bars1, plot_list1, data_labels1, "", xlabel, title1, yerr_list=yerr_1, ax=ax1)
    ax2 = plot_bar(labels_2, n_bars2, plot_list2, data_labels2, "", xlabel, title2, yerr_list=yerr_2, ax=ax2)

    for ax in (ax1, ax2):
        ax.set_ylabel(ylabel, fontsize=14)

    ax2.set_xlabel(xlabel, fontsize=14)

    handles, labels = ax1.get_legend_handles_labels()
    models = ['RNG', 'GPA', 'GG', '5NN', 'YAO', 'ER']
    new_handles = []
    new_labels = []
    for model in models:
        model_index = labels.index(model)
        new_labels.append(model)
        new_handles.append(handles[model_index])

    legend = ax1.legend(new_handles, new_labels, loc='upper right', bbox_to_anchor=(1.135, 1), prop={'size': 12}, edgecolor="black")
    legend.get_frame().set_alpha(None)

    #title = title[0].split("(")[0]
    #t1 = "{} {}".format(title, "(1:1)")
    #t2 = "{} {}".format(title, "(1:25)")
    ax1.set_title(title1)
    ax2.set_title(title2)
    if savefig_to:
        plt.savefig(savefig_to, dpi=300, bbox_inches='tight', pad_inches=0.002)
    plt.show()


def scatter_plot(models, geometry, strategy, ndep, radius, map="models", legacy=False, lv=1, save_fig=False, return_data=False, is_seismic=False, chapter=6):
    up_group = []
    low_group = []
    HDLA = {}
    print(strategy)
    if geometry == "20x500":
        shape = "(1:25)"
    else:
        shape = "(1:1)"
    fig, ax = plt.subplots()

    i = 0
    model_map_shuffle_dict = {}
    for model in models:

        gl_inv, nodes_removed, nr, vers, other_data = dp.correlated_damage_vs_nodes_removed(model, geometry, strategy, ndep, radius, legacy=legacy, lv=lv, is_seismic=is_seismic)

        z = np.ones(len(nodes_removed))
        p = [x/2000 for x in nodes_removed]

        if map == "models":

            custom_colors = {"RNG": '#7aa711',
                            "GPA": '#807dba',
                            "5NN": '#dd3497',
                            "YAO": '#6baed6',
                            "GG": '#ec7014',
                            "ER": '#B99D22'}
            custom_sizes = [20,20,20,20,20,20]
            title = "Localized attack over {} systems".format(shape)
            if strategy != "simple graphs":
                title = "Localized attack over {} + {} systems".format(shape, strategy)
            up_group += [(1-x) for x in gl_inv if (1-x) > 0.5]
            low_group += [(1-x) for x in gl_inv if (1-x) <= 0.5]

            gl_list = [(1 - x) for x in gl_inv]

            r_size_list = [x * custom_sizes[i] for x in z]

            c_list = [custom_colors[model] for z in p]

            first_third = {"p": p[0:333], "gl": gl_list[0:333], "s": r_size_list[0:333], "c": c_list[0:333]}
            second_third = {"p": p[333:666], "gl": gl_list[333:666], "s": r_size_list[333:666], "c": c_list[333:666]}
            third_third = {"p": p[666::], "gl": gl_list[666::], "s": r_size_list[666::], "c": c_list[666::]}

            model_map_shuffle_dict[model] = [first_third, second_third, third_third]

            #ax.scatter(p, [(1 - x) for x in gl_inv], s=[x * custom_sizes[i] for x in z], alpha=1,
            #          c=[custom_colors[model] for z in p],
            #           label=model)

        if map == "magnitude" and is_seismic:
            print(model)

            title = "Magnitude of seismic attacks for {} based systems".format(model)
            magnitude = []
            p = []
            gl = []
            Mw_high = []
            Mw_low = []
            max_nodes_rem = 0
            mnr_mw = 0
            max_mw = 0
            mm_nrem  = 0
            for k in range(len(nr)):
                gl.append(1-gl_inv[k])
                magnitude.append(other_data["Mw"][k])
                p.append(nodes_removed[k]/2000)
                if nodes_removed[k]/2000 == 0:
                    if 1-gl_inv[k] < 1:
                        print("????")

            z = np.ones(len(p))
            print("min (1-p): {}, max: {}".format(min(p),max(p)))
            plt.scatter(p, gl, s=[x * 10 for x in z], alpha=1, c=magnitude, cmap='viridis_r',
                        label=model)

        if map == "find":
            print(model)
            data = dp.read_scatter_plot_data(model, ndep, geometry, radius, strategy, legacy=legacy, lv=lv, is_seismic=is_seismic)
            is_l50 = data["isl50"]
            title = "Is {} removed during the cascading failure? {}. {}".format(r'$u_L^b$', shape, model)
            if strategy != "simple graphs":
                title += " + {}".format(strategy)
            color_true = '#f03b20'
            color_false = '#252525'
            color_list = []
            p_aux_1 = []
            gl_aux_1 = []
            p_aux_2 = []
            gl_aux_2 = []

            if is_seismic:
                Mw_high = []
                Mw_low = []
            for k in range(len(nr)):
                if is_l50[k]:
                    color_list.append(color_true)
                    center = (other_data["x_center"][k], other_data["y_center"][k])
                    #print("HDLA in model: {}, version: {}, {}".format(model, vers[k], center))
                    p_aux_1.append(p[k])
                    gl_aux_1.append(1-gl_inv[k])
                    if is_seismic:
                        Mw_low.append(other_data["Mw"][k])
                else:
                    color_list.append(color_false)
                    p_aux_2.append(p[k])
                    gl_aux_2.append(1 - gl_inv[k])
                    if is_seismic:
                        Mw_high.append(other_data["Mw"][k])
                    if gl_inv[k] > 0.5:
                        print("mlem")
            if is_seismic:
                print("HDLA Mw = ({},{})".format(min(Mw_low), max(Mw_low)))
                print("Non-HDLA Mw = ({},{})".format(min(Mw_high), max(Mw_high)))
            size = 20
            if model == models[(len(models) - 1)]:
                ax.scatter(p_aux_1, gl_aux_1, s=[x * size for x in np.ones(len(p_aux_1))], alpha=1, c=color_true,
                           label="{} in CF".format(r'$u_L^b$'),edgecolor='black', linewidth=0.2)
                ax.scatter(p_aux_2, gl_aux_2, s=[x * size for x in np.ones(len(p_aux_2))], alpha=1, c=color_false,
                           label="{} not in CF".format(r'$u_L^b$'),edgecolor='gray', linewidth=0.1)
            else:
                ax.scatter(p_aux_1, gl_aux_1, s=[x * size for x in np.ones(len(p_aux_1))], alpha=1, c=color_true
                    ,edgecolor='black', linewidth=0.2)
                ax.scatter(p_aux_2, gl_aux_2, s=[x * size for x in np.ones(len(p_aux_2))], alpha=1, c=color_false
                           ,edgecolor='gray', linewidth=0.1)

            if p_aux_1 == []:
                p_aux_1.append(-1)
            if p_aux_2 == []:
                p_aux_2.append(-1)
            print("min (1-p): {}, max: {}".format(min(min(p_aux_1), min(p_aux_2)), max(max(p_aux_1), max(p_aux_2))))
            #ax.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=color_l, label=model)
            print("Total points: {}, HDLA: {}".format(len(color_list), len([x for x in color_list if x == color_true])))
            HDLA[model] = len([x for x in color_list if x == color_true])

        elif map == "betweenness":
            print(model)
            title = "Localized attacks over {} systems\nmax(betweenness) of logical nodes removed.".format(shape)
            if strategy != "simple graphs":
                title = "Localized attacks over {} + {}\nmax(betweenness) of logical nodes removed.".format(shape, strategy)
            data = dp.read_scatter_plot_data(model, ndep, geometry, radius, strategy, legacy=legacy)
            betweenness = data["betweenness"]

            blep = []
            for k in range(len(nr)):
                if gl_inv[k] >= 0.5 and betweenness[k] < 0.35:
                    blep.append(k)
            blepi = [x for x in gl_inv if x >= 0.5]
            print("{} of {} do not remove L50".format(len(blep), len(blepi)))

            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=betweenness, cmap='viridis_r',
                       label=model)
        elif map == "degree":
            title = "{} localized attacks: {}".format(shape,map)
            c = []
            for k in range(len(nr)):
                node_list = nr[k]
                # sacar el betweenness normalizado
                internode_list = dp.get_internodes_from_list(node_list, geometry, ndep)

                failed_nodes = dp.get_failed_logic_nodes(internode_list, geometry, ndep)
                betweenness = dp.logic_node_degree(failed_nodes)
                # average betweenness of removed logic nodes
                bet = []
                for b in betweenness:
                    bet.append(b[1])
                if len(bet) > 0:
                    c.append(np.mean(bet))
                else:
                    c.append(0)
                    print(failed_nodes)
            # colormapthing

            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=c, cmap='viridis',
                       label=model)
        elif map == "physical":
            title = "{} localized attacks: {}".format(shape, map)
            data = dp.read_scatter_plot_data(model, ndep, geometry, radius, strategy, legacy=legacy)
            c = data["physic damage"]

            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=c, cmap='viridis_r',
                            label=model)
        elif map == "diff":
            title = "{} localized attacks: {}".format(shape, map)
            c = []
            for k in range(len(nr)):
                dif = dp.difference_on_logic_nodes_removed(nr[k], geometry, ndep, vers[k], model)
                if dif < 20 and (1-gl_inv[k]) < 0.5:
                    print(vers[k])
                    print(nr[k])
                    print(dif)
                elif dif > 20 and (1-gl_inv[k] < 0.5):
                    print("high")
                    print(dif)
                c.append(dif)

            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=c, cmap='viridis',
                            label=model)
        elif map == "logical":

            title = "{} localized attacks: {}".format(shape, map)
            data = dp.read_scatter_plot_data(model, ndep, geometry, radius, strategy, legacy=legacy)
            c = data["logic damage"]

            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=c, cmap='viridis',
                            label=model)
        elif map == "logical+physical":

            title = "{} localized attacks: {}".format(shape, map)
            c = []
            for k in range(len(nr)):
                node_list = nr[k]
                # sacar el betweenness normalizado
                internode_list = dp.get_internodes_from_list(node_list, geometry, ndep)

                failed_nodes = dp.get_failed_logic_nodes(internode_list, geometry, ndep)
                logic_damage = 1-dp.gl_after_removal(failed_nodes, ndep)
                physical_damage = 1-dp.functional_physical_nodes_after_removal(nr[k], model, vers[k], ndep, geometry, strategy=strategy)
                total_damage = logic_damage+physical_damage
                c.append(total_damage)

            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=c, cmap='viridis',
                        label=model)

        elif map == "p_providers":
            title = "{} localized attacks: {}".format(shape, map)
            c = []
            for k in range(len(nr)):
                print (dp.amount_of_providers_in_node_list(nr[k], geometry, ndep))
                c.append(len(dp.amount_of_providers_in_node_list(nr[k], geometry, ndep)))
            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=c, cmap='jet',
                        label=model)
        elif map == "interlinks":
            title = "{} localized attacks: {}".format(shape, map)
            c = []
            for k in range(len(nr)):
                inter_degree = dp.get_interdegree_distribution_from_list(nr[k], geometry, ndep)

                total_inter_l = dp.get_total_interlinks(inter_degree)
                c.append(total_inter_l/len(nr[k]))
            plt.scatter(p, [(1 - x) for x in gl_inv], s=[x * 10 for x in z], alpha=1, c=c, cmap='jet',
                        label=model)
        i += 1
    plt.rc('legend', fontsize=13)
    if map == "models":
        plt.rc('legend', fontsize=10)
        if len(up_group) > 0:
            print("up range ({},{})".format(min(up_group), max(up_group)))
        if len(low_group) > 0:
            print("low range ({},{})".format(min(low_group), max(low_group)))

        # order: 1- RNG (0), GG (1), 5NN(2) 2- GG(3), 5NN(4), RNG(5) 3- 5NN(6), RNG(7), GG(8)
        order_list = ["RNG", "GG", "5NN", "ER", "YAO", "GPA",
                      "GG", "ER", "YAO", "GPA", "5NN", "RNG",
                      "5NN", "RNG", "ER", "YAO", "GPA", "GG"]
        total_points = 0
        for i in range(len(order_list)):
            total_points += len(model_map_shuffle_dict[model][i % 3]["p"])
            model = order_list[i]
            ax.scatter(model_map_shuffle_dict[model][i % 3]["p"],
                       model_map_shuffle_dict[model][i % 3]["gl"],
                       s=model_map_shuffle_dict[model][i % 3]["s"], alpha=1,
                       c=model_map_shuffle_dict[model][i % 3]["c"],
                       label=model if i < len(models) else "", edgecolors='black', linewidth=0.3)

        ax.legend(loc='lower left')
        print(total_points)
    if map == "find":
        ax.legend(loc='lower left')
    elif map != "find" and map != "models":
        cbar = plt.colorbar()
        cbar.set_label(map, fontsize=15)

    if is_seismic and map != "models" and map != "magnitude":
        ax.legend(loc='center left', bbox_to_anchor=(0, 0.62))
    elif is_seismic and map == "models":
        plt.rc('legend', fontsize=9.5)
        ax.legend(loc='center left', bbox_to_anchor=(0.01, 0.68))

    plt.ylim(-0.01, 1.02)
    if geometry == "20x500":
        if not is_seismic:
            plt.xlim(0.039, 0.0905)
        else:
            plt.xlim(-0.001, 0.106)
    else:
        plt.xlim(0.0455, 0.1465)

    plt.ylabel(r'$G_{L}$', fontsize=18)
    plt.xlabel('(1 - p)', fontsize=15)

    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], minor=False)
    ax.yaxis.grid(True, which='minor')
    ax.axhline(0, color='gray', linewidth=1, linestyle='dotted')
    ax.axhline(0.5, color='gray', linewidth=1, linestyle='dotted')
    ax.axhline(1, color='gray', linewidth=1, linestyle='dotted')

    st_name = strategy.split(" ")
    st_name = st_name[0]
    st_name = st_name.replace("_aux", "")
    space_fig_name = {"20x500": "ln", "100x100": "sq"}
    fig_name = 'cap{}_scatter_ndep_{}_{}_{}_{}.png'.format(chapter,ndep, map, st_name, space_fig_name[geometry])

    if save_fig:
        print(fig_name)
        fig_path = '../figures/cap{}/{}'.format(chapter, fig_name)
        plt.savefig(fig_path, dpi=300, bbox_inches='tight', pad_inches=0.002)
    plt.title("")

    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    if not return_data:
        plt.show()
    else:
        plt.clf()
        if map == 'models':
            return up_group, low_group
        if map == 'find':
            total_hdla = 0
            for key in HDLA:
                total_hdla += HDLA[key]
            HDLA['total'] = total_hdla
            return HDLA


def write_stuff(geometry, strategy, ndep=3, lv=1, use_legacy=False, use_model=[], is_seismic=False, mode="minimal"):
    print(ndep)
    all_data = dp.run_data()
    if len(use_model) > 0:
        models = use_model
    else:
        models = all_data["models"]

    radius = 20
    print("Starting {}, {} ...".format(strategy, geometry))
    start_time = datetime.datetime.now()
    versions_time = []
    scatter_plot_path = all_data["scatter_plot_path"][strategy]

    for model in models:

        gl_inv, nodes_removed, nr, vers, other = dp.correlated_damage_vs_nodes_removed(model, geometry, strategy, ndep, radius, legacy=use_legacy, lv=lv, is_seismic=is_seismic)

        is_l50 = []
        bet_list = []
        logic_damage = []
        physic_damage = []
        versions_viewed = []
        total_ver_count = Counter(vers)
        current_ver = 1
        for k in range(len(nr)):
            if vers[k] != current_ver:
                versions_time.append(datetime.datetime.now())
            current_ver = vers[k]
            versions_viewed.append(current_ver)
            current_count = Counter(versions_viewed)

            print("Model: {} {}, v{}: , {}/{}".format(model, geometry, current_ver, current_count[current_ver], total_ver_count[current_ver]))

            pnode_list = nr[k]

            # find

            is_l50.append(dp.is_removed_during_attack(['l50'], pnode_list, model, vers[k], ndep, geometry, strategy=strategy))


            if mode == "minimal":
                bet_list.append(-1)
            else:
                # betweenness
                failed_nodes = dp.get_all_logical_nodes_lost_from_original_pnode_list(pnode_list, model, vers[k], geometry, ndep, strategy)
                betweenness = dp.logic_node_betweenness(failed_nodes, "logic_exp_2.5_v{}.csv".format(lv))
                # average betweenness of removed logic nodes
                bet = []

                for b in betweenness:
                    bet.append(b[1] / ((300 - 1) * (300 - 2)))
                if len(bet) > 0:
                    bet_list.append(max(bet))
                else:
                    bet_list.append(0)

            # logical damage
            if mode == "minimal":
                logic_damage.append(-1)
            else:
                internode_list = dp.get_internodes_from_list(pnode_list, ndep)

                failed_nodes = dp.get_failed_logic_nodes(internode_list, ndep)

                logic_damage.append(dp.gl_after_removal(failed_nodes, ndep))

            # physical damage
            if mode == "minimal":
                physic_damage.append(-1)
            else:
                physic_damage.append(1 - dp.functional_physical_nodes_after_removal(nr[k], model, vers[k], ndep, geometry, strategy=strategy))
        end_time = datetime.datetime.now()
        if use_legacy:
            f_name = "legacy_"
        if lv:
            f_name = "lv{}_".format(lv)
        else:
            f_name = ""
        f_name += "scatter_plot_data_model_{}_ndep_{}_geometry_{}_radius_{}_st_{}.csv".format(model, ndep, geometry, radius, strategy)
        if is_seismic:
            file_path = os.path.join(scatter_plot_path, "seismic", f_name)
        else:
            file_path = os.path.join(scatter_plot_path, f_name)
        print("writing '{}'".format(file_path))

        with open(file_path, mode='w') as file:

            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['betweenness', 'is_l50', 'logic_damage', 'physic_damage'])
            for k in range(len(nr)):
                file_writer.writerow([str(bet_list[k]), str(is_l50[k]), str(logic_damage[k]), str(physic_damage[k])])

        print("Start time: {} - End time: {}".format(start_time, end_time))
        i = 1
        for t in versions_time:
            print("Version {}: {}".format(i, t))
    print("Finished {}, {} ...".format(strategy, geometry))






