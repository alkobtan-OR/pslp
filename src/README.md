PSLP Support — Instance Generator & Validator
===================================================

Utilities for the Parallel Stack Loading Problem (PSLP):
- pslp_gen_instance.py — create valid instances.
- pslp_validator.py — validate solutions and compute the objective J(u) (blocking pairs).

Python: 3.10+ recommended (uses type hints).
License: same as the main repo (see top-level LICENSE).

---------------------------------------------------
File formats
---------------------------------------------------

Instance (.txt)
---------------
Three lines:
  T S
  N
  p1 p2 ... pN

- T: number of tiers (capacity per stack)
- S: number of stacks
- N: number of items (must equal T*S)
- p1..pN: permutation of 1..N (retrieval orders); the list position i is the arrival index.

Assumptions:
- All stacks have equal capacity T and the bay is exactly full (TS=N).
- Retrieval orders are distinct (no ties).

Solution (.txt)
---------------
One line (or whitespace-separated) with N integers:
  u1 u2 ... uN

- ui ∈ {1..S} — the stack assigned to item i (arrival order).
- Capacity rule: each stack appears exactly T times.

---------------------------------------------------
Instance Generator — pslp_gen_instance.py
---------------------------------------------------

Create instances with random retrieval orders.

Usage:
  python pslp_gen_instance.py --tiers T --stacks S [--seed SEED] [-o OUTPUT]
  python pslp_gen_instance.py -T T -S S [--seed SEED] [-o OUTPUT]

Options:
- -T, --tiers (int, required): number of tiers T.
- -S, --stacks (int, required): number of stacks S.
- --seed (int, optional): RNG seed for reproducibility.
- -o, --output (path, optional): file path; “-” or omitted → stdout.

Examples:
  # 4x3 bay, print to stdout
  python pslp_gen_instance.py -T 4 -S 3

  # 3x2 bay with fixed seed, write to file
  python gen_instance.py -T 3 -S 2 --seed 123 -o instance.txt

---------------------------------------------------
Validator — pslp_validator.py
---------------------------------------------------

Checks validity of instance and solution files, and computes J(u).

Usage:
  python pslp_validator.py -i INSTANCE -s SOLUTION [--quiet]

Options:
- -i, --instance: path to instance file.
- -s, --solution: path to solution file.
- --quiet: only print J(u), suppress extra output.

Exit codes:
- 0: OK (valid instance + solution)
- 1: CLI / I/O error
- 2: Invalid instance
- 3: Invalid solution

Examples:
  # Validate and show details
  python pslp_validator.py -i instance.txt -s solution.txt

  # Validate and print only J(u)
  python pslp_validator.py -i instance.txt -s solution.txt --quiet

---------------------------------------------------
Objective Scoring
---------------------------------------------------

J(u) counts blocking pairs:
- For any i<j in the same stack,
- If p_i < p_j then (i,j) contributes 1.

Arrival order is the natural index i=1..N.
Within each stack, items are stored bottom-to-top in arrival order.
