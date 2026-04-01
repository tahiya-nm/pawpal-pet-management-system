import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner setup ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes per day", min_value=1, max_value=480, value=60)

if st.button("Set Owner"):
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)
    st.success(f"Owner set: {owner_name} ({available_minutes} mins/day)")

if st.session_state.owner is None:
    st.info("Set an owner above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

st.divider()

# --- Add Pet ---
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    pet = Pet(name=pet_name, species=species)
    owner.add_pet(pet)
    st.success(f"Added {pet_name} the {species}.")

if owner.pets:
    st.write("Pets:", [p.name for p in owner.pets])

st.divider()

# --- Add Task ---
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    selected_pet_name = st.selectbox("Assign to pet", [p.name for p in owner.pets])

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        scheduled_time_str = st.text_input("Scheduled time (HH:MM, optional)", placeholder="e.g. 08:30")
    with col5:
        recurrence_str = st.selectbox("Recurrence", ["none", "daily", "weekly"])

    if st.button("Add Task"):
        priority_map = {"high": Priority.HIGH, "medium": Priority.MEDIUM, "low": Priority.LOW}
        scheduled_time = scheduled_time_str.strip() if scheduled_time_str.strip() else None
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority_map[priority_str],
            scheduled_time=scheduled_time,
            recurrence=recurrence_str if recurrence_str != "none" else None,
        )
        for pet in owner.pets:
            if pet.name == selected_pet_name:
                pet.add_task(task)
                st.success(f"Added '{task_title}' to {selected_pet_name}.")
                break

    # --- Conflict warnings (shown inline with task list) ---
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        with st.container(border=True):
            st.warning(f"**{len(conflicts)} scheduling conflict(s) detected — tasks overlap in time:**")
            for msg in conflicts:
                st.warning(msg)

    # --- Task list sorted by scheduled time ---
    for pet in owner.pets:
        tasks = pet.get_tasks()
        if tasks:
            sorted_tasks = scheduler.sort_by_time(tasks)
            st.write(f"**{pet.name}'s tasks** (sorted by scheduled time):")
            st.table([
                {
                    "Title": t.title,
                    "Time": t.scheduled_time or "—",
                    "Duration (mins)": t.duration_minutes,
                    "Priority": t.priority.name,
                    "Recurrence": t.recurrence or "one-time",
                    "Done": "✓" if t.completed else "",
                }
                for t in sorted_tasks
            ])

st.divider()

# --- Filter Tasks ---
st.subheader("Filter Tasks")

if not owner.pets:
    st.info("No pets yet.")
else:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
    with col_f2:
        filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    filter_pet_arg = None if filter_pet == "All" else filter_pet
    filter_done_arg = {"All": None, "Pending": False, "Completed": True}[filter_status]

    filtered = owner.get_filtered_tasks(completed=filter_done_arg, pet_name=filter_pet_arg)
    if filtered:
        st.table([
            {
                "Pet": pet.name,
                "Task": task.title,
                "Duration (mins)": task.duration_minutes,
                "Priority": task.priority.name,
                "Status": "Done" if task.completed else "Pending",
            }
            for pet, task in filtered
        ])
    else:
        st.info("No tasks match your filter.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    scheduler = Scheduler(owner)

    # Show conflicts prominently before the schedule
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        with st.container(border=True):
            st.warning(f"**Heads up: {len(conflicts)} time conflict(s) found. "
                       "Consider adjusting task times before committing to this schedule.**")
            for msg in conflicts:
                st.warning(msg)

    plan = scheduler.generate_plan()

    # Time budget progress bar
    budget_fraction = plan.total_time_used / owner.available_minutes
    st.markdown(f"**Time budget:** {plan.total_time_used} / {owner.available_minutes} mins used")
    st.progress(budget_fraction)

    # Scheduled tasks
    st.markdown("#### Scheduled Tasks")
    if plan.scheduled:
        for pet, task, _ in plan.scheduled:
            label = f"**{pet.name}**: {task.title} — {task.duration_minutes} mins  |  {task.priority.name} priority"
            if task.scheduled_time:
                label += f"  |  {task.scheduled_time}"
            st.success(label)
    else:
        st.info("No tasks could be scheduled.")

    # Skipped tasks
    st.markdown("#### Skipped Tasks")
    if plan.skipped:
        for pet, task, reason in plan.skipped:
            st.error(f"**{task.title}** ({task.duration_minutes} mins) — {reason}")
    else:
        st.info("All tasks fit within your time budget.")
