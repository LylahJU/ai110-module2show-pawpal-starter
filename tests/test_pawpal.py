import pytest
from datetime import date, time, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, HealthStatus, Priority, Frequency


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


def test_scheduler_sorts_tasks_by_time():
    owner = Owner("Alice")
    pet = Pet("Buddy", 3, "Golden Retriever", HealthStatus.HEALTHY)
    owner.add_pet(pet)

    task_early = Task("task1", "Morning meds", date.today(), pet, "Medication", Frequency.ONCE, Priority.MEDIUM, time="08:00")
    task_middle = Task("task2", "Lunch break", date.today(), pet, "Feeding", Frequency.ONCE, Priority.MEDIUM, time="12:00")
    task_late = Task("task3", "Evening stretch", date.today(), pet, "Exercise", Frequency.ONCE, Priority.MEDIUM, time="18:00")
    task_no_time = Task("task4", "Journal", date.today(), pet, "Care", Frequency.ONCE, Priority.LOW)

    owner.add_task(task_middle)
    owner.add_task(task_late)
    owner.add_task(task_no_time)
    owner.add_task(task_early)

    scheduler = Scheduler(owner)
    ordered = scheduler.get_tasks_sorted_by_time()

    assert ordered[0].id == "task1"
    assert ordered[1].id == "task2"
    assert ordered[2].id == "task3"
    assert ordered[-1].id == "task4"


def test_conflict_warnings_detect_duplicate_time():
    owner = Owner("Alice")
    pet1 = Pet("Buddy", 3, "Golden Retriever", HealthStatus.HEALTHY)
    pet2 = Pet("Milo", 2, "Beagle", HealthStatus.HEALTHY)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task("task1", "Feed Buddy", date.today(), pet1, "Feeding", Frequency.ONCE, Priority.HIGH, time="09:00")
    task2 = Task("task2", "Feed Milo", date.today(), pet2, "Feeding", Frequency.ONCE, Priority.HIGH, time="09:00")
    task3 = Task("task3", "Walk Buddy", date.today(), pet1, "Walking", Frequency.ONCE, Priority.MEDIUM, time="10:00")

    owner.add_task(task1)
    owner.add_task(task2)
    owner.add_task(task3)

    scheduler = Scheduler(owner)
    warnings = scheduler.get_conflict_warnings()

    assert len(warnings) == 1
    assert "09:00" in warnings[0]
    assert "Feed Buddy" in warnings[0]
    assert "Feed Milo" in warnings[0]
