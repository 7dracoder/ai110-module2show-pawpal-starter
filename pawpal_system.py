from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    time: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Return the next task when this one repeats."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            title=self.title,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            due_date=next_date,
        )

    def as_row(self, pet_name: str) -> dict[str, str | int | bool]:
        """Format a task for tables and simple output."""
        return {
            "pet": pet_name,
            "task": self.title,
            "date": self.due_date.isoformat(),
            "time": self.time,
            "duration": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "done": self.completed,
        }


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return how many tasks this pet has."""
        return len(self.tasks)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def find_pet(self, pet_name: str) -> Pet | None:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task with the pet it belongs to."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks: list[tuple[Pet, Task]] | None = None) -> list[tuple[Pet, Task]]:
        """Sort tasks from earliest date and time to latest."""
        task_list = self.owner.all_tasks() if tasks is None else tasks
        return sorted(task_list, key=lambda item: (item[1].due_date, item[1].time))

    def sort_by_priority(self, tasks: list[tuple[Pet, Task]] | None = None) -> list[tuple[Pet, Task]]:
        """Sort tasks by priority first, then time."""
        task_list = self.owner.all_tasks() if tasks is None else tasks
        return sorted(
            task_list,
            key=lambda item: (PRIORITY_ORDER.get(item[1].priority, 1), item[1].time),
        )

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by pet name or completion status."""
        tasks = self.owner.all_tasks()
        if pet_name:
            tasks = [(pet, task) for pet, task in tasks if pet.name.lower() == pet_name.lower()]
        if completed is not None:
            tasks = [(pet, task) for pet, task in tasks if task.completed == completed]
        return tasks

    def detect_conflicts(self) -> list[str]:
        """Return warnings for tasks that share the same date and time."""
        seen: dict[tuple[date, str], tuple[Pet, Task]] = {}
        warnings: list[str] = []

        for pet, task in self.sort_by_time():
            key = (task.due_date, task.time)
            if key in seen:
                other_pet, other_task = seen[key]
                warnings.append(
                    f"{task.due_date.isoformat()} at {task.time}: "
                    f"{other_pet.name}'s {other_task.title} conflicts with "
                    f"{pet.name}'s {task.title}."
                )
            else:
                seen[key] = (pet, task)

        return warnings

    def mark_task_complete(self, pet_name: str, task_title: str) -> Task | None:
        """Complete a task and add the next one if it repeats."""
        pet = self.owner.find_pet(pet_name)
        if pet is None:
            return None

        for task in pet.tasks:
            if task.title.lower() == task_title.lower() and not task.completed:
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task:
                    pet.add_task(next_task)
                return task

        return None

    def daily_plan(self) -> list[dict[str, str | int | bool]]:
        """Return a readable schedule table."""
        return [task.as_row(pet.name) for pet, task in self.sort_by_priority()]
