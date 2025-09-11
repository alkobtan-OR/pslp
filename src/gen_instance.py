#!/usr/bin/env python3
"""
Parallel Stack Loading Problem (PSLP) — Instance Generator

Format (three lines):
  1) "T S"                      # tiers, stacks
  2) N                          # number of items (1 <= N <= T*S)
  3) p_1 p_2 ... p_N            # retrieval priorities; either a permutation of 1..N
                                # or (if --allow-duplicates) integers from 1..N with repetitions

Usage examples:
  # Classic case (permutation, N = T*S)
  python gen_instance.py --tiers 4 --stacks 3 --seed 42

  # N < T*S (permutation, no duplicates)
  python gen_instance.py -T 3 -S 4 -N 7 --seed 123

  # With duplicates (priorities from 1..N, may repeat)
  python gen_instance.py -T 4 -S 3 -N 10 --allow-duplicates --seed 99
"""

import argparse
import random
import sys
from typing import List, Optional


def build_priorities(N: int, seed: Optional[int], allow_duplicates: bool) -> List[int]:
    """Generate the retrieval priorities list.

    If duplicates are not allowed:
        -> return a random permutation of 1..N
    If duplicates are allowed:
        -> return a list of N integers, each uniformly chosen from 1..N
    """
    rng = random.Random(seed)

    if not allow_duplicates:
        # Permutation of 1..N
        P = list(range(1, N + 1))
        rng.shuffle(P)
        return P

    # With duplicates: sample N integers uniformly in [1..N]
    return [rng.randint(1, N) for _ in range(N)]


def generate_instance(
    T: int,
    S: int,
    N: Optional[int] = None,
    seed: Optional[int] = None,
    allow_duplicates: bool = False,
) -> str:
    """Generate one PSLP instance as a string in the 3-line format."""

    # Validate tiers (T) and stacks (S)
    if not isinstance(T, int) or not isinstance(S, int) or T <= 0 or S <= 0:
        raise ValueError("tiers (T) and stacks (S) must be positive integers.")

    # Determine N
    if N is None:
        N = T * S
    if not isinstance(N, int) or N <= 0:
        raise ValueError("N must be a positive integer.")
    if N > T * S:
        raise ValueError("N cannot exceed T*S (total capacity).")

    # Build the priority list
    P = build_priorities(N, seed, allow_duplicates)

    # Format the instance as 3 lines
    out = []
    out.append(f"{T} {S}")                 # line 1
    out.append(str(N))                     # line 2
    out.append(" ".join(map(str, P)))      # line 3
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate PSLP instances (supports N <= T*S and duplicate priorities)."
    )
    parser.add_argument("-T", "--tiers", type=int, required=True, help="Number of tiers (T).")
    parser.add_argument("-S", "--stacks", type=int, required=True, help="Number of stacks (S).")
    parser.add_argument(
        "-N", "--items", type=int, default=None,
        help="Number of items N (default: T*S). Must satisfy 1 <= N <= T*S."
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument(
        "--allow-duplicates",
        action="store_true",
        help="Allow duplicate priorities in the retrieval list (values in 1..N may repeat)."
    )
    parser.add_argument(
        "-o", "--output", type=str, default="-",
        help="Output path (default: stdout)."
    )
    args = parser.parse_args(argv)

    try:
        content = generate_instance(
            T=args.tiers,
            S=args.stacks,
            N=args.items,
            seed=args.seed,
            allow_duplicates=args.allow_duplicates,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.output == "-" or args.output is None:
        sys.stdout.write(content)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
