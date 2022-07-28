import data_proc.common_plots as cp
import numpy as np


def tgl_table_for_imax(ndep, just_middle=False, prefix=""):
    if len(prefix) > 1:
        if prefix[-1] != "_":
            prefix += "_"
    interlink_type = "provider_priority"
    interlink_version = 3
    strategy = "simple graphs"
    models = ['RNG', 'GPA', 'GG', '5NN', 'Yao', 'ER']
    spaces = [(20, 500), (100, 100)]
    lvs = list(range(1, 11))

    if not just_middle:
        print("\\begin{table}[h]")
        print("\\small")
        print("\\tabcolsep=0.11cm")
        print("\\begin{tabular}{|c|l|l|l|l|l|l|l|}")
        print("\\hline")
    print("\\multicolumn{8}{|c|}{$I_{max} = " + str(ndep) + "$}                            \\\\ \\hline")
    print("$q$ & space & RNG & GG & GPA & 5-NNG & Yao & ER \\\\ \\hline")
    for lv in lvs:
        for space in spaces:
            values = {}
            for model in models:
                lvs, curves_as_p = cp.get_curves_as_points(lv, interlink_type, interlink_version, model, ndep, space, strategy, add_to_title=prefix)
                p_means = np.round(np.mean(curves_as_p), 2)
                p_std = np.round(np.std(curves_as_p), 2)
                values[model] = ("{} ({})".format(p_means, p_std))
            if space == (20, 500):
                start_str = "\\multirow{2}{*}{"+str(lv)+"}  & (1:25) &"
                end_str = "\\\\ \\cline{2-8}"
            else:
                start_str = "                    & (1:1)  &"
                end_str = "\\\\ \\hline"
            middle_str = " {} & {} & {} & {} & {} & {} ".format(values['RNG'], values['GPA'], values['GG'], values['5NN'], values['Yao'], values['ER'])
            print("{} {} {}".format(start_str, middle_str, end_str))

    if not just_middle:
        print("\\end{tabular}")
        print("\caption{Average $TG_L$ results for $I_{max}="+str(ndep)+"$, standard deviation in parenthesis. Variable $q$ indicates the logical network version used. Averages were obtained across the 10 " \
                                                          "physical network instances for a given space and physical model.}")
        print("\\end{table}")


def tgl_longtable():
    ndeps = list(range(1, 11))
    print("{")
    print("\\small")
    print("\\tabcolsep=0.11cm")
    print("\\begin{longtable}{|c|l|l|l|l|l|l|l|}")
    print("\\hline")

    for ndep in ndeps:
        tgl_table_for_imax(ndep, just_middle=True)
    print("\\end{longtable}")
    print("}")



