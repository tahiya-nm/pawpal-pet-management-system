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
    owner.add_pet(pet)  # Owner.add_pet() stores the Pet in owner.pets
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

    if st.button("Add Task"):
        priority_map = {"high": Priority.HIGH, "medium": Priority.MEDIUM, "low": Priority.LOW}
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority_map[priority_str],
        )
        # Find the chosen pet and call Pet.add_task()
        for pet in owner.pets:
            if pet.name == selected_pet_name:
                pet.add_task(task)  # Pet.add_task() appends to pet._tasks
                st.success(f"Added '{task_title}' to {selected_pet_name}.")
                break

    # Show current tasks per pet
    for pet in owner.pets:
        tasks = pet.get_tasks()
        if tasks:
            st.write(f"**{pet.name}'s tasks:**")
            st.table([
                {"title": t.title, "duration (mins)": t.duration_minutes, "priority": t.priority.name}
                for t in tasks
            ])

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    plan = Scheduler(owner).generate_plan()  # Scheduler.generate_plan() returns a Plan
    st.text(plan.summary())                  # Plan.summary() formats the result
