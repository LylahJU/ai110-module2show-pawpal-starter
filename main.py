from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, HealthStatus, Priority, Frequency, Scheduler

# Create an Owner
owner = Owner("Alice")

# Create at least two Pets
pet1 = Pet("Buddy", 3, "Golden Retriever", HealthStatus.HEALTHY)
pet2 = Pet("Whiskers", 2, "Siamese Cat", HealthStatus.HEALTHY)

# Add pets to the owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Get today's date
today = date.today()

# Create at least three Tasks with different due dates
task1 = Task("task1", "Feed Buddy", today + timedelta(days=1), pet1, "Feeding", Frequency.DAILY, Priority.HIGH)
task2 = Task("task2", "Groom Whiskers", today + timedelta(days=2), pet2, "Grooming", Frequency.WEEKLY, Priority.MEDIUM)
task3 = Task("task3", "Vet appointment for Buddy", today, pet1, "Health Check", Frequency.MONTHLY, Priority.HIGH)
# Add two tasks at the same date and time to validate lightweight conflict detection
task4 = Task("task4", "Brush Buddy", today + timedelta(days=1), pet1, "Grooming", Frequency.ONCE, Priority.MEDIUM, time="10:00")
task5 = Task("task5", "Play with Whiskers", today + timedelta(days=1), pet2, "Playtime", Frequency.ONCE, Priority.LOW, time="10:00")

# Add tasks out of order to verify ordering logic
owner.add_task(task3)
owner.add_task(task1)
owner.add_task(task2)
owner.add_task(task4)
owner.add_task(task5)

# Complete one task to show pending filtering
owner.complete_task("task2")

# Scheduler for filtered and sorted views
scheduler = Scheduler(owner)

conflict_warnings = scheduler.get_conflict_warnings()
if conflict_warnings:
    print("\nConflict Warnings:")
    for warning in conflict_warnings:
        print(f"- {warning}")

print("Today's Schedule:")
todays_tasks = owner.get_todays_tasks(today)
for task in todays_tasks:
    print(
        f"- {task.title} for {task.pet.name} (Due: {task.due_date}, Priority: {task.priority.value}, Frequency: {task.frequency.value})"
    )

print("\nAll Tasks (sorted by due date):")
for task in sorted(scheduler.get_all_tasks(), key=lambda t: t.due_date):
    status = "completed" if task.completed else "pending"
    print(
        f"- {task.due_date}: {task.title} for {task.pet.name} [{task.priority.value}, {task.frequency.value}, {status}]"
    )

print("\nPending Tasks:")
for task in scheduler.get_pending_tasks():
    print(f"- {task.title} for {task.pet.name} (Due: {task.due_date})")

print("\nHigh Priority Tasks:")
for task in scheduler.get_tasks_by_priority(Priority.HIGH):
    print(f"- {task.title} for {task.pet.name} (Due: {task.due_date})")

print("\nWeekly Tasks:")
for task in scheduler.get_tasks_by_frequency(Frequency.WEEKLY):
    print(f"- {task.title} for {task.pet.name} (Due: {task.due_date})")
