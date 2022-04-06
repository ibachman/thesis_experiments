import plotly.graph_objects as go

import data_proc.data_processing as dp

#G = nx.random_geometric_graph(200, 0.125)

geometry = "20x500"
model = "RNG"
#G = dp.create_nx_graph(geometry, model, "1")
#G = dp.create_nx_graph(geometry, model, "1", extra_edges="degree")
#G = dp.create_nx_graph(geometry, model, "1", extra_edges="distance")
#
providers = ['p914',
'p1246',
'p831',
'p376',
'p904',
'p1021',
'p43',
'p1963',
'p1926',
'p150',
'p1958',
'p1278',
'p577',
'p1699',
'p1566',
'p332',
'p1356',
'p17',
'p854',
'p1753',
'p4',
'p1954',
'p1171',
'p1343',
'p724',
'p860',
'p1492',
'p482',
'p388',
'p31',
'p1203',
'p137',
'p1688',
'p80',
'p434',
'p238',
'p439',
'p1392',
'p1680',
'p1701',
'p493',
'p1608',
'p1561',
'p761',
'p1135',
'p1494',
'p1446',
'p1981',
'p188',
'p867',
'p62',
'p1891',
'p1729',
'p231',
'p1363',
'p106',
'p653',
'p1104',
'p357',
'p1041']
color_removed_nodes = dp.check_logic_nodes_removed_immediately(models=[model])
use_index = 0
version_j = 10

G = dp.create_nx_graph(geometry, model, version_j)
dimensions = geometry.split("x")
space = (int(dimensions[0]), int(dimensions[1]))
zoom_factor = 4.4#7.5
if geometry == "20x500":
    zoom_factor = zoom_factor*3


edge_x = []
edge_y = []
for edge in G.edges():

    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#656363'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='Viridis',
        reversescale=True,
        color=[],
        size=8,
        colorbar=dict(
            thickness=8,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=0.7))
node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_name = adjacencies[0]
    pos = (round(G.nodes[node_name]['pos'][0], 3), round(G.nodes[node_name]['pos'][1], 3))

    node_text.append('name: {}, degree: {}, pos: {}'.format(node_name, len(adjacencies[1]), pos))

#node_trace.marker.color = node_adjacencies
color_using =[]
color_map = []
for node in G.nodes():
    if node in providers and node in color_removed_nodes[use_index]:
        color_map.append('black')
    elif node in providers and node not in color_removed_nodes[use_index]:
        color_map.append('red')
    elif node in ['p52', 'p1821', 'p651'] and node in color_removed_nodes[use_index]:
        color_using.append(10)
        color_map.append('#9d0ae2')
    elif node in ['p52', 'p1821', 'p651'] and node not in color_removed_nodes[use_index]:
        color_using.append(7)
        color_map.append('#e00ae2')
    elif node not in ['p52', 'p1821', 'p651'] and node in color_removed_nodes[use_index]:
        color_using.append(2)
        color_map.append('#ffba09')
    else:
        color_map.append('#e5ffb0')
        color_using.append(1)
node_trace.marker.color = color_map#color_using

node_trace.text = node_text
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(paper_bgcolor='#f8ffff', plot_bgcolor='#f8ffff',
                    title='<br>Network graph made with Python',
                    titlefont_size=16,
                    height=space[1] * zoom_factor,
                    width=space[0] * zoom_factor,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=5, l=5, r=5, t=5),
                    annotations=[dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.1, y=-0.1)],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
fig.show()