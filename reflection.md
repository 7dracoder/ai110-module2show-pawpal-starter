# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My first design used four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` stores the pet list, `Pet` stores tasks, `Task` stores the details of one care activity, and `Scheduler` handles sorting, filtering, conflicts, and completion.

**b. Design changes**

I added recurrence fields to `Task` after starting the scheduler logic. At first a task was only a title and time, but daily and weekly tasks needed a due date and frequency so the system could create the next task after completion.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers date, time, priority, pet name, and completion status. I treated time and priority as the most important because a pet owner mainly needs to know what should happen first and what matters most.

**b. Tradeoffs**

The conflict checker only looks for exact date and time matches. It does not calculate overlapping durations. That is reasonable for this version because it keeps the logic easy to understand and still catches the most obvious scheduling problem.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI for planning the class structure, writing the first version of the scheduler, and checking the tests. The most helpful prompts were specific ones like asking how the scheduler should collect tasks from the owner and how to test recurrence.

**b. Judgment and verification**

I did not keep the sorting exactly as first written because sorting only by clock time made tomorrow's recurring task appear before later tasks from today. I changed it to sort by date and then time, then verified it with the CLI output and tests.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding tasks, sorting by time, daily recurrence, and conflict detection. These tests matter because they cover the main things the app promises to do.

**b. Confidence**

I am about 4 out of 5 confident. The core behavior works, but I would add more tests for duplicate pet names, invalid task times, and larger schedules.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the simple connection between the backend classes and Streamlit. The app is not fancy, but adding pets and tasks actually uses the same logic as the demo and tests.

**b. What you would improve**

I would improve conflict detection so it can notice overlapping durations, not just exact time matches. I would also add saving to a JSON file so the app remembers data after closing.

**c. Key takeaway**

My main takeaway is that AI is useful for moving faster, but I still need to act like the architect. The design only stayed clean when I checked each suggestion against what the project actually needed.
