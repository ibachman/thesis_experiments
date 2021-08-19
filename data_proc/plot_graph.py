import plotly.graph_objects as go

import data_proc.data_processing as dp

#G = nx.random_geometric_graph(200, 0.125)

geometry = "20x500"
model = "RNG"
#G = dp.create_nx_graph(geometry, model, "1")
#G = dp.create_nx_graph(geometry, model, "1", extra_edges="degree")
#G = dp.create_nx_graph(geometry, model, "1", extra_edges="distance")
#
G = dp.create_nx_graph(geometry, model, "9", extra_edges="random")
dimensions = geometry.split("x")
space = (int(dimensions[0]), int(dimensions[1]))
zoom_factor = 7.5
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
    line=dict(width=1, color='#888'),
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
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=False,
        color=[],
        size=5,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=0.5))
node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: {}, pos: ({})'.format(len(adjacencies[1]), G.nodes[adjacencies[0]]['pos']))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
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