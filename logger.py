log_items = []

def record(descr, entity=None):
    log_items.append({'descr': descr, 'entity': entity})

def get_last_actions(count=10):
    return [itm['descr'] for itm in log_items[-10:]]