"""
Script to generate index automatically from the titles of the markdown files.
"""

from __future__ import annotations

import os
import re
import subprocess
import time
from dataclasses import dataclass

# Index header that has been seen by a thread.
seen_headers = set()


class TitleNotFound(Exception):
    """Markdown file missing a title that starts with a '#' sign."""

    pass


@dataclass(slots=True)  # type: ignore
class Index:
    """Dataclass to represent an index element.
    Every index must live under a header. For example:

    ## Header

    * Index 1
    * Index 2
    * ...
    """

    header: str
    header_formatted: str
    body: str
    body_formatted: str


def discover_markdowns(root_dir: str) -> set[str]:
    """Recursively discover markdown files by traversing
    down from the root directory."""

    filepaths = set()

    for root, _, files in os.walk(root_dir, onerror=OSError):
        for file in files:
            if not file.endswith(".md"):
                continue
            rel_dir = os.path.relpath(root, root_dir)
            rel_file = os.path.join(root_dir, rel_dir, file)
            filepaths.add(rel_file)

    return filepaths


def get_index(src_filepath: str) -> Index:
    """Create index from a single file."""

    with open(src_filepath, "r") as f:
        for line in f.readlines():
            if not re.match("^# ", line):
                raise TitleNotFound(
                    f"no title found in file '{src_filepath}'; make sure there is no blank line before the title",
                )

            markdown_title = line.replace("\n", "").replace("#", "").strip()
            body = f"* [{markdown_title}]({src_filepath})"

            matched = re.search(r"./til/\W*(\w+)", src_filepath)
            if matched:
                header = matched.group(1)
            else:
                raise TitleNotFound(
                    f"no title found for file '{src_filepath}'; make sure the markdown file lives under the 'til' folder",
                )

            header_formatted = f"\n## {header.title()}\n"
            body_formatted = f"{body}\n\n"

            index = Index(
                header=header,
                header_formatted=header_formatted,
                body=body,
                body_formatted=body_formatted,
            )
            return index


def save_index_header(index: Index, dest_filepath: str = "./README.md") -> None:
    """Save a single index header to the 'dest_file'."""

    with open(dest_filepath, "a+") as f:
        if index.header not in seen_headers:
            f.write(index.header_formatted)
            seen_headers.add(index.header)


def sort_index_header(dest_filepath: str) -> None:
    subprocess.run(f"awk '$1' {dest_filepath} | sort -o {dest_filepath}", shell=True)


def save_index_body(index: Index, dest_filepath: str) -> None:
    """Save a single index body to the 'dest_file'."""

    with open(dest_filepath, "r+") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if index.header_formatted.strip() in line:
                lines.insert(idx + 1, index.body_formatted)

        f.truncate(0)  # truncates the file
        f.seek(0)  # moves the pointer to the start of the file
        f.writelines(lines)  # write the new data to the file


def clear_destination(dest_filepath: str) -> None:
    """Clear the 'README.md' file before start writing to it."""
    subprocess.run(f" > {dest_filepath}", shell=True)


def main(root_dir: str, dest_filepath: str = "./README.md") -> None:
    """Orchestrate all the routines."""

    # Clear the destination file.
    clear_destination(dest_filepath=dest_filepath)

    # Discover the relative paths of all the markdown files in the rootpath.
    src_filepaths = discover_markdowns(root_dir=root_dir)

    # Extract indexes from the files found in the 'src_filepaths'.
    indexes = [get_index(src_filepath) for src_filepath in src_filepaths]
    indexes = [index for index in indexes if index]

    # Only save the headers of the indexes.
    for index in indexes:
        save_index_header(index, dest_filepath=dest_filepath)

    # Sort the index headers.
    sort_index_header(dest_filepath=dest_filepath)

    # Save the index elements under the appropriate headers.
    # This function is quite slow now and threading doesn't work with it as of now.
    for index in indexes:
        save_index_body(index, dest_filepath=dest_filepath)


if __name__ == "__main__":

    start = time.monotonic()

    main(root_dir="./til")

    end = time.monotonic()

    print(f"execution time: {((end-start))} sec")
