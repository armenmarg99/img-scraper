from dataclasses import dataclass, astuple


@dataclass
class BfsNode:
    url: str
    output_folder: str
    depth: int

    def __iter__(self):
        yield from astuple(self)
