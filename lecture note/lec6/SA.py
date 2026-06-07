"""
Simulated Annealing for the Traveling Salesman Problem (TSP)

Algorithm outline:
  - Start from an initial tour (0, 1, ..., n-1)
  - Repeatedly swap two random cities to generate a neighbor
  - Accept the neighbor if it improves the tour distance, or with
    probability exp(-delta / T) if it does not (Metropolis criterion)
  - Cool the temperature by factor 0.99 each outer iteration
  - Stop when temperature drops below the threshold
"""

import math
import random

import numpy as np


# ── Parameters ────────────────────────────────────────────────────────────────

NUM_CITIES = 30
INITIAL_TEMP = 120.0
MIN_TEMP = 0.001
COOLING_RATE = 0.99
MAX_NO_IMPROVE = 150   # restart cooling when this many consecutive rejects occur
MAX_ITER_PER_TEMP = 500


# ── Data loading ──────────────────────────────────────────────────────────────

def load_locations(filepath: str) -> np.ndarray:
    """Load city (x, y) coordinates from a whitespace-delimited text file."""
    return np.loadtxt(filepath)


# ── Distance utilities ────────────────────────────────────────────────────────

def build_distance_matrix(locations: np.ndarray) -> np.ndarray:
    """Return the symmetric Euclidean distance matrix for the given locations."""
    diff = locations[:, np.newaxis, :] - locations[np.newaxis, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))


def tour_length(dist: np.ndarray, path: list[int]) -> float:
    """Calculate the total round-trip distance for a given tour."""
    n = len(path)
    return sum(dist[path[i], path[(i + 1) % n]] for i in range(n))


# ── Simulated Annealing ───────────────────────────────────────────────────────

def simulated_annealing(
    dist: np.ndarray,
    *,
    initial_temp: float = INITIAL_TEMP,
    min_temp: float = MIN_TEMP,
    cooling_rate: float = COOLING_RATE,
    max_no_improve: int = MAX_NO_IMPROVE,
    max_iter_per_temp: int = MAX_ITER_PER_TEMP,
) -> tuple[list[int], float]:
    """
    Run simulated annealing on the TSP instance described by `dist`.

    Returns
    -------
    best_path : list[int]
        City indices in visit order.
    best_dist : float
        Total round-trip distance of the best tour found.
    """
    n = dist.shape[0]
    path = list(range(n))
    current_dist = tour_length(dist, path)

    best_path = path[:]
    best_dist = current_dist

    temp = initial_temp

    while temp > min_temp:
        no_improve_count = 0
        iter_count = 0

        while no_improve_count < max_no_improve and iter_count < max_iter_per_temp:
            # Pick two distinct cities at random and swap them
            i, j = random.sample(range(n), 2)
            new_path = path[:]
            new_path[i], new_path[j] = new_path[j], new_path[i]

            new_dist = tour_length(dist, new_path)
            delta = new_dist - current_dist

            if delta < 0 or math.exp(-delta / temp) > random.random():
                path = new_path
                current_dist = new_dist
                if current_dist < best_dist:
                    best_dist = current_dist
                    best_path = path[:]
            else:
                no_improve_count += 1

            iter_count += 1

        temp *= cooling_rate

    return best_path, best_dist


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import pathlib

    data_file = pathlib.Path(__file__).parent / "city_location.txt"
    locations = load_locations(data_file)

    dist_matrix = build_distance_matrix(locations)

    best_path, best_dist = simulated_annealing(dist_matrix)

    print(f"Shortest distance : {best_dist:.4f}")
    print(f"Best tour         : {best_path}")
