# PawPal+ Project Reflection

## 1. System Design

### a. Initial design

The app design was centered around four main classes: `Pet`, `Task`, `Walk`, and `Owner`.

- `Pet`: stores pet profile data and validates walk eligibility based on health and age.
- `Task`: stores care tasks with fields for title, due date, assigned pet, task type, priority, recurrence, and optional scheduled time.
- `Walk`: manages walk scheduling details and allows rescheduling and duration updates.
- `Owner`: aggregates pets, tasks, and walks while enforcing ownership validation and task lifecycle operations.

### b. Design changes

Yes, the design evolved during implementation. The most meaningful change was adding a dedicated `Scheduler` class to separate planning concerns from data management.

- `Scheduler` now handles sorted task lists, pending task filters, and conflict warnings.
- `Owner` kept core data operations, while the scheduler became responsible for planning behavior.
- This separation made the system cleaner and easier to extend without mixing UI and scheduling logic.

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

The scheduler considers:

- time ordering for scheduled tasks
- pending status so only incomplete tasks are shown
- exact same date/time conflicts to warn the owner
- task priority and recurrence through the task model, with daily and weekly recurrence handled after completion

I focused on time ordering and conflict detection first because they directly impact the user's ability to trust the daily plan.

### b. Tradeoffs

One tradeoff is that conflict detection only checks exact date/time overlaps, not task duration overlaps.

That tradeoff is reasonable for this early pet-care planner because it keeps the scheduler simple and easy to understand while still catching the most obvious scheduling mistakes.

## 3. AI Collaboration

### a. How I used AI

I used AI as a design and implementation assistant. Copilot helped me draft method names, suggested class responsibilities, and offered small refactorings while I built `pawpal_system.py` and `app.py`.

The most helpful prompts were focused on behavior: "How should a scheduler detect conflicts?" and "What is the cleanest way to sort tasks by time and keep untimed tasks last?"

### b. Judgment and verification

I did not accept every AI suggestion as-is. For example, an early suggestion proposed combining task sorting and conflict detection in one method. I rejected that because it blurred responsibilities and made testing harder.

I verified AI suggestions by checking the underlying logic in `pawpal_system.py`, then confirming the class methods remained isolated and easy to reason about.

### c. Separate chat sessions

Using separate chat sessions for design, implementation, and documentation helped me stay organized. Each phase had a clear goal, so I could keep the architecture clean while making the final app and docs consistent.

### d. Lead architect takeaway

I learned that being the lead architect means guiding the overall design, choosing when to accept AI help, and making sure AI-generated suggestions fit the system's structure rather than dictating it.

## 4. Testing and Verification

### a. What I tested

I tested core behaviors such as:

- tasks sorted by time with untimed tasks last
- duplicate-time conflict warnings for same-day tasks
- recurring task generation after completing daily or weekly tasks

These behaviors are important because they ensure the scheduler produces a reliable daily plan and alerts the owner to obvious issues.

### b. Confidence

I am reasonably confident the scheduler works for the implemented behaviors. The main edge cases I would test next are overlapping tasks with durations, multiple-day recurrence, and pet-specific preference rules.

## 5. Reflection

### a. What went well

The clean division between data management and scheduling logic worked well. It made the app easier to connect to Streamlit and allowed the scheduler to be tested independently.

### b. What I would improve

If I had another iteration, I would expand conflict detection beyond exact same-time matches to capture duration overlaps, and I would add a richer UI for editing task times directly from the schedule.

### c. Key takeaway

The most important lesson is that AI works best when it supports the architect's decisions rather than replacing them. Clear design boundaries and a strong acceptance/rejection process keep the system maintainable.
