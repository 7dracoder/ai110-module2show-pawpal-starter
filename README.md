# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

This is the output from running `python main.py`:

```
Care Schedule
-------------
2026-07-05 07:30 | Luna | Breakfast (10 min, high, open)
2026-07-05 08:00 | Mochi | Morning walk (30 min, high, done)
2026-07-05 08:00 | Luna | Medication (5 min, high, open)
2026-07-05 18:30 | Mochi | Brush coat (15 min, low, open)
2026-07-06 08:00 | Mochi | Morning walk (30 min, high, open)

Conflict Warnings
-----------------
- 2026-07-05 at 08:00: Mochi's Morning walk conflicts with Luna's Medication.
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests cover task completion, adding tasks to pets, sorting, recurring daily tasks, and conflict detection.

```
============================= test session starts =============================
platform win32 -- Python 3.11.1, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 5 items

tests\test_pawpal.py .....                                               [100%]

============================== 5 passed in 0.04s ==============================
```

Confidence level: 4/5. The main behaviors work, but I would still add more edge case tests for bad time input and duplicate pet names.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | Sorts by date/time or by priority first. |
| Filtering | `Scheduler.filter_tasks()` | Can filter by pet name or completion status. |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags exact date/time matches as warnings. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Daily tasks move forward 1 day and weekly tasks move forward 7 days. |

## 📸 Demo Walkthrough

1. Enter the owner name at the top of the app.
2. Add one or more pets with a name and species.
3. Add tasks for each pet with a time, duration, priority, and repeat setting.
4. Review the schedule table. It shows the pet, task, date, time, priority, repeat setting, and completion status.
5. If two tasks land on the same date and time, the app shows a warning.
6. Mark an open task complete. If it is daily or weekly, the next task is created automatically.

The Streamlit UI uses the same classes as the command line demo, so the displayed schedule is coming from the real backend logic in `pawpal_system.py`.
