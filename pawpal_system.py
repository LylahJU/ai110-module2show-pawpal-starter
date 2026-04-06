from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import List, Optional, Dict
from enum import Enum


class HealthStatus(Enum):
    HEALTHY = "healthy"
    SICK = "sick"
    INJURED = "injured"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Frequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ONCE = "once"


@dataclass
class Pet:
    name: str
    age: int
    breed: str
    health: HealthStatus
    owner: Optional[Owner] = None
    tasks: List[Task] = field(default_factory=list)

    def __post_init__(self):
        """Validate pet attributes after initialization."""
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if not isinstance(self.health, HealthStatus):
            raise ValueError("Health must be a HealthStatus enum")

    def update_profile(self, *, name: Optional[str] = None, age: Optional[int] = None, breed: Optional[str] = None, health: Optional[HealthStatus] = None) -> None:
        """Update the pet's profile attributes."""
        if name is not None:
            self.name = name
        if age is not None:
            if age < 0:
                raise ValueError("Age cannot be negative")
            self.age = age
        if breed is not None:
            self.breed = breed
        if health is not None:
            if not isinstance(health, HealthStatus):
                raise ValueError("Health must be a HealthStatus enum")
            self.health = health

    def can_go_for_walk(self) -> bool:
        """Return whether this pet is eligible for a walk."""
        return self.health == HealthStatus.HEALTHY and self.age > 0


@dataclass
class Task:
    id: str
    title: str
    due_date: date
    pet: Pet
    task_type: str
    frequency: Frequency = Frequency.ONCE
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    time: Optional[str] = None  # Optional time in "HH:MM" format

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if self.due_date < date.today():
            raise ValueError("Due date cannot be in the past")
        if not isinstance(self.priority, Priority):
            raise ValueError("Priority must be a Priority enum")
        if not isinstance(self.frequency, Frequency):
            raise ValueError("Frequency must be a Frequency enum")
        if self.time is not None:
            # Validate "HH:MM" format
            try:
                hours, minutes = map(int, self.time.split(':'))
                if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                    raise ValueError("Invalid time format")
            except (ValueError, IndexError):
                raise ValueError("Time must be in 'HH:MM' format (e.g., '09:30')")

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update(self, *, title: Optional[str] = None, due_date: Optional[date] = None, task_type: Optional[str] = None, frequency: Optional[Frequency] = None, priority: Optional[Priority] = None) -> None:
        """Update task details."""
        if title is not None:
            self.title = title
        if due_date is not None:
            if due_date < date.today():
                raise ValueError("Due date cannot be in the past")
            self.due_date = due_date
        if task_type is not None:
            self.task_type = task_type
        if frequency is not None:
            if not isinstance(frequency, Frequency):
                raise ValueError("Frequency must be a Frequency enum")
            self.frequency = frequency
        if priority is not None:
            if not isinstance(priority, Priority):
                raise ValueError("Priority must be a Priority enum")
            self.priority = priority


class Walk:
    def __init__(self, id: str, pet: Pet, walk_date: date, walk_time: time, length_minutes: int) -> None:
        """Initialize a walk with validation."""
        if length_minutes <= 0:
            raise ValueError("Length must be positive")
        if walk_date < date.today():
            raise ValueError("Walk date cannot be in the past")
        self.id = id
        self.pet = pet
        self.walk_date = walk_date
        self.walk_time = walk_time
        self.length_minutes = length_minutes

    def reschedule(self, new_date: date, new_time: time) -> None:
        """Move the walk to a new date or time."""
        if new_date < date.today():
            raise ValueError("Walk date cannot be in the past")
        self.walk_date = new_date
        self.walk_time = new_time

    def update_length(self, length_minutes: int) -> None:
        """Update the walk duration."""
        if length_minutes <= 0:
            raise ValueError("Length must be positive")
        self.length_minutes = length_minutes


