import ast

from utils import config

allowlist_cache = set()


def load():
    global allowlist_cache
    try:
        with open(config.allowlist_path, 'r') as f:
            allowlist_file = f.read()
            if not allowlist_file == str(set()):
                allowlist_cache = ast.literal_eval(allowlist_file)
            else:
                allowlist_cache = set()
    except (FileNotFoundError, SyntaxError):
        allowlist_cache = set()


def commit():
    global allowlist_cache
    with open(config.allowlist_path, 'w') as file:
        file.write(str(allowlist_cache))


def add(user_id: int):
    global allowlist_cache
    allowlist_cache.add(user_id)


def remove(user_id: int):
    global allowlist_cache
    allowlist_cache.remove(user_id)


def clear():
    global allowlist_cache
    allowlist_cache.clear()
