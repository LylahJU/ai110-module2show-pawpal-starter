from pawpal_system import Owner, Pet, Task, HealthStatus, Priority, Frequency
from datetime import date

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

# Create at least three Tasks with different due dates (interpreting "different times" as different dates)
task1 = Task("task1", "Feed Buddy", today, pet1, "Feeding", Frequency.DAILY, Priority.HIGH)
task2 = Task("task2", "Groom Whiskers", today, pet2, "Grooming", Frequency.WEEKLY, Priority.MEDIUM)
task3 = Task("task3", "Vet appointment for Buddy", today.replace(day=today.day + 1), pet1, "Health Check", Frequency.MONTHLY, Priority.HIGH)

# Add tasks to the owner
owner.add_task(task1)
owner.add_task(task2)
owner.add_task(task3)

# Print "Today's Schedule"
todays_tasks = owner.get_todays_tasks(today)
print("Today's Schedule:")
for task in todays_tasks:
    print(f"- {task.title} for {task.pet.name} (Priority: {task.priority.value}, Frequency: {task.frequency.value})")
