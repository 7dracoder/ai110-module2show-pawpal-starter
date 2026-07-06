from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")

    mochi.add_task(Task("Morning walk", "08:00", 30, "high", "daily", date.today()))
    mochi.add_task(Task("Brush coat", "18:30", 15, "low", "weekly", date.today()))
    luna.add_task(Task("Breakfast", "07:30", 10, "high", "daily", date.today()))
    luna.add_task(Task("Medication", "08:00", 5, "high", "once", date.today()))

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner


def print_schedule(scheduler: Scheduler) -> None:
    print("Care Schedule")
    print("-------------")
    for pet, task in scheduler.sort_by_time():
        status = "done" if task.completed else "open"
        print(
            f"{task.due_date.isoformat()} {task.time} | {pet.name} | {task.title} "
            f"({task.duration_minutes} min, {task.priority}, {status})"
        )

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print()
        print("Conflict Warnings")
        print("-----------------")
        for warning in conflicts:
            print(f"- {warning}")


if __name__ == "__main__":
    demo_owner = build_demo_owner()
    demo_scheduler = Scheduler(demo_owner)
    demo_scheduler.mark_task_complete("Mochi", "Morning walk")
    print_schedule(demo_scheduler)
