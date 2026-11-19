# Customer journey storage
journey = {}

# ZONES will be set by main.py after resolution is detected
ZONES = {}


def get_zone(x, y):
    for name, (x1, y1, x2, y2) in ZONES.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return name
    return "UNKNOWN"


def update_journey(track_id, zone):
    if track_id not in journey:
        journey[track_id] = []

    if len(journey[track_id]) == 0 or journey[track_id][-1] != zone:
        journey[track_id].append(zone)