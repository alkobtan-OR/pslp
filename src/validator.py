#!/usr/bin/env python3
"""
PSLP — Validator (relaxed for N <= T*S and duplicate priorities)

Instance format (three lines):
  1) "T S"
  2) N               (must satisfy 1 <= N <= T*S)
  3) p_1 ... p_N     (integers in 1..N; duplicates allowed)

Solution format:
  One or more whitespace-separated integers: u_1 ... u_N
  where each u_i in {1..S} and each stack has at most T items (capacity <= T).

Exit codes:
  0 -> OK (valid)            1 -> CLI / I/O error
  2 -> Invalid instance      3 -> Invalid solution
"""

import argparse
import sys
from collections import Counter, defaultdict
from typing import Tuple, List


def read_instance(path: str) -> Tuple[int, int, int, List[int]]:
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


def validate_instance(T: int, S: int, N: int, p: List[int]) -> None:
    # Basic checks: positive integers
    if any(x <= 0 for x in (T, S, N)):
        raise ValueError("T, S and N must be positive integers.")

    # Capacity bound
    cap = T * S
    if N > cap:
        raise ValueError(f"N exceeds capacity T*S (got N={N}, T*S={cap}).")

    # Priorities length
    if len(p) != N:
        raise ValueError(f"Line 3 must have exactly N={N} integers (got {len(p)}).")

    # Priorities range (duplicates allowed, but must be in 1..N)
    if not all(1 <= x <= N for x in p):
        raise ValueError("All priorities p_i must be integers in 1..N (duplicates allowed).")


def read_solution(path: str, expected_N: int) -> List[int]:
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


def validate_solution(u: List[int], S: int, T: int) -> None:
    # Domain: assignments must point to valid stacks
    if not all(1 <= s <= S for s in u):
        raise ValueError("All u_i must be in {1..S}.")

    # Capacity per stack: at most T items
    cnt = Counter(u)
    for s in range(1, S + 1):
        if cnt.get(s, 0) > T:
            raise ValueError(f"Stack {s} has {cnt.get(s,0)} items (capacity {T} exceeded).")


def score_J(u: List[int], p: List[int], S: int) -> int:
    """
    J(u) counts blocking pairs:
      For any i<j in the same stack, if p_i < p_j then (i,j) contributes 1.
    Arrival order is the natural index i=1..N; within each stack, items are
    stored bottom-to-top in arrival order.
    """
    N = len(u)
    J = 0
    for i in range(N - 1):
        for j in range(i + 1, N):
            if u[i] == u[j] and p[i] < p[j]:
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
