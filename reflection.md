# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

PawPal+ is designed around three core user actions that drive the entire system:

1. **Add a pet** — The user enters basic owner and pet information (owner name, pet name, species, and how many minutes per day are available for care). This data seeds the scheduler with the time budget it works within.

2. **Add and manage care tasks** — The user creates individual tasks such as walks, feeding, medications, grooming, or enrichment activities. Each task has a title, a duration in minutes, and a priority level (e.g., high / medium / low). Tasks can be added, edited, or removed at any time.

3. **Generate and view today's plan** — The user triggers schedule generation. The system selects and orders tasks based on priority and available time, then displays the resulting daily plan alongside a plain-language explanation of why each task was included or excluded (e.g., "Medication was scheduled first because it is high priority" or "Extended walk was skipped — not enough time remaining").

These three actions map to four natural classes: `Owner` (holds owner info and daily time budget), `Pet` (holds pet info and its task list), `Task` (title, duration, priority), and `Scheduler` (takes an owner + pet and returns an ordered plan with reasoning).

- What classes did you include, and what responsibilities did you assign to each?
    - `Owner`: Stores owner name and daily time budget.
    - `Pet`: Stores pet name, species, and list of care tasks.
    - `Task`: Represents a care task with title, duration, and priority.
    - `Scheduler`: Contains the logic to generate a daily care plan based on the owner's time budget and the pet's tasks, while providing explanations for scheduling decisions.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
