import pytest
from datetime import date
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
