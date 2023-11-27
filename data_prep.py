

# This method will be used to normalize any features whose values don't fall between 0 and 1.
def normalize_features(audio_features):
    for af in audio_features:
        af[5] = (af[5] - -60) / (0 - -60)   # Loudness -- {-60, 0}

    return audio_features


# This method is used to get the x-axis coordinate data for each song.
def get_x(audio_features):
    # x = [af[0] for af in audio_features]  # Picks first feature as x-coord

    # Sets x-coordinate values as the average of the first half of the features
    x = []
    for af in audio_features:
        dr = (af[0] + af[1] + af[2] + af[3]) / 4
        x.append(dr)
    return x


# This method is used to get the y-axis coordinate data for each song.
def get_y(audio_features):
    # y = [af[1] for af in audio_features]    # Picks second feature as y-coord

    # Sets y-coordinate values as the average of the second half of the features
    y = []
    for af in audio_features:
        dr = (af[4] + af[5] + af[6] + af[7]) / 4
        y.append(dr)
    return y


# This method is used to get the z-axis coordinate data for each song.
# This method also contains a try except block as we might not need any z-coord data in the case that we are
#     making a 2-D plot.
def get_z(audio_features):
    try:
        z = [af[2] for af in audio_features]    # Picks third feature as z-coord
        return z
    except:
        return None


def data_prep_main(song_uris, audio_features):
    audio_features = normalize_features(audio_features)
    x = get_x(audio_features)
    y = get_y(audio_features)
    z = get_z(audio_features)
    return x, y, z, audio_features
