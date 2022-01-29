# src.py
from __future__ import annotations

from operator import itemgetter

main_dict = {
    "this": 0,
    "is": 1,
    "an": 2,
    "example": 3,
    "of": 4,
    "speech": 5,
    "synthesis": 6,
    "in": 7,
    "english": 8,
}

sub_keys = ["this", "is", "an", "example"]

sub_dict = dict(zip(sub_keys, itemgetter(*sub_keys)(main_dict)))

print(sub_dict)
