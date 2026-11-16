from collections import deque  # Importing deque for an efficient queue implementation (used in AC-3)
import time  # To measure time performance
import copy  # To deep copy domains so that we don't modify the original

# -----------------------------------------
# 1. Problem Definition (CSP Components)
# -----------------------------------------

# List of subjects (variables to assign time slots to)
variables = ["Math", "Physics", "Chemistry", "English"]

# Each subject has a list of valid time slots (its domain)
full_domains = {
    "Math": ["T1", "T2"],           # Math can be scheduled in T1 or T2
    "Physics": ["T1"],              # Physics is fixed to T1 only
    "Chemistry": ["T2", "T3"],      # Chemistry cannot be in T1
    "English": ["T1", "T2", "T3"]   # English has full flexibility
}

# Neighbors: subjects that share students (conflicts) and thus can't occur at the same time
neighbors = {
    "Math": ["Physics", "Chemistry"],
    "Physics": ["Math", "English"],
    "Chemistry": ["Math", "English"],
    "English": ["Physics", "Chemistry"]
}

# Constraint function: two conflicting exams cannot be at the same time
def constraint(x, y):
    return x != y  # Return True if times are different (no conflict)

# -----------------------------------------
# 2. AC-3 Algorithm to Reduce Domains
# -----------------------------------------

def ac3(domains, neighbors, constraint):
    # Initialize queue with all arcs (xi, xj) for each neighbor pair
    queue = deque([(xi, xj) for xi in neighbors for xj in neighbors[xi]])
    removed_values = []  # Track values removed for explanation

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj, constraint, removed_values):
            if not domains[xi]:
                return False, removed_values
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True, removed_values

# Revise function: remove inconsistent values from xi's domain
def revise(domains, xi, xj, constraint, removed_values):
    revised = False
    for x in domains[xi][:]:  # Iterate over a copy of xi's domain
        if all(not constraint(x, y) for y in domains[xj]):
            domains[xi].remove(x)
            removed_values.append((xi, x, xj))
            revised = True
    return revised

# -----------------------------------------
# 3. Backtracking Search
# -----------------------------------------

def backtracking_search(variables, domains, neighbors, constraint):
    return backtrack({}, variables, domains, neighbors, constraint)

def backtrack(assignment, variables, domains, neighbors, constraint):
    if len(assignment) == len(variables):
        return assignment
    var = select_unassigned_variable(assignment, variables)
    for value in domains[var]:
        if is_consistent(var, value, assignment, neighbors, constraint):
            assignment[var] = value
            result = backtrack(assignment, variables, domains, neighbors, constraint)
            if result:
                return result
            del assignment[var]
    return None

# Heuristic: pick first unassigned variable
def select_unassigned_variable(assignment, variables):
    for var in variables:
        if var not in assignment:
            return var

# Check whether assigning 'value' to 'var' does not conflict with neighbors
def is_consistent(var, value, assignment, neighbors, constraint):
    for neighbor in neighbors[var]:
        if neighbor in assignment and not constraint(value, assignment[neighbor]):
            return False
    return True

# -----------------------------------------
# 4. Run without AC-3 (Brute-force backtracking)
# -----------------------------------------

domains_without_ac3 = copy.deepcopy(full_domains)
start_time = time.time()
solution_no_ac3 = backtracking_search(variables, domains_without_ac3, neighbors, constraint)
end_time = time.time()

print("=== Without AC-3 ===")
if solution_no_ac3:
    for subj, time_slot in solution_no_ac3.items():
        print(f"{subj}: {time_slot}")
else:
    print("No valid schedule found.")
print(f"Time taken without AC-3: {end_time - start_time:.6f} seconds\n")

# -----------------------------------------
# 5. Run AC-3 Before Backtracking (Optimized)
# -----------------------------------------

domains_with_ac3 = copy.deepcopy(full_domains)
ac3_start = time.time()
ac3_result, removed = ac3(domains_with_ac3, neighbors, constraint)
ac3_end = time.time()

print("=== AC-3 Domain Pruning ===")
print("Values removed by AC-3:")
for xi, val, xj in removed:
    print(f"Removed '{val}' from '{xi}' due to inconsistency with '{xj}'")
print(f"Time spent on AC-3 preprocessing: {ac3_end - ac3_start:.6f} seconds\n")

if ac3_result:
    bt_start = time.time()
    solution_with_ac3 = backtracking_search(variables, domains_with_ac3, neighbors, constraint)
    bt_end = time.time()
    print("=== With AC-3 ===")
    if solution_with_ac3:
        for subj, time_slot in solution_with_ac3.items():
            print(f"{subj}: {time_slot}")
    else:
        print("No valid schedule found.")
    print(f"Time taken after AC-3: {bt_end - bt_start:.6f} seconds")
else:
    print("AC-3 detected no solution is possible — backtracking skipped.")