class Owner:
    def __init__(self, name: str) -> None:
        """Initialize an owner with a name."""
        self.name = name
        self.pets: List[Pet] = []
        self.tasks: Dict[str, Task] = {}
        self.walks: Dict[str, Walk] = {}

    def edit_name(self, new_name: str) -> None:
        """Update the owner's name."""
        self.name = new_name

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        if pet in self.pets:
            raise ValueError("Pet already added")
        self.pets.append(pet)
        pet.owner = self

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name."""
        original_count = len(self.pets)
        self.pets = [pet for pet in self.pets if pet.name != pet_name]
        removed = len(self.pets) < original_count
        if removed:
            # Note: pet.owner remains set, but that's okay for this skeleton
            pass
        return removed

    def assign_pet(self, pet: Pet) -> None:
        """Assign an existing pet to this owner."""
        if pet in self.pets:
            raise ValueError("Pet already assigned")
        self.pets.append(pet)
        pet.owner = self

    def add_task(self, task: Task) -> None:
        """Add a new pet care task."""
        if task.pet not in self.pets:
            raise ValueError("Task's pet is not owned by this owner")
        if task.id in self.tasks:
            raise ValueError("Task ID already exists")
        self.tasks[task.id] = task
        task.pet.tasks.append(task)

    def _generate_unique_task_id(self, base_id: str) -> str:
        """Return a unique task ID for a recurring task."""
        candidate = f"{base_id}-next"
        counter = 1
        while candidate in self.tasks:
            counter += 1
            candidate = f"{base_id}-next-{counter}"
        return candidate

    def _schedule_next_task(self, task: Task, days_until_next: int) -> None:
        """Create a new task instance for the next recurring occurrence."""
        next_due_date = date.today() + timedelta(days=days_until_next)
        next_task_id = self._generate_unique_task_id(task.id)
        next_task = Task(
            next_task_id,
            task.title,
            next_due_date,
            task.pet,
            task.task_type,
            task.frequency,
            task.priority,
        )
        self.add_task(next_task)

    def get_todays_tasks(self, today: date) -> List[Task]:
        """Return tasks due today."""
        return [task for task in self.tasks.values() if task.due_date == today]

    def schedule_walk(self, walk: Walk) -> None:
        """Add a scheduled walk for a pet."""
        if walk.pet not in self.pets:
            raise ValueError("Walk's pet is not owned by this owner")
        if not walk.pet.can_go_for_walk():
            raise ValueError("Pet is not eligible for a walk")
        if walk.id in self.walks:
            raise ValueError("Walk ID already exists")
        self.walks[walk.id] = walk

    def edit_task(self, task_id: str, **kwargs) -> bool:
        """Update a task by ID."""
        if task_id not in self.tasks:
            return False
        self.tasks[task_id].update(**kwargs)
        return True

    def complete_task(self, task_id: str) -> bool:
        """Mark a task complete by ID and schedule the next occurrence for recurring tasks."""
        if task_id not in self.tasks:
            return False
        task = self.tasks[task_id]
        task.complete()
        if task.frequency == Frequency.DAILY:
            self._schedule_next_task(task, days_until_next=1)
        elif task.frequency == Frequency.WEEKLY:
            self._schedule_next_task(task, days_until_next=7)
        return True

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.pet.tasks.remove(task)
            del self.tasks[task_id]
            return True
        return False

    def remove_walk(self, walk_id: str) -> bool:
        """Remove a walk by ID."""
        if walk_id in self.walks:
            del self.walks[walk_id]
            return True
        return False


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize a scheduler for an owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the owner's pets."""
        return list(self.owner.tasks.values())

    def get_tasks_by_pet(self) -> Dict[Pet, List[Task]]:
        """Organize tasks by pet for better management."""
        tasks_by_pet = {}
        for pet in self.owner.pets:
            tasks_by_pet[pet] = list(pet.tasks)
        return tasks_by_pet

    def get_pending_tasks(self) -> List[Task]:
        """Retrieve only incomplete tasks across all pets."""
        return [task for task in self.owner.tasks.values() if not task.completed]

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Retrieve tasks by priority."""
        return [task for task in self.owner.tasks.values() if task.priority == priority]

    def get_tasks_by_frequency(self, frequency: Frequency) -> List[Task]:
        """Retrieve tasks by frequency."""
        return [task for task in self.owner.tasks.values() if task.frequency == frequency]

    def get_conflict_warnings(self) -> List[str]:
        """Detect tasks scheduled at the same date and time and return warning messages.

        This method checks exact date/time matches only, not overlapping durations,
        so it can warn about direct conflicts while keeping the scheduling logic simple.
        """
        warnings: List[str] = []
        scheduled_tasks: Dict[tuple[date, str], List[Task]] = {}
        for task in self.owner.tasks.values():
            if task.time is None:
                continue
            key = (task.due_date, task.time)
            scheduled_tasks.setdefault(key, []).append(task)

        for (due_date, time_str), tasks in scheduled_tasks.items():
            if len(tasks) > 1:
                pet_names = sorted({task.pet.name for task in tasks})
                pet_description = "same pet" if len({task.pet.name for task in tasks}) == 1 else "different pets"
                titles = "; ".join(f"{task.title} ({task.pet.name})" for task in tasks)
                warnings.append(
                    f"Warning: {len(tasks)} tasks scheduled at the same time on {due_date} {time_str} "
                    f"for {pet_description}: {titles}"
                )
        return warnings

    def get_tasks_sorted_by_time(self) -> List[Task]:
        """Retrieve all tasks sorted by time (earliest first). Tasks without time sort last."""
        return sorted(
            self.owner.tasks.values(),
            key=lambda task: (
                int(task.time.split(':')[0]) * 60 + int(task.time.split(':')[1]) if task.time else float('inf')
            )
        )

    def get_tasks_filtered(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Retrieve tasks filtered by completion status and/or pet name."""
        tasks = list(self.owner.tasks.values())
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet.name == pet_name]
        return tasks
