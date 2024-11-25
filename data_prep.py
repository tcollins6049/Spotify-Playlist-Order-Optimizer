

# This method will be used to normalize any features whose values don't fall between 0 and 1.
def normalize_features(audio_features):
    for af in audio_features:
        af[5] = (af[5] - -60) / (0 - -60)   # Loudness -- {-60, 0}

    return audio_features


def data_prep_main(song_uris, audio_features):
    audio_features = normalize_features(audio_features)
    return audio_features
