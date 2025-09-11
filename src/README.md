PSLP Support — Instance Generator & Validator
===================================================

Utilities for the Parallel Stack Loading Problem (PSLP):
- `gen_instance.py` — create valid instances.
- `validator.py` — validate instances/solutions and compute the objective `J(u)` (blocking pairs).

Python: 3.10+ recommended (uses type hints).  
License: same as the main repo (see top-level LICENSE).

---------------------------------------------------
File formats
---------------------------------------------------

Instance (.txt)
---------------
Three lines:
```
T S
N
p1 p2 ... pN
```

- **T**: number of tiers (capacity per stack).  
- **S**: number of stacks.  
- **N**: number of items (`1 ≤ N ≤ T*S`).  
- **p1..pN**: retrieval priorities.  
  - Each `p_i ∈ [1..N]`.  
  - Either a permutation (all distinct) or may include duplicates (if generated with `--allow-duplicates`).  
  - The list position `i` is the arrival index of item `i`.  

Notes:
- The bay may be full (`N = T*S`) or partially filled (`N < T*S`).  
- Retrieval orders may be unique or duplicated.  

Solution (.txt)
---------------
One line (or whitespace-separated) with N integers:
```
u1 u2 ... uN
```

- Each `u_i ∈ {1..S}` — the stack assigned to item `i` (by arrival order).  
- Capacity rule: each stack can hold **at most T items**.  

---------------------------------------------------
Instance Generator — gen_instance.py
---------------------------------------------------

Create instances with random retrieval orders.

Usage:
```
python gen_instance.py --tiers T --stacks S [--items N] [--seed SEED] [--allow-duplicates] [-o OUTPUT]
```

Options:
- `-T, --tiers (int, required)`: number of tiers T.  
- `-S, --stacks (int, required)`: number of stacks S.  
- `-N, --items (int, optional)`: number of items N (default = T*S). Must satisfy `1 ≤ N ≤ T*S`.  
- `--seed (int, optional)`: RNG seed for reproducibility.  
- `--allow-duplicates`: generate priorities with possible duplicates (values in `[1..N]`).  
- `-o, --output (path, optional)`: output path; “-” or omitted → stdout.  

Examples:
```
# 4x3 bay, N = 12, priorities are a permutation
python gen_instance.py -T 4 -S 3

# 3x2 bay with N = 4, permutation priorities
python gen_instance.py -T 3 -S 2 -N 4 --seed 123

# 4x3 bay with N = 7, duplicate priorities allowed
python gen_instance.py -T 4 -S 3 -N 7 --allow-duplicates --seed 7
```

---------------------------------------------------
Validator — validator.py
---------------------------------------------------

Checks validity of instance and solution files, and computes `J(u)`.

Usage:
```
python validator.py -i INSTANCE -s SOLUTION [--quiet]
```

Options:
- `-i, --instance`: path to instance file.  
- `-s, --solution`: path to solution file.  
- `--quiet`: only print J(u), suppress extra output.  

Exit codes:
- `0`: OK (valid instance + solution)  
- `1`: CLI / I/O error  
- `2`: Invalid instance  
- `3`: Invalid solution  

Examples:
```
# Validate and show details
python validator.py -i instance.txt -s solution.txt

# Validate and print only J(u)
python validator.py -i instance.txt -s solution.txt --quiet
```

---------------------------------------------------
Objective Scoring
---------------------------------------------------

`J(u)` counts blocking pairs:  

- For any `i < j` in the same stack,  
- If `p_i < p_j` then pair `(i,j)` contributes `1`.  

Arrival order is the natural index `i=1..N`.  
Within each stack, items are stored bottom-to-top in arrival order.  
