import streamlit as st
from pawpal_system import Pet, Owner, Task, Walk, Scheduler, HealthStatus, Priority, Frequency
from datetime import date
import uuid

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Initialize Owner in session_state if not present
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Default Owner")

owner = st.session_state.owner

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value=owner.name)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, value=2)
health = st.selectbox("Health status", ["healthy", "sick", "injured"], index=0)

if st.button("Update Owner Name"):
    owner.edit_name(owner_name)

if st.button("Add Pet"):
    health_enum = HealthStatus(health.upper())
    pet = Pet(name=pet_name, age=age, breed=species, health=health_enum)
    owner.add_pet(pet)
    st.success(f"Added pet {pet_name}!")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if not owner.pets:
    st.warning("Add a pet first before adding tasks.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        selected_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
    with col5:
        task_time = st.text_input("Time (HH:MM)", value="", placeholder="e.g., 09:30")

    if st.button("Add task"):
        selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
        task_id = str(uuid.uuid4())
        priority_enum = Priority(priority.upper())
        task = Task(
            id=task_id,
            title=task_title,
            due_date=date.today(),
            pet=selected_pet,
            task_type="care",
            frequency=Frequency.ONCE,
            priority=priority_enum,
            time=task_time if task_time else None
        )
        owner.add_task(task)
        st.success(f"Added task {task_title}!")

    # Display current tasks
    if owner.tasks:
        st.write("Current tasks:")
        task_data = [
            {
                "Title": task.title,
                "Pet": task.pet.name,
                "Due Date": task.due_date,
                "Time": task.time or "N/A",
                "Priority": task.priority.value,
                "Completed": task.completed
            }
            for task in owner.tasks.values()
        ]
        st.table(task_data)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    pending_tasks = scheduler.get_pending_tasks()
    # Sort by time
    sorted_tasks = scheduler.get_tasks_sorted_by_time()
    # Filter to only pending tasks
    sorted_pending_tasks = [task for task in sorted_tasks if not task.completed]
    if sorted_pending_tasks:
        st.write("Pending Tasks Schedule (sorted by time):")
        schedule_data = [
            {
                "Title": task.title,
                "Pet": task.pet.name,
                "Due Date": task.due_date,
                "Time": task.time or "N/A",
                "Priority": task.priority.value
            }
            for task in sorted_pending_tasks
        ]
        st.table(schedule_data)
    else:
        st.info("No pending tasks to schedule.")
