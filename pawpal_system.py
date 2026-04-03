from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time
from typing import List, Optional


@dataclass
class Pet:
    name: str
    age: int
    breed: str
    health: str

    def update_profile(self, *, name: Optional[str] = None, age: Optional[int] = None, breed: Optional[str] = None, health: Optional[str] = None) -> None:
        """Update the pet's profile attributes."""
        if name is not None:
            self.name = name
        if age is not None:
            self.age = age
        if breed is not None:
            self.breed = breed
        if health is not None:
            self.health = health

    def can_go_for_walk(self) -> bool:
        """Return whether this pet is eligible for a walk."""
        return True


@dataclass
class Task:
    title: str
    due_date: date
    pet: Pet
    task_type: str
    priority: str = "medium"
    completed: bool = False

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update(self, *, title: Optional[str] = None, due_date: Optional[date] = None, task_type: Optional[str] = None, priority: Optional[str] = None) -> None:
        """Update task details."""
        if title is not None:
            self.title = title
        if due_date is not None:
            self.due_date = due_date
        if task_type is not None:
            self.task_type = task_type
        if priority is not None:
            self.priority = priority


class Walk:
    def __init__(self, pet: Pet, walk_date: date, walk_time: time, length_minutes: int) -> None:
        self.pet = pet
        self.walk_date = walk_date
        self.walk_time = walk_time
        self.length_minutes = length_minutes

    def reschedule(self, new_date: date, new_time: time) -> None:
        """Move the walk to a new date or time."""
        self.walk_date = new_date
        self.walk_time = new_time

    def update_length(self, length_minutes: int) -> None:
        """Update the walk duration."""
        self.length_minutes = length_minutes


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []
        self.walks: List[Walk] = []

    def edit_name(self, new_name: str) -> None:
        """Update the user's name."""
        self.name = new_name

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the user."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name."""
        original_count = len(self.pets)
        self.pets = [pet for pet in self.pets if pet.name != pet_name]
        return len(self.pets) < original_count

    def assign_pet(self, pet: Pet) -> None:
        """Assign an existing pet to this user."""
        if pet not in self.pets:
            self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add a new pet care task."""
        self.tasks.append(task)

    def get_todays_tasks(self, today: date) -> List[Task]:
        """Return tasks due today."""
        return [task for task in self.tasks if task.due_date == today]

    def schedule_walk(self, walk: Walk) -> None:
        """Add a scheduled walk for a pet."""
        self.walks.append(walk)

    def edit_task(self, task_title: str, **kwargs) -> bool:
        """Update a task by title."""
        for task in self.tasks:
            if task.title == task_title:
                task.update(**kwargs)
                return True
        return False

    def complete_task(self, task_title: str) -> bool:
        """Mark a task complete by title."""
        for task in self.tasks:
            if task.title == task_title:
                task.complete()
                return True
        return False
