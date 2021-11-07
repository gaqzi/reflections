from __future__ import annotations

import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_markdown_files(root_dir: str) -> set[str]:
    file_set = set()

    for root, _, files in os.walk(root_dir, onerror=OSError):
        for file in files:
            if not file.endswith(".md"):
                continue
            rel_dir = os.path.relpath(root, root_dir)
            rel_file = os.path.join(root_dir, rel_dir, file)
            file_set.add(rel_file)

    return file_set


def generate_index(file: str) -> str:
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            if not re.match("^# ", line):
                continue

            line = line.replace("#", "", 1).strip(" ").strip("\n")
            return f"* [{line}]({file})"


def save_indexes(root_dir: str, thread_count: int):
    file_set = get_markdown_files(root_dir=root_dir)
    with ThreadPoolExecutor(
        max_workers=thread_count,
        thread_name_prefix="index_thread",
    ) as executor:

        futures = [
            executor.submit(generate_index, file=file) for file in file_set
        ]

        for fut in as_completed(futures):
            pass


save_indexes(root_dir="./til", thread_count=8)
