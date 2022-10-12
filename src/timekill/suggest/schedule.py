from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Schedule:
    """How often a certain activity should be completed or recommended."""

    # TODO: Would a cron-style format be better?

    activity: str
    frequency: int
    unit: str
    last: datetime | None = None

    def should(self) -> bool:
        """Check if the activity should be completed/recommended."""
        if self.last is None:
            return True

        if self.unit == "day":
            return self.last + timedelta(days=self.frequency) < datetime.now()
        if self.unit == "week":
            return self.last + timedelta(weeks=self.frequency) < datetime.now()
        if self.unit == "month":
            return self.last + timedelta(weeks=self.frequency * 4) < datetime.now()

        raise ValueError(f"Unknown unit {self.unit}")

    def done(self) -> None:
        """Mark the activity as completed/recommended."""
        self.last = datetime.now()
