from pydantic import BaseModel

__all__ = [
    "BalancedCurve",
    "DisabledCurve",
    "PerformanceCurve",
    "SilentCurve",
]


class BaseFanCurve(BaseModel):
    points: list[tuple[float, float]]
    """List of tuples of temperature and PWM points"""

    def __init__(self, points: list[tuple[float, float]]) -> None:
        super().__init__(points=points)

    def get_pwm(self, temp: float) -> float:
        for i, (t, p) in enumerate(self.points):
            if temp <= t:
                if i == 0:
                    return p
                t0, p0 = self.points[i - 1]
                return p0 + (p - p0) * (temp - t0) / (t - t0)
        return self.points[-1][1]


SilentCurve = BaseFanCurve(
    [
        (0, 0),
        (40, 30),
        (60, 50),
        (70, 70),
        (80, 100),
    ],
)
BalancedCurve = BaseFanCurve(
    [
        (0, 25),
        (40, 30),
        (60, 70),
        (70, 90),
        (80, 100),
    ],
)
PerformanceCurve = BaseFanCurve(
    [
        (0, 30),
        (40, 40),
        (60, 100),
    ],
)

# DANGEROUS, obviously.
DisabledCurve = BaseFanCurve(
    [
        (0, 0),
    ],
)
