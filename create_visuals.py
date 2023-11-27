import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import pairwise_distances
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from sklearn.metrics.pairwise import euclidean_distances
import random
import itertools


# Creates a 3D scatter plot of the x and y data passed in.
def scatter_3d(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatters points in graph
    ax.scatter(x, y, z, c='blue', marker='o')

    # Connects points in given order
    for i in range(len(x) - 1):
        ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], [z[i], z[i + 1]], color='black')

    # Highlight the first point as green and last point as red
    ax.scatter(x[0], y[0], z[0], c='orange', marker='o')
    ax.scatter(x[-1], y[-1], z[-1], c='red', marker='o')

    # Set labels
    ax.set_xlabel('acousticness')
    ax.set_ylabel('danceability')
    ax.set_zlabel('energy')

    # Displays plot and saves to a file
    plt.savefig('org_scatter.png')
    # plt.show()


# Creates a 2D scatter plot of the x and y data passed in.
def scatter_2d(x, y):
    # Create scatter plot using x and y
    plt.scatter(x, y, c='blue', marker='o')

    # Connect points using black lines
    for i in range(len(x) - 1):
        plt.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color='black')

    # Highlight the first point as green and last as purple
    plt.scatter(x[0], y[0], c='green', marker='o')
    plt.scatter(x[-1], y[-1], c='purple', marker='o')

    # Set labels
    plt.xlabel('first features')
    plt.ylabel('last features')

    plt.savefig('2d_scatter.png')


def create_heat_map(org_features, order, filename, avg_score):
    print("LLLLLLLLLLLLLLL ", len(org_features))
    # Need to reorder audio features based on order
    audio_features = []
    for i in order:
        audio_features.append(org_features[i])

    df = pd.DataFrame(audio_features,
                      columns=['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                               'speechiness', 'valence'])
    print(df.shape)

    similarity_matrix = pairwise_distances(df.T, metric='euclidean')
    print(similarity_matrix.shape)

    colors = [
        (1.0, 1.0, 0.5),  # Yellow for low values
        (0.6, 0.8, 0.6),  # Green
        (0.7, 0.7, 0.7),  # Light gray
        (0.7, 0.7, 0.7),  # Light gray
        (0.7, 0.7, 0.7),  # Light gray
        (0.7, 0.7, 0.7),  # Light gray
        (0.1, 0.1, 0.1),  # Darker gray for high values
    ]
    cmap = LinearSegmentedColormap.from_list('custom_colormap', colors, N=256)

    plt.figure(figsize=(10, 8))

    sns.heatmap(similarity_matrix, annot=True, cmap=cmap, xticklabels=df.index, yticklabels=df.index)

    plt.title("Avg: " + str(avg_score))
    plt.savefig('saved_images/' + filename)


def avg_score_bar(avg_scores, x_axis):
    plt.bar(x_axis, avg_scores)
    plt.xlabel("Optimal and Shuffle Iterations")
    plt.ylabel("Average Similarity Scores")
    plt.savefig('saved_images/bar.png')


# -------------------------------------------------------------------------------------------------------------------- #
# Randomly shuffles songs in playlist and gets the average similarity score across all songs. Does this n times.
# Returns list of average scores for n amount of shuffles.
# Also returns worst average and worst order.
def shuffle(avg_scores, opt_order, audio_features, itr_count):
    worst_shuffle = []
    worst_avg = 0
    for i in range(itr_count):
        sh_ord = random.sample(opt_order, len(opt_order))
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
            score = get_sim_score(audio_features[song], audio_features[order[idx + 1]])
            sim_score += score
    return sim_score / len(order)


# Main method for class called by transition_order.py to perform all operations related to visualization creation.
def create_visuals_main(x, y, z, audio_features, opt_order):
    # Create avg_scores list and add the average score for the optimal order to it.
    avg_scores = []
    opt_score = get_avg_sim_score(opt_order, audio_features)
    avg_scores.append(opt_score)

    # Get average scores for a number of order shuffles.
    avg_scores, worst_order, worst_avg = shuffle(avg_scores, opt_order, audio_features, 20)

    # Pass opt order into heat map
    # create_heat_map(audio_features, opt_order, "opt_heat_map", opt_score)

    # Pass worst order into heat map

    # Make bar graph of avg_scores[]
    x_axis = range(1, len(avg_scores))
    x_axis = [str(x) for x in x_axis]
    x_axis = ["OPT"] + x_axis
    avg_score_bar(avg_scores, x_axis)
