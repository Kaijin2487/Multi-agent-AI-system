# Memory stub - we’ll integrate Redis or SQLite later

shared_log = []

def log_entry(entry: dict):
    shared_log.append(entry)

def get_all_logs():
    return shared_log
