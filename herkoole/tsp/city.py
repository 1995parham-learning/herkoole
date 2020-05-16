import dataclasses


@dataclasses.dataclass(repr=True)
class City:
    identifier: int
    x: float
    y: float
