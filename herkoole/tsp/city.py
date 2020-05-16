import dataclasses


@dataclasses.dataclass(repr=True)
class City:
    identifier: str
    x: float
    y: float
