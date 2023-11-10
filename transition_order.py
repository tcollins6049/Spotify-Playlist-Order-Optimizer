

# ____________________________________________________________________________________________________________________ #
def get_audio_features(sp, song_uris):
    song_features = []
    for i in range(0, (len(song_uris) // 100) + 1):
        track_ids = [item[0] for item in song_uris[i:i + 100]]
        extracted_f = sp.audio_features(track_ids)
        for e in extracted_f:
            song_features.append(e)

    return song_features


# ____________________________________________________________________________________________________________________ #
# This will act as the main method to be called by spotify_access.py
def transitions_main(sp, song_uris):
    audio_features = get_audio_features(sp, song_uris)

    # This is returning a temporary testing list
    return [1, 2, 3, 4, 5, 6, 7, 8, 0]

# This is the main method which can be used for testing
def main():
    pass


if __name__ == "__main__":
    main()
