import CAIDA_data.data_handler as dh

path = "ipinfo_webpages/"

def query_asn_web_files():
    path = "ipinfo_webpages/"
    web_file = "AS52411.html"

    while True:
        asn_id = input("ASN? (*AS+number*):")
        if asn_id == "exit":
            break
        web_file = "{}.html".format(asn_id)
        dh.parse_ipinfowebpage(path + web_file)


def find_missing_chile_asn():
    asn_in_chile_asn_csv = list(dh.get_chile_asn().keys())
    print(len(asn_in_chile_asn_csv))
    asn_in_chile_asn_html = dh.parse_different_as_from_html(path + "Chile_ASN_summary.html")
    print(len(asn_in_chile_asn_html))
    missing_asn_list = []
    for asn in asn_in_chile_asn_html:
        if asn not in asn_in_chile_asn_csv:
            missing_asn_list.append(asn)
    return list(set(missing_asn_list))


use_file = ["asninfo_rels.csv", "20211201_as_rel2.csv"]
index = 1
edge_list, b = dh.get_caida_data_asn_as_directed_edges(use_file[index])

print(len(b))
graph = dh.make_directed_graph(use_file[index], use_html_names=True)
providers = dh.get_chile_providers_using_isp_marker(use_international_connection=use_file[index])

if index == 1:
    providers += ['61440', '270056', '266724', '272025', '271993', '51076', '272031']

bn2 = dh.get_bridge_nodes_directed_2(providers, graph)

exit(3)
dh.print_graph(graph, providers=providers, bridge_nodes=[], bn_providers=[], out_nodes=['266713','263702'], use_label=False)

bn = dh.get_all_bridge_nodes_directed(providers, graph)
print(len(bn))
