from pawpal_system import Owner, Pet, Task, Priority, Scheduler

# Create owner with 90 available minutes
owner = Owner(name="Jordan", available_minutes=90)

# Create pets
buddy = Pet(name="Buddy", species="dog")
whiskers = Pet(name="Whiskers", species="cat")
coco = Pet(name="Coco", species="other")

# Add tasks to Buddy
buddy.add_task(Task(title="Morning Walk", duration_minutes=30, priority=Priority.HIGH))
buddy.add_task(Task(title="Obedience Training", duration_minutes=20, priority=Priority.MEDIUM))
buddy.add_task(Task(title="Bath Time", duration_minutes=25, priority=Priority.LOW))

# Add tasks to Whiskers
whiskers.add_task(Task(title="Vet Checkup", duration_minutes=40, priority=Priority.HIGH))
whiskers.add_task(Task(title="Grooming", duration_minutes=15, priority=Priority.MEDIUM))
whiskers.add_task(Task(title="Playtime", duration_minutes=10, priority=Priority.LOW))

# Add tasks to Coco
coco.add_task(Task(title="Cage Cleaning", duration_minutes=20, priority=Priority.HIGH))
coco.add_task(Task(title="Feeding & Water", duration_minutes=5, priority=Priority.MEDIUM))

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)
owner.add_pet(coco)

# Generate plan
plan = Scheduler(owner).generate_plan()

# Print Today's Schedule
print("=" * 45)
print("         PAWPAL+ — TODAY'S SCHEDULE")
print("=" * 45)
print(f"  Owner : {plan.owner.name}")
print(f"  Budget: {plan.owner.available_minutes} mins available")
print(f"  Used  : {plan.total_time_used} mins scheduled")
print("=" * 45)

print("\n  SCHEDULED TASKS")
print("  " + "-" * 41)
for pet, task, _ in plan.scheduled:
    priority_label = task.priority.name.capitalize()
    print(f"  [{priority_label:6}] {pet.name:10} — {task.title} ({task.duration_minutes} mins)")

if plan.skipped:
    print("\n  SKIPPED TASKS")
    print("  " + "-" * 41)
    for pet, task, reason in plan.skipped:
        print(f"  {pet.name:10} — {task.title} ({task.duration_minutes} mins)")
        print(f"             Reason: {reason}")

print("\n" + "=" * 45)
