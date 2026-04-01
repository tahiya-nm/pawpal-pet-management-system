from dataclasses import dataclass, field
from enum import Enum


class Priority(Enum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority  # Priority.HIGH, Priority.MEDIUM, or Priority.LOW

    def priority_value(self) -> int:
        """Return the numeric value of this task's priority for sorting."""
        pass

    def __repr__(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", or "other"
    _tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove the first task matching the given title from this pet's task list."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks associated with this pet."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int  # total time available per day across all pets
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        pass


@dataclass
class Plan:
    owner: Owner
    scheduled: list[tuple[Pet, Task, str]] = field(default_factory=list)  # (pet, task, reason included)
    skipped: list[tuple[Pet, Task, str]] = field(default_factory=list)    # (pet, task, reason skipped)
    total_time_used: int = 0

    def summary(self) -> str:
        """Return a plain-language explanation of the full plan for display,
        including the owner name and how the shared time budget was used."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> Plan:
        """Collect all tasks across all of the owner's pets, sort by priority,
        fit as many as possible into the shared available_minutes budget,
        and record why each task was included or skipped."""
        pass
