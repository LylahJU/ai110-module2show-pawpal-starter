from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
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


@dataclass
class Pet:
    name: str
    age: int
    breed: str
    health: HealthStatus
    owner: Optional[User] = None

    def __post_init__(self):
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
    priority: Priority = Priority.MEDIUM
    completed: bool = False

    def __post_init__(self):
        if self.due_date < date.today():
            raise ValueError("Due date cannot be in the past")
        if not isinstance(self.priority, Priority):
            raise ValueError("Priority must be a Priority enum")

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update(self, *, title: Optional[str] = None, due_date: Optional[date] = None, task_type: Optional[str] = None, priority: Optional[Priority] = None) -> None:
        """Update task details."""
        if title is not None:
            self.title = title
        if due_date is not None:
            if due_date < date.today():
                raise ValueError("Due date cannot be in the past")
            self.due_date = due_date
        if task_type is not None:
            self.task_type = task_type
        if priority is not None:
            if not isinstance(priority, Priority):
                raise ValueError("Priority must be a Priority enum")
            self.priority = priority


class Walk:
    def __init__(self, id: str, pet: Pet, walk_date: date, walk_time: time, length_minutes: int) -> None:
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


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: List[Pet] = []
        self.tasks: Dict[str, Task] = {}
        self.walks: Dict[str, Walk] = {}

    def edit_name(self, new_name: str) -> None:
        """Update the user's name."""
        self.name = new_name

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the user."""
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
        """Assign an existing pet to this user."""
        if pet in self.pets:
            raise ValueError("Pet already assigned")
        self.pets.append(pet)
        pet.owner = self

    def add_task(self, task: Task) -> None:
        """Add a new pet care task."""
        if task.pet not in self.pets:
            raise ValueError("Task's pet is not owned by this user")
        if task.id in self.tasks:
            raise ValueError("Task ID already exists")
        self.tasks[task.id] = task

    def get_todays_tasks(self, today: date) -> List[Task]:
        """Return tasks due today."""
        return [task for task in self.tasks.values() if task.due_date == today]

    def schedule_walk(self, walk: Walk) -> None:
        """Add a scheduled walk for a pet."""
        if walk.pet not in self.pets:
            raise ValueError("Walk's pet is not owned by this user")
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
        """Mark a task complete by ID."""
        if task_id not in self.tasks:
            return False
        self.tasks[task_id].complete()
        return True

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def remove_walk(self, walk_id: str) -> bool:
        """Remove a walk by ID."""
        if walk_id in self.walks:
            del self.walks[walk_id]
            return True
        return False
