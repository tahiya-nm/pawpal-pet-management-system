from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "high", "medium", or "low"

    def priority_value(self) -> int:
        """Convert priority string to numeric value for sorting (high=3, medium=2, low=1)."""
        pass

    def __repr__(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", or "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove a task from this pet's task list by title."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks associated with this pet."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int  # total time available per day for pet care


@dataclass
class Plan:
    scheduled: list[tuple[Task, str]] = field(default_factory=list)  # (task, reason included)
    skipped: list[tuple[Task, str]] = field(default_factory=list)    # (task, reason skipped)
    total_time_used: int = 0

    def summary(self) -> str:
        """Return a plain-language explanation of the full plan for display."""
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def generate_plan(self) -> Plan:
        """Sort tasks by priority, fit as many as possible into the available time budget,
        and record why each task was included or skipped."""
        pass
