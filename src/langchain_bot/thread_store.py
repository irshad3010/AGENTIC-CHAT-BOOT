
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

THREADS_FILE = PROJECT_ROOT / "threads.json"


def load_threads(user_email):

    if not THREADS_FILE.exists():
        return []

    try:
        with open(THREADS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get(user_email, [])

    except (json.JSONDecodeError, OSError):
        return []


def save_threads(user_email, threads):

    data = {}

    if THREADS_FILE.exists():

        try:
            with open(
                THREADS_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

        except (json.JSONDecodeError, OSError):
            data = {}

    data[user_email] = threads

    with open(
        THREADS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def add_thread(user_email, conversation_id):

    threads = load_threads(user_email)

    # Avoid duplicate conversation IDs
    if any(
        thread["id"] == conversation_id
        for thread in threads
    ):
        return threads

    threads.append({
        "id": conversation_id,
        "label": f"Chat {conversation_id[:8]}"
    })

    save_threads(user_email, threads)

    return threads


__all__ = [
    "load_threads",
    "save_threads",
    "add_thread"
]
