#!/usr/bin/env python3
"""
PSLP — Validator

Instance format (three lines):
  1) "T S"
  2) N               (must equal T*S)
  3) p_1 ... p_N     (permutation of 1..N, retrieval order)

Solution format:
  One or more whitespace-separated integers: u_1 ... u_N
  where each u_i in {1..S} and each stack has exactly T items.

Exit codes:
  0 -> OK (valid)            1 -> CLI / I/O error
  2 -> Invalid instance      3 -> Invalid solution
"""

import argparse
import sys
from collections import Counter, defaultdict


def read_instance(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            line1 = f.readline()
            if not line1:
                raise ValueError("Missing line 1 (T S).")
            parts = line1.split()
            if len(parts) != 2:
                raise ValueError("Line 1 must have exactly two integers: T S.")
            T, S = map(int, parts)

            line2 = f.readline()
            if not line2:
                raise ValueError("Missing line 2 (N).")
            N = int(line2.strip())

            line3 = f.readline()
            if not line3:
                raise ValueError("Missing line 3 (p_1 ... p_N).")
            p = list(map(int, line3.split()))
    except OSError as e:
        print(f"[ERROR] Cannot read instance file: {e}", file=sys.stderr)
        raise
    return T, S, N, p


def validate_instance(T: int, S: int, N: int, p: list[int]) -> None:
    # Basic types / positivity
    if any(x <= 0 for x in (T, S, N)):
        raise ValueError("T, S and N must be positive integers.")

    # N = T*S
    if N != T * S:
        raise ValueError(f"N != T*S (got N={N}, T*S={T*S}).")

    # p must be a permutation of 1..N
    if len(p) != N:
        raise ValueError(f"Line 3 must have exactly N={N} integers.")
    if sorted(p) != list(range(1, N + 1)):
        raise ValueError("p is not a permutation of 1..N.")


def read_solution(path: str, expected_N: int):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read().split()
            if not data:
                raise ValueError("Solution file is empty.")
            u = list(map(int, data))
    except OSError as e:
        print(f"[ERROR] Cannot read solution file: {e}", file=sys.stderr)
        raise

    if len(u) != expected_N:
        raise ValueError(f"Solution must contain exactly N={expected_N} integers (got {len(u)}).")
    return u


def validate_solution(u: list[int], S: int, T: int) -> None:
    # Domain
    if not all(1 <= s <= S for s in u):
        raise ValueError("All u_i must be in {1..S}.")

    # Capacity per stack: exactly T items per stack
    cnt = Counter(u)
    for s in range(1, S + 1):
        if cnt.get(s, 0) != T:
            raise ValueError(f"Stack {s} has {cnt.get(s,0)} items (expected {T}).")


def score_J(u: list[int], p: list[int], S: int) -> int:
    """
    J(u) counts blocking pairs:
      For any i<j in the same stack, if p_i < p_j then (i,j) contributes 1.
    Arrival order is the natural index i=1..N; within each stack, items are
    stored bottom-to-top in arrival order.
    """
    N = len(u)
    stacks = defaultdict(list)
    for i in range(1, N + 1):     # arrival order
        stacks[u[i - 1]].append(i)

    J = 0
    for s in range(1, S + 1):
        col = stacks[s]  # arrival-ordered list (bottom to top)
        L = len(col)
        for a in range(L):
            i = col[a]
            for b in range(a + 1, L):
                j = col[b]
                if p[i - 1] < p[j - 1]:
                    J += 1
    return J


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate a PSLP solution and compute J(u).")
    parser.add_argument("-i", "--instance", required=True, help="Path to instance file.")
    parser.add_argument("-s", "--solution", required=True, help="Path to solution file.")
    parser.add_argument("--quiet", action="store_true", help="Only print J on success.")
    args = parser.parse_args(argv)

    # Read & validate instance
    try:
        T, S, N, p = read_instance(args.instance)
        validate_instance(T, S, N, p)
    except Exception as e:
        print(f"[INVALID INSTANCE] {e}", file=sys.stderr)
        return 2

    # Read & validate solution
    try:
        u = read_solution(args.solution, N)
        validate_solution(u, S, T)
    except Exception as e:
        print(f"[INVALID SOLUTION] {e}", file=sys.stderr)
        return 3

    # Score
    J = score_J(u, p, S)

    if args.quiet:
        print(J)
    else:
        print("OK")
        print(f"T={T}  S={S}  N={N}")
        print(f"J(u) = {J}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
