from dataclasses import dataclass

from model.Constructor import Constructor


@dataclass

class Edge:
    c1:Constructor
    c2:Constructor
    weight: int