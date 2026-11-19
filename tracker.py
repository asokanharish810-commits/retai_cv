# tracker.py
# Re-identification based on last known position

import math

# Stores last known center position per stable ID
last_positions = {}  # stable_id → (cx, cy)
id_map = {}          # raw_id → stable_id
next_id = [1]

# Max pixel distance to consider same person
DISTANCE_THRESHOLD = 100


def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def get_stable_id(raw_id, cx, cy):
    # If we've seen this raw_id before, reuse its stable_id
    if raw_id in id_map:
        stable_id = id_map[raw_id]
        last_positions[stable_id] = (cx, cy)
        return stable_id

    # New raw_id — check if it matches a lost person by position
    best_match = None
    best_dist = float("inf")

    for stable_id, (lx, ly) in last_positions.items():
        dist = euclidean((cx, cy), (lx, ly))
        if dist < DISTANCE_THRESHOLD and dist < best_dist:
            best_dist = dist
            best_match = stable_id

    if best_match is not None:
        # Re-identify as existing person
        id_map[raw_id] = best_match
        last_positions[best_match] = (cx, cy)
        print(f"🔁 Re-identified raw={raw_id} → Customer {best_match} (dist={best_dist:.1f}px)")
        return best_match

    # Truly new person
    stable_id = next_id[0]
    next_id[0] += 1
    id_map[raw_id] = stable_id
    last_positions[stable_id] = (cx, cy)
    print(f"🆕 New Customer {stable_id} (raw={raw_id})")
    return stable_id