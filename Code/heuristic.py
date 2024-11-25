from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import manhattan_distances
import data_prep as dp
import create_visuals as cv
from collections import defaultdict
import heapq
import random


def get_sequence(start_comb, mid, j_start, j_end):
    seq = []
    j = j_start
    visited = set()

    seq = start_comb[:mid]
    for n in seq:
        visited.add(n)

    while len(seq) < len(start_comb):
        if j_end[j] not in visited:
            seq.append(j_end[j])
            visited.add(j_end[j])
            j += 1
        else:
            j += 1
            while start_comb[j_start] in visited:
                j_start += 1
                if j_start == len(start_comb):
                    break
            if j_start < len(start_comb):
                seq.append(start_comb[j_start])
                visited.add(start_comb[j_start])
                j_start += 1

    return seq


def cross(comb1, comb2):
    mid = len(comb1) // 2

    seq1 = get_sequence(comb1, mid, mid, comb2)
    seq2 = get_sequence(comb2, mid, mid, comb1)

    # Test prints to make sure crossover is working correctly
    # print("Comb1: ", comb1)
    # print("Comb2: ", comb2)
    # print("Seq1: ", seq1)
    # print("Seq2: ", seq2)

    return seq1, seq2


# Finds all crossovers given half of the best songs
def compute_crossovers(combinations, audio_features):
    new_combs = []
    for i in range(0, 5000):
        seq1_idx = random.randint(0, 4999)
        seq2_idx = random.randint(0, 4999)
        while seq1_idx == seq2_idx:
            seq2_idx = random.randint(0, 4999)

        seq1, seq2 = cross(combinations[seq1_idx][0], combinations[seq2_idx][0])
        new_combs.append([seq1, get_avg_sim_score(seq1, audio_features)])
        new_combs.append([seq2, get_avg_sim_score(seq1, audio_features)])

    return new_combs


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


# Get the orders and average distances for 10,000 random combinations
def get_random_combos(audio_features):
    length = len(audio_features)
    combinations = []
    order = list(range(length))
    for i in range(10000):
        random.shuffle(order)
        combinations.append([order.copy(), get_avg_sim_score(order, audio_features)])

    return combinations


# Return order found by heuristic approach
def heuristics_approach(audio_features):
    iterations = 1

    # Get 10,000 random combinations list
    combs = get_random_combos(audio_features)
    combs = sorted(combs, key=lambda x: x[1])
    current_best = combs[0]

    for i in range(0, iterations):
        print("Iteration ", i+1, " of ", iterations)
        # Save the best so far and take the best half for the next iteration
        top_half = combs[:len(combs) // 2]  # This will be the top 5,000 songs.

        cross_combs = compute_crossovers(top_half, audio_features)
        cross_combs = sorted(cross_combs, key=lambda x: x[1])

        if cross_combs[0][1] < current_best[1]:
            current_best = cross_combs[0]
        combs = cross_combs
        print(current_best[1])

    return current_best[0], current_best[1]     # return order, score
