from sklearn.metrics.pairwise import euclidean_distances


# Computes similarity score between song-i and song-j
def get_sim_score(songi_data, songj_data):
    af_score = euclidean_distances([songi_data], [songj_data])
    return af_score


# Finds optimal path through playlist using the nearest neighbor method.
def naive_nearest_neighbor(audio_features, song_uris):
    curr_node = 0
    visited_nodes_set = {curr_node}
    visited_nodes_list = [curr_node]
    for i in range(len(song_uris) - 1):
        curr_min_dist = float('inf')
        curr_min_node = -1
        for j, song_data in enumerate(song_uris):
            if song_data[1] in visited_nodes_set:
                continue
            dist = get_sim_score(audio_features[curr_node], audio_features[song_data[1]])
            if dist < curr_min_dist:
                curr_min_dist = dist
                curr_min_node = song_data[1]
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
    for i in range(0, (len(song_uris) // 100) + 1):
        track_ids = [item[0] for item in song_uris[i:i + 100]]
        extracted_f = sp.audio_features(track_ids)
        for e in extracted_f:
            # Possible features to be added:
            #   - duration_ms, key, mode, tempo, time_signature
            f = [e['acousticness'], e['danceability'], e['energy'], e['instrumentalness'], e['liveness'], e['loudness'],
                 e['speechiness'], e['valence']]
            song_features.append(f)

    return song_features


# ____________________________________________________________________________________________________________________ #
# This will act as the main method to be called by spotify_access.py
def transitions_main(sp, song_uris):
    audio_features = get_audio_features(sp, song_uris)
    order = naive_nearest_neighbor(audio_features, song_uris)

    # This is returning a temporary testing list
    return order
    #return [1, 2, 3, 4, 5, 6, 7, 8, 0]

# This is the main method which can be used for testing
def main():
    pass


if __name__ == "__main__":
    main()
