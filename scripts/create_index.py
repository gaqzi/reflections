"""
Script to generate index automatically from the titles of the markdown files.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

# Index header that has been seen by a thread.
seen_headers = set()


class TitleNotFound(Exception):
    """Markdown file missing a title that starts with a '#' sign."""

    pass


@runtime_checkable
class ProtoIndex(Protocol):
    """Interface that represents an index entry."""

    index_header: str = "example header"
    markdown_title: str = "# some markdown title"
    markdown_path: str = "./notes/header/path/to/markdown/file.md"

    @property
    def header_formatted(self):
        ...

    @property
    def entry_formatted(self):
        ...


@dataclass(slots=True)  # type: ignore
class Index:
    """Dataclass to represent an index element.
    Every index must live under a header. For example:

    ## Header

    * Index 1
    * Index 2
    * ...
    """

    index_header: str = "example header"
    markdown_title: str = "# some markdown title"
    markdown_path: str = "./notes/header/path/to/markdown/file.md"

    @property
    def header_formatted(self):
        return f"## {self.index_header.title()}\n"

    @property
    def entry_formatted(self):
        markdown_title = self.markdown_title.replace("#", "").strip()
        index_entry = f"* [{markdown_title}]({self.markdown_path})\n"
        return index_entry


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

            matched = re.search(r"./notes/\W*(\w+)", src_filepath)
            if matched:
                index_header = matched.group(1)
            else:
                raise TitleNotFound(
                    f"no title found for file '{src_filepath}'; make sure the markdown file lives under the 'notes' folder",
                )

            index = Index(
                index_header=index_header,
                markdown_title=line,
                markdown_path=src_filepath,
            )
            return index


def save_index_header(index: Index, dest_filepath: str = "./README.md") -> None:
    """Save a single index header to the 'dest_file'."""

    with open(dest_filepath, "a+") as f:
        if index.index_header not in seen_headers:
            f.write(index.header_formatted)
            seen_headers.add(index.index_header)


def sort_index_header(dest_filepath: str) -> None:
    with open(dest_filepath, "r+") as f:
        sorted_contents = "\n".join(sorted(f.readlines()))

        f.seek(0)  # moves the pointer to the start of the file
        f.truncate(0)  # truncates the file
        f.writelines(sorted_contents)  # write the new data to the file


def save_index_entry(index: Index, dest_filepath: str) -> None:
    """Save a single index body to the 'dest_file'."""

    with open(dest_filepath, "r+") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if index.header_formatted in line:
                lines.insert(idx + 1, index.entry_formatted)

        f.seek(0)  # moves the pointer to the start of the file
        f.truncate(0)  # truncates the file
        f.writelines(lines)  # write the new data to the file


def clear_destination(dest_filepath: str) -> None:
    """Clear the 'README.md' file before start writing to it."""
    with open(dest_filepath, "r+") as f:
        f.truncate()


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
        save_index_entry(index, dest_filepath=dest_filepath)


if __name__ == "__main__":

    start = time.monotonic()

    main(root_dir="./notes")

    end = time.monotonic()

    print(f"execution time: {((end-start))} sec")
