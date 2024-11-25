import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import manhattan_distances
from sklearn.metrics.pairwise import cosine_similarity
import random
import networkx as nx
import plotly.graph_objects as go


def avg_score_bar(avg_scores, x_axis):
    plt.bar(x_axis, avg_scores)
    plt.xlabel("Optimal and Shuffle Iterations")
    plt.ylabel("Average Similarity Scores")
    plt.title("1000 Songs (Euclidean), H = 5 iterations")
    plt.savefig('test_images/bar.png')
    plt.close()


def display_mst(mst_edges, filename):
    # Create a new graph
    G = nx.Graph()

    # Add edges based on MST
    for edge in mst_edges:
        # Avoid self loops
        if edge[1] != edge[3]:
            G.add_edge(edge[1], edge[3], weight=f"{edge[0]:.2f}")

    # Compute layout of graph using spring layout
    pos = nx.spring_layout(G)

    # Extract x and y edges for scatter plot edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Create scatter plot for edges
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Extract x and y for nodes
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    # Create a scatter plot for nodes
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=5,
            colorbar=dict(
                thickness=15,
                title='MST',
                xanchor='left',
                titleside='right'
            )
        )
    )

    # count connections
    node_adj = []
    node_text = []
    for node, adj in enumerate(G.adjacency()):
        node_adj.append(len(adj[1]))
        node_text.append('# of connections: ' + str(len(adj[1])))

    # Set text for each node
    node_trace.text = node_text

    # Create figure with edge and node traces
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    # Save figure
    fig.write_html("test_images/" + filename)

    plt.close()


# -------------------------------------------------------------------------------------------------------------------- #
# Randomly shuffles songs in playlist and gets the average similarity score across all songs. Does this n times.
# Returns list of average scores for n amount of shuffles.
# Also returns worst average and worst order.
def shuffle(avg_scores, opt_order, audio_features, itr_count):
    worst_shuffle = []
    worst_avg = 0
    order = list(range(len(opt_order)))
    sh_ord = opt_order.copy()
    for i in range(itr_count):
        # sh_ord = random.sample(order, len(opt_order))
        random.shuffle(sh_ord)
        curr_avg = get_avg_sim_score(sh_ord, audio_features)
        avg_scores.append(curr_avg)
        if curr_avg > worst_avg:
            worst_avg = curr_avg
            worst_shuffle = sh_ord
    return avg_scores, worst_shuffle, worst_avg


# Computes similarity score between song-i and song-j
def get_sim_score(songi_data, songj_data):
    af_score = euclidean_distances([songi_data], [songj_data])
    return af_score[0][0]


# Computes average similarity score across a specified order of songs.
def get_avg_sim_score(order, audio_features):
    sim_score = 0
    for idx, song in enumerate(order):
        if idx != len(order) - 1:
            score = get_sim_score(audio_features[order[idx]], audio_features[order[idx + 1]])
            sim_score += score
    return sim_score / len(order)


# Main method for class called by transition_order.py to perform all operations related to visualization creation.
def create_visuals_main(audio_features, naive_order, mst_order, mst_edges, all_edges, h_score):
    # Create avg_scores list and add the average score for the optimal order to it.
    avg_scores = []
    naive_score = get_avg_sim_score(naive_order, audio_features)
    avg_scores.append(naive_score)
    # mst_score = get_avg_sim_score(mst_order, audio_features)
    mst_score = 0
    avg_scores.append(mst_score)
    avg_scores.append(h_score)


    # Get average scores for a number of order shuffles.
    avg_scores, worst_order, worst_avg = shuffle(avg_scores, naive_order, audio_features, 20)

    # Make bar graph of avg_scores[]
    x_axis = range(1, len(avg_scores) - 2)
    x_axis = [str(x) for x in x_axis]
    x_axis = ["G", "M", "H"] + x_axis
    avg_score_bar(avg_scores, x_axis)

    # display_mst(mst_edges, "100_MST_edges_euc.html")
    # display_mst(all_edges, "100_edge_visual_euc.html")
