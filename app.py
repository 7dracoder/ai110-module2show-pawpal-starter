from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.title("🐾 PawPal+")
st.caption("Simple pet care scheduling")

owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Pets")
with st.form("pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet and pet_name.strip():
    if owner.find_pet(pet_name) is None:
        owner.add_pet(Pet(pet_name.strip(), species))
        st.success(f"Added {pet_name.strip()}.")
    else:
        st.warning("That pet is already listed.")

if owner.pets:
    st.table([{"name": pet.name, "species": pet.species, "tasks": pet.task_count()} for pet in owner.pets])
else:
    st.info("Add a pet to get started.")

st.subheader("Tasks")
pet_options = [pet.name for pet in owner.pets]

with st.form("task_form", clear_on_submit=True):
    selected_pet = st.selectbox("Pet", pet_options, disabled=not pet_options)
    title = st.text_input("Task")
    time = st.time_input("Time")
    duration = st.number_input("Duration minutes", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["high", "medium", "low"])
    frequency = st.selectbox("Repeats", ["once", "daily", "weekly"])
    add_task = st.form_submit_button("Add task", disabled=not pet_options)

if add_task and title.strip():
    pet = owner.find_pet(selected_pet)
    if pet:
        pet.add_task(
            Task(
                title.strip(),
                time.strftime("%H:%M"),
                int(duration),
                priority,
                frequency,
                date.today(),
            )
        )
        st.success("Task added.")

st.subheader("Schedule")
all_rows = scheduler.daily_plan()
if all_rows:
    st.table(all_rows)

    conflicts = scheduler.detect_conflicts()
    for warning in conflicts:
        st.warning(warning)

    open_tasks = scheduler.filter_tasks(completed=False)
    st.caption(f"{len(open_tasks)} open task(s)")
else:
    st.info("No tasks yet.")

st.subheader("Mark Complete")
open_task_labels = [
    f"{pet.name} - {task.title}" for pet, task in scheduler.sort_by_time() if not task.completed
]

if open_task_labels:
    selected = st.selectbox("Open task", open_task_labels)
    if st.button("Mark complete"):
        pet_name, task_title = selected.split(" - ", 1)
        scheduler.mark_task_complete(pet_name, task_title)
        st.success("Marked complete.")
        st.rerun()
else:
    st.caption("No open tasks to complete.")
