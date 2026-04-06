# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit-based pet care planning assistant. It helps pet owners manage tasks, schedule routines, and surface possible conflicts so care stays consistent and predictable.

## Overview

This app models three core domains:

- Pet ownership and pet profiles
- Pet care tasks with priority, due date, and optional scheduled time
- A scheduling engine that sorts tasks, filters pending work, and warns of same-time conflicts

The user interface is built in `app.py`, while the domain logic is implemented in `pawpal_system.py`.

## Features

- Sorting by time: tasks are ordered by scheduled time, with untimed tasks listed last
- Conflict warnings: same-date/time tasks are detected and clearly presented to the owner
- Pending task filtering: only incomplete tasks are shown in the generated schedule
- Daily and weekly recurrence: completing recurring tasks creates the next occurrence automatically
- Task validation: invalid dates, times, and priorities are rejected with clear feedback
- Pet ownership validation: tasks and walks must belong to a pet owned by the active owner
- Walk eligibility rules: only healthy pets may be scheduled for walks

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

## Usage

1. Enter the owner name and pet details.
2. Add tasks with titles, priorities, due dates, and optional times.
3. Click **Generate schedule** to view sorted pending tasks.
4. Review any conflict warnings and adjust task times before finalizing care.

## Architecture

The app uses the following classes in `pawpal_system.py`:

- `Owner`: manages pets, tasks, and walks
- `Pet`: stores pet profile information and walk eligibility logic
- `Task`: stores scheduled work, priority, frequency, and completion status
- `Scheduler`: provides sorted schedules, filtered task lists, and conflict detection

## Testing

Run the tests with:

```bash
python -m pytest
```

The repository includes coverage for:

- task completion and recurring daily/weekly task generation
- scheduler sorting of tasks by time, with untimed tasks last
- duplicate-time conflict detection for same-day tasks

Confidence Level: ⭐⭐⭐⭐⭐
