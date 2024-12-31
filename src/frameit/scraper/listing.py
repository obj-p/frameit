from dataclasses import dataclass
from typing import Optional


@dataclass
class Listing:
    artist: Optional[str]
    title: Optional[str]
    url: Optional[str]
