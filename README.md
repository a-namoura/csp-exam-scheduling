# CSP Exam Scheduling with Backtracking & AC-3

A Python implementation of **exam timetabling as a Constraint Satisfaction Problem (CSP)**. This project demonstrates how recursive backtracking finds a conflict-free exam schedule and how **AC-3 (Arc Consistency Algorithm #3)** can prune invalid time-slot choices before the search begins.

Developed as coursework for the **Artificial Intelligence Lab at Al-Quds University** (June 4, 2025).

## Overview

An exam schedule must assign each subject a time slot while respecting availability and student-conflict constraints. The project models the problem using:

- **Variables:** exams to schedule.
- **Domains:** permitted time slots for each exam.
- **Constraints:** exams that share students cannot occupy the same time slot.

The program solves the same instance twice:

1. **Backtracking only:** searches for a valid assignment using the original domains.
2. **AC-3 + backtracking:** first eliminates values that are inconsistent with neighboring exams, then searches the reduced domains.

Both runs display their schedules and execution times. The AC-3 run also reports which domain values were removed.

## Problem Instance

The example contains four exams and three symbolic time slots (`T1`, `T2`, and `T3`).

| Exam | Allowed time slots | Conflicts with |
| --- | --- | --- |
| Math | T1, T2 | Physics, Chemistry |
| Physics | T1 | Math, English |
| Chemistry | T2, T3 | Math, English |
| English | T1, T2, T3 | Physics, Chemistry |

For every pair of conflicting exams, the constraint is:

```python
def constraint(slot_a, slot_b):
    return slot_a != slot_b
```

Exams without a conflict may share a time slot.

## Getting Started

### Requirements

- Python 3
- Git (optional, for cloning)

No third-party packages are required; the script uses only Python's standard library (`collections`, `copy`, and `time`).

### Installation and Usage

```bash
git clone https://github.com/a-namoura/csp-exam-scheduling.git
cd csp-exam-scheduling
python3 csp-exam-scheduling.py
```

On Windows, use `python csp-exam-scheduling.py` if `python3` is not available.

The script runs both approaches automatically. No command-line arguments or input files are needed.

## Example Result

Both approaches produce the following conflict-free schedule for the included dataset:

| Exam | Assigned time slot |
| --- | --- |
| Math | T2 |
| Physics | T1 |
| Chemistry | T3 |
| English | T2 |

Math and English can share `T2` because they are not defined as conflicting exams.

Before backtracking, AC-3 removes these inconsistent values:

```text
Removed 'T1' from 'Math' due to inconsistency with 'Physics'
Removed 'T2' from 'Chemistry' due to inconsistency with 'Math'
Removed 'T1' from 'English' due to inconsistency with 'Physics'
Removed 'T3' from 'English' due to inconsistency with 'Chemistry'
```

The resulting domains each contain one valid time slot. The program prints timings for backtracking without preprocessing, AC-3 preprocessing, and backtracking after AC-3. **Actual timing values depend on the machine and run.** Because this is a small example, the measurements are illustrative rather than a general performance benchmark.

## How It Works

### Backtracking Search

The recursive solver assigns exams in the order listed in `variables`:

1. Select the first unassigned exam.
2. Try each time slot in that exam's domain.
3. Check the proposed slot against already-assigned conflicting exams.
4. Continue recursively if consistent; otherwise try another value.
5. Backtrack when no value works.

A complete assignment is returned when all exams are scheduled; otherwise the solver returns `None`.

### AC-3 Domain Pruning

AC-3 processes directed arcs between conflicting exams. For each arc `(Xi, Xj)`, it removes a value from `Xi` when no value in `Xj` supports the constraint. When a domain changes, neighboring arcs are revisited.

If a domain becomes empty, AC-3 detects inconsistency and the program skips backtracking. Otherwise, backtracking runs over the reduced domains.

**Important:** Arc consistency alone does not guarantee that a solution exists for every CSP. Backtracking is still needed in the general case.

## Customizing the Schedule

Edit the problem definition at the top of [`csp-exam-scheduling.py`](csp-exam-scheduling.py):

- `variables` — subjects to schedule.
- `full_domains` — permitted time slots for each subject.
- `neighbors` — pairs of subjects that cannot be scheduled simultaneously.

Keep conflict relationships symmetric (if A lists B as a neighbor, B should list A as well), and ensure every subject has a domain and a neighbors entry. The script currently uses a fixed, in-code dataset; it does not read external timetables or accept CLI configuration.

## Repository Contents

| File | Description |
| --- | --- |
| [`csp-exam-scheduling.py`](csp-exam-scheduling.py) | CSP model, AC-3 implementation, backtracking search, and comparison output. |
| [`CSP Exam Scheduling with Backtracking and AC-3.pdf`](CSP%20Exam%20Scheduling%20with%20Backtracking%20and%20AC-3.pdf) | Accompanying project PDF. |
| `README.md` | Project documentation and usage instructions. |

## Educational Scope

This is a small, self-contained demonstration of **constraint modeling**, **systematic search**, and **constraint propagation**. It is intended for learning and experimentation rather than production-scale exam scheduling. The implementation uses the first-unassigned-variable ordering and does not include advanced search heuristics or a user interface.
