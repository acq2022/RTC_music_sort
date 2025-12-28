from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DiscogsResult:
    release_id: int
    album_title: str
    album_artist: str
    year: Optional[int]
    label: Optional[str]
    catno: Optional[str]
    tracklist = List[str]
    track_count: Optional[int]
    styles: List[str]
