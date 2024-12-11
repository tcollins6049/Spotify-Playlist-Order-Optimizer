# Spotify Playlist Order Optimizer
## Overview
A Python-based tool designed to reorder songs within a Spotify playlist to achieve the shortest average distance between songs. Distance between songs are determined by the euclidean distance between two songs vectors with vectors being computed using a songs audio features. This creates a travelling salesman probem (TSP)

## Features
- Extracts audio features from songs using the Spotify API to create feature vectors.
- Computes Euclidean distances between songs based on feature vectors.
- Implements three optimization algorithms to solve TSP:
  1. Naive Nearest Neighbor: A greedy approach for reordering.
  2. Minimum Spanning Tree (MST): Constructs optomized ordering using a tree structure.
  3. Heuristics: Custom algorithm for order optimization.
- Saves reordered playlist to user's Spotify account.

## Algorithms
### 1. Naive Nearest Neighbor
A greedy algorithm that starts at a random song and iteratively adds the nearest unvisited song to the order.

**Advantages**: Simple and fast solution

**Disadvantages**: May result in suboptimal solutions.
