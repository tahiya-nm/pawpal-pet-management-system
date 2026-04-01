---
name: PawPal system class structure
description: Attribute names, constructor signatures, enum values, and design conventions for pawpal_system.py
type: project
---

Key structural facts about `pawpal_system.py`:

- `Priority` enum: HIGH=3, MEDIUM=2, LOW=1 (integer values used for sort ordering)
- `Task` fields: `title: str`, `duration_minutes: int` (NOT `duration`), `priority: Priority`
- `Pet` fields: `name: str`, `species: str`, `_tasks: list[Task]` (private, via `default_factory=list`)
- `Owner` fields: `name: str`, `available_minutes: int`, `pets: list[Pet]` (public)
- `Plan` fields: `owner: Owner`, `scheduled: list[tuple[Pet, Task, str]]`, `skipped: list[tuple[Pet, Task, str]]`, `total_time_used: int = 0`
- `Scheduler.__init__` takes a single `owner: Owner`; `generate_plan()` returns a `Plan`

Scheduler algorithm:
1. Flatten all pet tasks into `(task, pet)` tuples via `pet.get_tasks()`
2. Sort by `-priority_value()` then `duration_minutes` ascending (greedy, highest priority + shortest first)
3. Greedy fill up to `owner.available_minutes`; remainder goes to `skipped`

**Why:** These exact attribute names matter — the dataclass field `_tasks` on Pet is private but is the backing store; `get_tasks()` / `add_task()` / `remove_task()` are the public interface.

**How to apply:** Always use `duration_minutes` (not `duration`) when referencing task length. Access pet tasks through `get_tasks()`, never `_tasks` directly in Scheduler.
