from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import manhattan_distances
import data_prep as dp
import create_visuals as cv
from collections import defaultdict
import heapq
import random
import heuristic as hs


# ____________________________________________________________________________________________________________________ #
# Computes similarity score between song-i and song-j
def get_sim_score(songi_data, songj_data):
    af_score = euclidean_distances([songi_data], [songj_data])
    return af_score[0][0]


# Calculates an array of all edges in the original graph.
def get_edge_array(audio_features, song_uris):
    edge_array = []
    # First loop iterates over element using each one as a starting point
    for current_point in range(len(audio_features)):
        # Second loop iterates over each element again except now as an ending point
        for next_point in range(1, len(audio_features)):
            # If the starting and ending points aren't the same then we have found a new edge.
            # Compute the sim score and add that edge to the array.
            if current_point != next_point:
                sim_score = get_sim_score(audio_features[current_point], audio_features[next_point])
                appendable_item = [sim_score, current_point, 'E', next_point, 'B']
                edge_array.append(appendable_item)
        # 0 is the starting point for the ordering, so it can be ignored. Every other point will need a transition from
        # its beginning to its end of distance 0.
        # if current_point != 0:
        #     edge_array.append([0, current_point, 'B', current_point, 'E'])

    return edge_array


# This method calculates the edges of the MST (Minimum Spanning Tree)
def calculate_mst(sorted_edges, mst_edges, visited_nodes, length):
    # Build an adjacency list to make getting possible edges faster
    adj_list = build_adjacency_list_w_scores(sorted_edges)

    # Create an empty priority queue. Will be used to make accessing element with the lowest score faster.
    priority_queue = []

    # Create two arrays, one contains starting nodes and the other contains ending nodes and scores.
    verts = []
    neighbors = []
    for vert, neighbor in adj_list.items():
        verts.append(vert)
        neighbors.append(neighbor)

    start = 0
    while len(mst_edges) != length - 1:     # This means the MST is complete
        # Iterate through each edge in "start" nodes adjacency list and add to queue
        for edge in neighbors[start]:
            heapq.heappush(priority_queue, (edge[1], verts[start], edge[0]))
        # pop out the minimum score edge and check to make sure no cycles are formed
        min_edge = heapq.heappop(priority_queue)
        while min_edge[2] in visited_nodes:
            min_edge = heapq.heappop(priority_queue)
        # Add min edge to visited nodes and the mst_edges and reset "start"
        visited_nodes.append(min_edge[2])
        mst_edges.append([min_edge[0], min_edge[1], "N", min_edge[2], "N"])
        start = min_edge[2]

    return mst_edges


# Builds an adjacency list of the MST.
# This list includes the similarity scores.
# This is used to make compute_mst faster.
def build_adjacency_list_w_scores(mst_edges):
    adj_list = defaultdict(list)
    for score, start, sl, end, el in mst_edges:
        if start != end:
            adj_list[start].append([end, score])

    return adj_list


# Builds an adjacency list of the MST.
# This will be used to traverse the MST.
def build_adjacency_list(mst_edges):
    adj_list = defaultdict(list)
    for score, start, sl, end, el in mst_edges:
        if start != end:
            adj_list[start].append(end)

    # Uncomment code below if you want to print adjacency list.
    for vert, neigh in adj_list.items():
        print(f"{vert}-> {neigh}")

    return adj_list


# Performs a DFS (Depth First Search) of the MST and returns the 2 approximate optimal ordering of the playlist.
def perform_dfs(adj_list, node, visited, trav_order):
    visited[node] = True
    trav_order.append(node)

    for neighbor in adj_list[node]:
        if not visited[neighbor]:
            perform_dfs(adj_list, neighbor, visited, trav_order)


# Performs a depth first search on the MST to get the optimal ordering for the playlist.
def get_traversal(mst_edges):
    adj_list = build_adjacency_list(mst_edges)

    start_node = 0
    visited = [False] * (len(mst_edges) + 1)

    trav_order = []
    perform_dfs(adj_list, start_node, visited, trav_order)

    return trav_order


