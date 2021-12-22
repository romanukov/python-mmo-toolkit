

events_queue = {}


def emit_event(player_id, name, payload):
    if player_id not in events_queue:
        events_queue[player_id] = {}
    if name not in events_queue[player_id]:
        events_queue[player_id][name] = []
    events_queue[player_id][name].append(payload)
