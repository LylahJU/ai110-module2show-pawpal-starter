# PawPal+ Project Reflection

## 1. System Design
Three core actions:
 - add a pet
 - schedule a walk
 - see today's tasks

 The main objects needed for the system:
 - pet attributes: name, age, breed, health
 - pet methods: add a pet, delete a pet, edit a pet
 - walk attributes: date, time, length
 - walk methods: schedule a walk, edit a walk
 - tasks attributes: title, due date, pet, type of task
 - tasks methods: add a task, edit a task, complete a task, view today's tasks

 - user attributes: name, pets
 - user methods: create user, edit user, assign pet to user

**a. Initial design**

The initial design was centered around four main classes: `Pet`, `Task`, `Walk`, and `User`.

- `Pet`: represented a pet's profile with attributes like `name`, `age`, `breed`, and `health`. Its responsibility was to store pet-specific data and provide methods to update the pet profile and check walk eligibility.
- `Task`: represented a pet care task with `title`, `due_date`, `pet`, `task_type`, `priority`, and `completed` status. It was responsible for tracking task details, marking completion, and allowing updates to task information.
- `Walk`: represented a scheduled walk with `pet`, `walk_date`, `walk_time`, and `length_minutes`. Its responsibility was to encapsulate walk scheduling details and support rescheduling or updating duration.
- `User`: acted as the system owner and aggregate manager. It held collections of pets, tasks, and walks, and provided methods for adding pets, scheduling walks, creating tasks, viewing today's tasks, editing task details, and completing tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- Relationships: Pets now link back to owners; tasks/walks validate pet ownership.
- Performance: Dicts eliminate linear searches for large datasets.
- Robustness: Input validation prevents invalid states (e.g., past dates, negative ages).
- Identification: Unique IDs make operations reliable and prevent conflicts.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- The scheduler currently checks for exact date/time matches when warning about conflicts, rather than testing whether tasks overlap in duration. This makes the logic simpler and efficient for a basic pet-care planner, while accepting that it may miss some duration-based conflicts.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
