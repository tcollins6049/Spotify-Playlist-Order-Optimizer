import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import pairwise_distances
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
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


def heat_map_creation(audio_features):
    df = pd.DataFrame(audio_features,
                      columns=['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                               'speechiness', 'valence'])

    similarity_matrix = 1 / (1 + pairwise_distances(df.T, metric='euclidean'))

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

    plt.savefig('saved_images/heat_map.png')


# Will be possibly used in the future to create 2d plots of all combinations of data
def scatter_pair_plots(audio_features):
    pass



def create_visuals_main(x, y, z, audio_features):
    # scatter_3d(x, y, z)
    # scatter_2d(x, y)
    heat_map_creation(audio_features)
