__author__ = 'ivana'


def graph_attacks(exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes, phys_nodes,
                  attack_type, model, it, extra_edges=""):
    # -ln 300 -pn 2000 -ia 1 -ls 6 -e 2.5 -x 20 -y 500 -v 1 -i 100 -at physical -r -m MRN
    # -ln 300 -pn 2000 -ia 1 -ls 6 -e 2.5 -x 20 -y 500 -v 1 -i 100 -at physical -r -m MRN -st random

    # simple graphs attacks

    the_array = []

    for n_inter in interdep_list:
        for lam in exp_list:
            for nprov in provider_list:
                for pair in dimension_list:
                    for v in version_list:
                        for m in model:
                            if extra_edges is "":
                                a = "-ln %d -pn %d -ia %d -ls %d -e %2.1f -x %d -y %d -v %d -i %s -at %s -r -m %s" % (
                                    logic_nodes, phys_nodes, n_inter, nprov,
                                    lam, pair[0], pair[1], v, it, attack_type, m)
                                the_array.append(a)
                            else:
                                a = "-ln %d -pn %d -ia %d -ls %d -e %2.1f -x %d -y %d -v %d -i %s -at %s -r -m %s -st %s" % (
                                    logic_nodes, phys_nodes, n_inter, nprov,
                                    lam, pair[0], pair[1], v, it, attack_type, m, extra_edges)
                                the_array.append(a)
    return the_array


def extra_edges(exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes, phys_nodes, model,
                type):
    # -ln 300 -pn 2000 -ia 1 -ls 6 -e 2.5 -x 20 -y 500 -v 1 -i 100 -it 1 -m MRN -me -st random
    the_array = []

    for n_inter in interdep_list:
        for lam in exp_list:
            for nprov in provider_list:
                for pair in dimension_list:
                    for v in version_list:
                        for m in model:
                            a = "-ln %d -pn %d -ia %d -ls %d -e %2.1f -x %d -y %d -v 1 -i 100 -it %d -m %s -me -st %s" % (
                                logic_nodes, phys_nodes, n_inter, nprov,
                                lam, pair[0], pair[1], v, m, type)
                            the_array.append(a)
    return the_array


def localized_attacks(radius, exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes,
                      phys_nodes, attack_type, model, it, extra_edges=""):
    the_array = graph_attacks(exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes,
                              phys_nodes, attack_type, model, it, extra_edges=extra_edges)
    modified_array = []
    radius_str = ""
    for r in radius:
        radius_str += str(r)+" "

    for line in the_array:

        modified_array.append("{} -lar {}".format(line,radius_str))
    return modified_array


def seismic_attacks(seismic_data_file, exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes,
                      phys_nodes, attack_type, model, it, extra_edges=""):

    # -ln 300 -pn 2000 -ia 3 -ls 6 -e 2.5 -x 20 -y 500 -v 1 -i 100 -at physical -r -m MRN -sf seismic_data.csv

    the_array = graph_attacks(exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes,
                              phys_nodes, attack_type, model, it, extra_edges=extra_edges)
    modified_array = []
    for line in the_array:
        modified_array.append("{} -sf {}".format(line, seismic_data_file))
    return modified_array


def create_phys_nets(model_list, versions):
    for model in model_list:
        for v in versions[model]:
            print("-m {} -v {} -cn".format(model, v))

model_l = ["RNG","GG"]
version_d = {"RNG": list(range(1, 11)),
             "GG": list(range(1, 11))}
create_phys_nets(model_l, version_d)

exp_list = [2.5] # 2.5, 2.7
interdep_list = [7, 1, 10, 3, 5] # 3, 30
provider_list = [6] # 6, 9
dimension_list = [(20, 500)]#, (100,100)] ,[56.568,707.1],[80,500],[46.19,866.025]]#,[1000,1000]]
version_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
logic_nodes = 300
phys_nodes = 2000
attack_type = 'physical'
model = ['MRN', 'GG', '5NN']
it = '100'
extra_ed = [""] #, "random","degree","distance"]
radius =[4, 8, 12, 16, 20]
the_array = []
seismic_data_file = 'seismic_data.csv'
for strategy in extra_ed:

    aux = seismic_attacks(seismic_data_file, exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes,
                      phys_nodes, attack_type, model, it, extra_edges=strategy)

    #aux = graph_attacks(exp_list, interdep_list, provider_list, [(100,100)], version_list, logic_nodes, phys_nodes,
    #                    attack_type, model, it, extra_edges=strategy)

    #aux = localized_attacks(radius, exp_list, interdep_list, provider_list, dimension_list, version_list, logic_nodes,
    #                  phys_nodes, attack_type, model, it, extra_edges=strategy)

    the_array += aux


#print(len(the_array))
#for i in range(len(the_array)):
#    print(str(the_array[i]))

