import pytest
from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, HealthStatus, Priority, Frequency


def test_task_completion():
    """Verify that calling complete() actually changes the task's status."""
    # Create a pet
    pet = Pet("Buddy", 3, "Golden Retriever", HealthStatus.HEALTHY)
    
    # Create a task
    task = Task("task1", "Feed Buddy", date.today(), pet, "Feeding", Frequency.DAILY, Priority.HIGH)
    
    # Initially, task should not be completed
    assert not task.completed
    
    # Call complete() method
    task.complete()
    
    # Now task should be completed
    assert task.completed


def test_task_addition_increases_pet_task_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Create an owner
    owner = Owner("Alice")
    
    # Create a pet
    pet = Pet("Buddy", 3, "Golden Retriever", HealthStatus.HEALTHY)
    
    # Add pet to owner
    owner.add_pet(pet)
    
    # Initially, pet should have no tasks
    assert len(pet.tasks) == 0
    
    # Create a task
    task = Task("task1", "Feed Buddy", date.today(), pet, "Feeding", Frequency.DAILY, Priority.HIGH)
    
    # Add task to owner (which also adds it to the pet)
    owner.add_task(task)
    
    # Now pet should have one task
    assert len(pet.tasks) == 1


def test_daily_task_generates_next_occurrence():
    owner = Owner("Alice")
    pet = Pet("Buddy", 3, "Golden Retriever", HealthStatus.HEALTHY)
    owner.add_pet(pet)
    task = Task("task1", "Feed Buddy", date.today(), pet, "Feeding", Frequency.DAILY, Priority.HIGH)
    owner.add_task(task)

    assert owner.complete_task("task1")
    assert task.completed
    assert len(owner.tasks) == 2

    next_task = next(t for t in owner.tasks.values() if t.id != "task1")
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert not next_task.completed


def test_weekly_task_generates_next_occurrence():
    owner = Owner("Alice")
    pet = Pet("Buddy", 3, "Golden Retriever", HealthStatus.HEALTHY)
    owner.add_pet(pet)
    task = Task("task1", "Groom Buddy", date.today(), pet, "Grooming", Frequency.WEEKLY, Priority.MEDIUM)
    owner.add_task(task)

    assert owner.complete_task("task1")
    assert task.completed
    assert len(owner.tasks) == 2

    next_task = next(t for t in owner.tasks.values() if t.id != "task1")
    assert next_task.due_date == date.today() + timedelta(weeks=1)
    assert not next_task.completed
