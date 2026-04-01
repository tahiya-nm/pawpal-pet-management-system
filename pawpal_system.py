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
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def priority_value(self) -> int:
        """Return the numeric value of this task's priority for sorting."""
        return self.priority.value

    def __repr__(self) -> str:
        """Return a readable string representation of the task."""
        return f"Task('{self.title}', {self.duration_minutes} mins, {self.priority})"


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", or "other"
    _tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self._tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove the first task matching the given title from this pet's task list."""
        for i, task in enumerate(self._tasks):
            if task.title == title:
                del self._tasks[i]
                return

    def get_tasks(self) -> list[Task]:
        """Return all tasks associated with this pet."""
        return self._tasks


@dataclass
class Owner:
    name: str
    available_minutes: int  # total time available per day across all pets
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)


@dataclass
class Plan:
    owner: Owner
    scheduled: list[tuple[Pet, Task, str]] = field(default_factory=list)  # (pet, task, reason included)
    skipped: list[tuple[Pet, Task, str]] = field(default_factory=list)    # (pet, task, reason skipped)
    total_time_used: int = 0

    def summary(self) -> str:
        """Return a formatted summary of scheduled and skipped tasks with time budget usage."""
        lines = []
        lines.append(f"Plan for {self.owner.name} "
                     f"({self.total_time_used}/{self.owner.available_minutes} mins used)")
        lines.append("")

        lines.append("Scheduled Tasks:")
        if self.scheduled:
            for pet, task, _ in self.scheduled:
                lines.append(f"- {pet.name}: {task.title} ({task.duration_minutes} mins)")
        else:
            lines.append("- None")

        lines.append("")

        lines.append("Skipped Tasks:")
        if self.skipped:
            for pet, task, reason in self.skipped:
                lines.append(
                    f"- {task.title} ({task.duration_minutes} mins) — {reason}"
                )
        else:
            lines.append("- None")

        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with the owner whose pets will be scheduled."""
        self.owner = owner

    def generate_plan(self) -> Plan:
        """Sort all pet tasks by priority and greedily schedule them within the owner's time budget."""
        # 1. Flatten: build list of (task, pet) tuples across all pets
        all_tasks: list[tuple[Task, Pet]] = []
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                all_tasks.append((task, pet))

        # 2. Sort: highest priority first; shortest duration as tie-breaker
        all_tasks.sort(key=lambda tp: (-tp[0].priority_value(), tp[0].duration_minutes))

        # 3. Iterate and schedule
        scheduled: list[tuple[Pet, Task, str]] = []
        skipped: list[tuple[Pet, Task, str]] = []
        remaining_minutes = self.owner.available_minutes

        for task, pet in all_tasks:
            if task.duration_minutes <= remaining_minutes:
                scheduled.append((pet, task, "High priority and fits in remaining time."))
                remaining_minutes -= task.duration_minutes
            else:
                skipped.append((
                    pet, task,
                    f"Insufficient remaining time (needs {task.duration_minutes} mins, "
                    f"only {remaining_minutes} left)."
                ))

        # 4. Return a Plan
        return Plan(
            owner=self.owner,
            scheduled=scheduled,
            skipped=skipped,
            total_time_used=self.owner.available_minutes - remaining_minutes,
        )


if __name__ == '__main__':
    # Owner with 60 available minutes
    owner = Owner(name="Alex", available_minutes=60)

    # Two pets
    rex = Pet(name="Rex", species="dog")
    luna = Pet(name="Luna", species="cat")

    # Tasks for Rex (dog)
    rex.add_task(Task(title="Morning Walk", duration_minutes=20, priority=Priority.HIGH))
    rex.add_task(Task(title="Fetch Training", duration_minutes=15, priority=Priority.MEDIUM))
    rex.add_task(Task(title="Bath Time", duration_minutes=25, priority=Priority.LOW))

    # Tasks for Luna (cat)
    luna.add_task(Task(title="Vet Checkup", duration_minutes=30, priority=Priority.HIGH))
    luna.add_task(Task(title="Grooming", duration_minutes=10, priority=Priority.MEDIUM))
    luna.add_task(Task(title="Playtime", duration_minutes=15, priority=Priority.LOW))

    # Total task time: 20+15+25+30+10+15 = 115 mins, exceeds 60

    # Add pets to owner
    owner.add_pet(rex)
    owner.add_pet(luna)

    # Generate and print the plan
    plan = Scheduler(owner).generate_plan()
    print(plan.summary())