# Finds the optimal path through the playlist using an MST (Minimum Spanning Tree)
# This will provide a 2-approximate solution.
def mst_2_approx(audio_features, song_uris):
    # Create 3-feature array of each edge in graph.
    edge_array = get_edge_array(audio_features, song_uris)

    # Compute MST edges
    mst_edges = []
    visited_nodes = [0]
    mst_edges = calculate_mst(edge_array, mst_edges, visited_nodes, len(song_uris))

    # for m in mst_edges:
    #     print(m)

    # Output final optimal ordering.
    trav_order = get_traversal(mst_edges)
    # print("LENGTH: ", len(trav_order))
    return trav_order, mst_edges, edge_array


# ____________________________________________________________________________________________________________________ #

# Finds optimal path through playlist using the nearest neighbor method.
# Print statements have been left in for testing purposes.
def greedy_nearest_neighbor(audio_features, song_uris):
    curr_node = 0
    visited_nodes_set = {curr_node}
    visited_nodes_list = [curr_node]
    for i in range(len(song_uris) - 1):
        # print("NNNNNNNNNNNNNEEEEEEEEEEEEEEEEEEEWWWWWWWWWWWWWWWWWWWWWWWWW")
        # if len(visited_nodes_list) < 5:
        #     print(curr_node)
        curr_min_dist = float('inf')
        curr_min_node = -1
        for j, song_data in enumerate(song_uris):
            if song_data[1] in visited_nodes_set:
                continue

            # if len(visited_nodes_list) < 5:
            #     print("data ", song_data)
            dist = get_sim_score(audio_features[curr_node], audio_features[song_data[1]])
            # if len(visited_nodes_list) < 5:
            #     print("dist ", dist)
            if dist < curr_min_dist:
                curr_min_dist = dist
                curr_min_node = song_data[1]
        # if len(visited_nodes_list) < 5:
        #     print("MMMMMMMMIIIIIIIIIINNNNNNNNNN", curr_min_dist)
        visited_nodes_set.add(curr_min_node)
        visited_nodes_list.append(curr_min_node)
        curr_node = curr_min_node

    return visited_nodes_list


# ____________________________________________________________________________________________________________________ #
# In this method we will iterate through each song in the playlist and get there audio features.
# We do this 100 songs at a time to avoid excess calls to the api.
# We will also be removing columns from the features that we don't want.
def get_audio_features(sp, song_uris):
    song_features = []
    start_idx = 0
    for i in range(0, (len(song_uris) // 100) + 1):
        track_ids = [item[0] for item in song_uris[start_idx:start_idx + 100]]
        if len(track_ids) > 0:
            extracted_f = sp.audio_features(track_ids)
            temp = False
            for e in extracted_f:
                try:
                    if temp:
                        print(sp.track(e['uri'])['name'])
                        temp = False
                    f = [e['acousticness'], e['danceability'], e['energy'], e['instrumentalness'], e['liveness'], e['loudness'],
                         e['speechiness'], e['valence']]
                    song_features.append(f)
                except:
                    print("SONG ERROR!")
                    temp = True
            start_idx += 100
    return song_features


# ____________________________________________________________________________________________________________________ #
# This method leads to all visualization creation, if this method is not called then data_prep.py and create_visual.py
# will never be used.
def visual_hub(opt_order, mst_order, song_uris, audio_features, mst_edges, all_edges, h_score):
    # audio_features = dp.data_prep_main(song_uris, audio_features)
    cv.create_visuals_main(audio_features, opt_order, mst_order, mst_edges, all_edges, h_score)


# This will act as the main method to be called by spotify_access.py
def transitions_main(sp, song_uris):
    print("Getting Audio Features")
    audio_features = get_audio_features(sp, song_uris)
    audio_features = dp.data_prep_main(song_uris, audio_features)

    print("Getting Greedy Solution")
    naive_order = greedy_nearest_neighbor(audio_features, song_uris)

    print("Getting MST Solution")
    # mst_order, mst_edges, all_edges = mst_2_approx(audio_features, song_uris)
    mst_order = [0, 1]
    mst_edges = [0,1]
    all_edges = [0,1]

    print("Getting Heuristic")
    h_order, h_score = hs.heuristics_approach(audio_features)

    print("Visualizing")
    visual_hub(naive_order, mst_order, song_uris, audio_features, mst_edges, all_edges, h_score)  # Comment if you don't want to see visuals

    return h_order


# This is the main method which can be used for testing
def main():
    pass


if __name__ == "__main__":
    main()
