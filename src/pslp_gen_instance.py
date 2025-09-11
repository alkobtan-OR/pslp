#!/usr/bin/env python3
"""
Parallel Stack Loading Problem (PSLP) — Instance Generator

Format (three lines):
  1) "T S"                      # tiers, stacks
  2) N                          # number of items (must equal T*S)
  3) p_1 p_2 ... p_N            # a permutation of 1..N (retrieval order)

Usage examples:
  python gen_instance.py --tiers 4 --stacks 3 --seed 42
  python gen_instance.py -T 3 -S 2 --seed 123 > instance.txt
"""

import argparse
import random
import sys


def build_retrieval_order(N: int, seed: int | None) -> list[int]:
    rng = random.Random(seed)
    P = list(range(1, N + 1))
    rng.shuffle(P)
    return P


def generate_instance(T: int, S: int, seed: int | None = None) -> str:
    if not isinstance(T, int) or not isinstance(S, int) or T <= 0 or S <= 0:
        raise ValueError("tiers (T) and stacks (S) must be positive integers.")

    N = T * S
    P = build_retrieval_order(N, seed)

    # Compose the instance as a string (three lines)
    out = []
    out.append(f"{T} {S}")
    out.append(str(N))
    out.append(" ".join(map(str, P)))
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate PSLP instances (requires N = T*S)."
    )
    parser.add_argument("-T", "--tiers", type=int, required=True, help="Number of tiers (T).")
    parser.add_argument("-S", "--stacks", type=int, required=True, help="Number of stacks (S).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument("-o", "--output", type=str, default="-",
                        help="Output path (default: stdout).")
    args = parser.parse_args(argv)

    try:
        content = generate_instance(args.tiers, args.stacks, args.seed)
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
