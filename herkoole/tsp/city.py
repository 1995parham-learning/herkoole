import dataclasses


@dataclasses.dataclass(repr=True)
class City:
    identifier: int
    x: float
    y: float

    def __str__(self) -> str:
        return f"{self.identifier}: ({self.x}, {self.y})"
