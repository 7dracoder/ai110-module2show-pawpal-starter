from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status():
    task = Task("Feed breakfast", "08:00", 10)

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")

    pet.add_task(Task("Walk", "09:00", 25))

    assert pet.task_count() == 1


def test_scheduler_sorts_tasks_by_time():
    owner = Owner("Jordan")
    pet = Pet("Luna", "cat")
    pet.add_task(Task("Dinner", "18:00", 10))
    pet.add_task(Task("Breakfast", "07:30", 10))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_titles = [task.title for _, task in scheduler.sort_by_time()]

    assert sorted_titles == ["Breakfast", "Dinner"]


def test_daily_recurrence_creates_tomorrow_task():
    today = date.today()
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    pet.add_task(Task("Morning walk", "08:00", 30, frequency="daily", due_date=today))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Mochi", "Morning walk")

    assert pet.tasks[0].completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == today + timedelta(days=1)
    assert pet.tasks[1].completed is False


def test_conflict_detection_flags_duplicate_times():
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    mochi.add_task(Task("Walk", "08:00", 30))
    luna.add_task(Task("Medication", "08:00", 5))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    assert len(scheduler.detect_conflicts()) == 1
