from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DiscogsResult:
    release_id: int
    title: str
    artist: str
    year: Optional[int]
    label: Optional[str]
    catno: Optional[str]
    formats: List[str]
    track_count: Optional[int]
    styles: List[str]
    country: Optional[str]
