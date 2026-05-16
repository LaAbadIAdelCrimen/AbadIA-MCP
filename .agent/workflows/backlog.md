---
description: my backlog
---

# Backlog Execution Workflow: {{task_description}}

This document outlines the standard operating procedure for handling tasks from the backlog based on the provided description: **{{task_description}}**. 

**Prerequisite Action**: The agent MUST generate a `task_name` in `snake_case` format, using no more than 5 words that accurately define the description. This `task_name` will be used for filenames and technical identifiers (e.g., `detach_collar_logic`).

## Workflow Steps

### 1. Task Definition & Context

* **Trigger**: A new task is defined based on the description: **{{task_description}}**.
* **Action**: Review **all** documents in `/docs` to gather full context before planning. In special the files BACKLOG.md and SPECS.md. Check if the task is defined or/and completed yet. 


### 2. Planning & Atomization

* **Create Plan**: Formulate a high-level plan to resolve the task.
* **Breakdown**: Decompose the plan into **atomic subtasks**.
* **Test Definition**: For **each** subtask, define the specific tests needed to verify its correctness.
* **Definition of Done (DoD)**: Establish clear criteria for when the task is considered complete.

### 3. Plan Documentation

Create a specific plan document in `/docs/plans/` for the task.
* **Filename**: `<generated_task_name>.md`
* Include the Definition of Done (DoD) in the plan document after the title.
* **Format**:

```markdown
# [Generated Task Name in Human Readable]

## Plan Overview

| Subtask Title | Intent | Resolution Plan | Current Status        | Est. Hours | Code/Test Difficulty |
| :------------ | :----- | :-------------- | :-------------------- | :--------- | :------------------- |
| *Subtask 1*   | *Why?* | *How?*          | *Implemented/Pending* | *X h*      | *Low/Med/High*       |
| *Subtask 2*   | ...    | ...             | ...                   | ...        | ...                  |

**Total Estimated Hours:** [Total]

```

### 4. Backlog Update (Initial)

* Update `docs/BACKLOG.md` with the task and its atomic subtasks. Append it to the end of the file. 

### 5. Execution Loop (Per Subtask)

For each subtask in the plan:

#### 5.1. **Log Start**: Append an entry to the **end** of `geminilog.md` (root directory).
* **Format**: Table with `Date/Time`, `Intent`, `Resolution Description`.


```markdown
| Date/Time        | Intent                | Resolution Description |
| :--------------- | :-------------------- | :--------------------- |
| YYYY-MM-DD HH:MM | <generated_task_name> | Started subtask...     |

```


#### 5.2. ** Tests for the subtask **: Check if the tests exist in the `tests` directory and cover the subtask and if not create it or expand the current tests if necessary.

#### 5.3. **Implementation**: Write the code to resolve the subtask.

#### 5.4. **Testing**: Run the tests defined in step 2 (Unit/E2E) to verify the fix/feature. If not are OK try again the 5.3 to fix it.

#### 5.5. **Backlog Update**: Mark the subtask as completed in `docs/BACKLOG.md`.

#### 5.6. **Git Operation**:

* `git commit -m "feat(<generated_task_name>): <subtask_description>"`
* `git pull` (if needed) and `git push`


### 6. Final Review

* Verify against the **Definition of Done (DoD)**.
* Close the main task in `docs/BACKLOG.md`.
* Update the plan file `<generated_task_name>.md` in `/docs/plan` with the task of the DoD completed.