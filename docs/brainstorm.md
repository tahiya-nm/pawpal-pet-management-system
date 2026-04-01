# PawPal+ — Object Design Brainstorm

## Core Objects

### `Task`
Represents a single care activity.

**Attributes:**
- `title: str` — e.g. "Morning walk", "Medication"
- `duration_minutes: int` — how long it takes
- `priority: str` — "high", "medium", or "low"

**Methods:**
- `priority_value() -> int` — converts priority to a number (high=3, medium=2, low=1) for sorting
- `__repr__()` — readable string for debugging/display

---

### `Pet`
Represents the animal being cared for. Owns the task list.

**Attributes:**
- `name: str` — e.g. "Mochi"
- `species: str` — "dog", "cat", "other"
- `tasks: list[Task]` — all care tasks associated with this pet

**Methods:**
- `add_task(task: Task)` — add a task to the list
- `remove_task(title: str)` — remove a task by title
- `get_tasks() -> list[Task]` — return all tasks

---

### `Owner`
Represents the person doing the care. Holds the daily time budget.

**Attributes:**
- `name: str` — e.g. "Jordan"
- `available_minutes: int` — total time available per day for pet care

**Methods:**
- (minimal — primarily a data holder; scheduling logic does not belong here)

---

### `Scheduler`
The brain of the system. Takes an owner + pet and produces a daily plan.

**Attributes:**
- `owner: Owner`
- `pet: Pet`

**Methods:**
- `generate_plan() -> Plan` — sorts tasks by priority, fits as many as possible into the available time budget, and records why each task was included or skipped

---

### `Plan`
The output of the scheduler. Separates scheduled vs. skipped tasks and holds reasoning.

**Attributes:**
- `scheduled: list[tuple[Task, str]]` — (task, reason it was included)
- `skipped: list[tuple[Task, str]]` — (task, reason it was skipped)
- `total_time_used: int` — minutes consumed

**Methods:**
- `summary() -> str` — plain-language explanation of the full plan for display in Streamlit

---

## Relationships

- `Owner` has a time budget
- `Pet` has many `Task`s
- `Scheduler` takes `Owner` + `Pet`, produces `Plan`
- `Plan` contains references to `Task`s with reasoning strings

```
Owner ──── time budget ────► Scheduler ──► Plan
Pet ────── tasks ──────────►              ↕
                                        Task (+ reasons)
```

---

## Planned File Structure

| File | Contents |
|---|---|
| `models.py` | `Task`, `Pet`, `Owner` |
| `scheduler.py` | `Scheduler`, `Plan` |
| `tests/test_scheduler.py` | unit tests for scheduling behavior |
| `app.py` | Streamlit UI — imports and calls the above |
