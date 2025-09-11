<!--
SPDX-FileCopyrightText: 2025 Mohamed ElWakil <m.elwakil@f-eng.tanta.edu.eg>
SPDX-FileCopyrightText: 2025 Tomás Marques <tmarques0580@gmail.com>

SPDX-License-Identifier: CC-BY-4.0
-->

# The Parallel Stack Loading Problem Minimizing the Number of Blockings 

Mohamed ElWakil, Production Engineering and Mechanical Design Department, Faculty of Engineering, Tanta University, Tanta, Egypt 

Tomás Marques, Department of Production and Systems, University of Minho, Portugal

Copyright 2025 Mohamed ElWakil and Tomás Marques 

This document is licensed under CC-BY-4.0.

## Introduction

Items of identical size arrive at a storage bay and are stored in vertical stacks. After some time, these items must be retrieved according to a sequence that may differ 
from the original storage order. Since the retrieval process operates under a last-in–first-out (LIFO) policy, blocking items may occur. A blocking item is defined as an item whose 
retrieval date is later than that of another item(s) located beneath it. In such cases, the blocking item must be relocated to enable access to the underlying items. 
These relocations represent additional handling operations, and minimizing their number is a key objective in optimizing the efficiency of the storage and retrieval process. 
(ElWakil _et al._, 2022). 

## Task

The problem consists of determining how to stack the arriving items in a storage bay with definite area so that the number of blockings is minimized. 

## Detailed description

The parallel stack loading problem considers stacking $N$ items. For each item, there is an arriving order $i$ and a retrieval order $p_i$; the larger the value of $p_i$, the later 
the retrieval date. The objective is to stack the items in a storage bay which is empty at the beginning of the planning horizon. The storage bay is 
composed of $S$ vertical stacks, where at most $T$ items can be stored in each stack $(ST = N)$. 

Let's say we have a group of items with $N = 6$ to be stacked in a storage bay with $S = 2$ and $T = 3$. If the arrival order is as follows
#### Arrival order (instance) 
```
[4] <-- [1] <-- [6] <-- [2] <-- [3] <-- [5]
```
Item 4 is the first to arrive, then item 1 until item 5 is the last to arrive. Each item is labelled with its retrieval order as we say item $p_i$. Based on that, item 6 is the third to
arrive and the last one to be retrieved. A number of different solutions can be generated for stacking the mentioned items. For example, 

##### Storage bay (solution)
```
T3   |   [2]   [5]                                      T3   |   [5]   [2]
T2   |   [1]   [3]                                      T2   |   [3]   [6]
T1   |   [4]   [6]                                      T1   |   [4]   [1]
      ----------------                                        ----------------
          S1    S2                                                S1    S2
        solution 1                                             solution 2 
```
#

For a pair of items, if item $i$ arrives earlier than item $j$ and both items are placed in the same stack, then $j$ will be above $i$. 
If, in addition, $p_i < p_j$ (so $i$ must be retrieved before $j$), then $j$ would block $i$ if they are stacked together.

For example, in solution 2 , if items 6 and 2 are in the same stack, item 2 is at tier 3 while item 6 is at tier 2 (because 6 arrives before 2). Since $p_6 < p_2$, item 2 must be relocated first to retrieve item 6; therefore item 2 is a blocking item. In solution 1, item 6 blocks item 1; in solution 2, it does not block any item.

---

## Blocking Relation

For all pairs with $i<j$ (item $i$ arrives earlier than item $j$), define the blocking parameter

$$
c_{ij} =
\begin{cases}
1, & \text{if } p_i < p_j \\
0, & \text{otherwise}
\end{cases}
\qquad \forall\ 1 \le i < j \le N.
$$

This parameter is derived from the retrieval order only and does not depend on the solution.

---

## Decision Variables

We introduce the following binary decision variables:

$$
x_{is} =
\begin{cases}
1, & \text{if item $i$ is stored in stack $s$}, \\
0, & \text{otherwise}
\end{cases}
\qquad \forall i=1,\dots,N,\ s=1,\dots,S.
$$

$$
y_{ij} =
\begin{cases}
1, & \text{if items $i$ and $j$ are stored in the same stack}, \\
0, & \text{otherwise}
\end{cases}
\qquad \forall\ 1 \le i < j \le N.
$$

$$
w_{ijs} =
\begin{cases}
1, & \text{if items $i$ and $j$ are both assigned to stack $s$}, \\
0, & \text{otherwise}
\end{cases}
\qquad \forall\ 1 \le i < j \le N,\ s=1,\dots,S.
$$

---

## Objective Function

We present two solver formulations of the optimisation problem.

### Formulation 1 — Non-linear MIQP

This compact formulation uses bilinear products:

$$
y_{ij} = \sum_{s=1}^S x_{is} \cdot x_{js}, \quad \forall\ i < j,
$$

The objective counts blocking pairs:

$$ 
J(u)=\sum_{i < j} c_{ij}\, y_{ij}, \qquad \min_{u} J(u).
$$

This is simple but non-linear, and requires a solver that supports quadratic binary terms.

---

### Formulation 2 — Linearised MILP

To avoid bilinear terms, we introduce auxiliary binaries $w_{ijs} \in \{0,1\}$ for each pair $(i,j)$ and stack $s$:

$$
\begin{aligned}
w_{ijs} &\le x_{is}, \\
w_{ijs} &\le x_{js}, \\
w_{ijs} &\ge x_{is} + x_{js} - 1,
\qquad &\forall\ 1 \le i < j \le N,\ s=1,\dots,S.
\end{aligned}
$$

These enforce $w_{ijs}=1$ if both $i$ and $j$ are assigned to stack $s$.

Two equivalent options exist for the objective:

- **Option A (with $y_{ij}$):**
  
$$
y_{ij} = \sum_{s=1}^S w_{ijs}, \quad \forall i < j, \qquad y_{ij}\in\{0,1\},
$$
  
$$
J(u) = \sum_{i < j} c_{ij}\, y_{ij}, \qquad \min_{u} J(u).
$$

- **Option B (without $y_{ij}$):**
  
$$
J(u) = \sum_{i < j} c_{ij} \sum_{s=1}^S w_{ijs}, \qquad \min_{u} J(u).
$$

This version is fully linear and can be solved with any MILP solver.

---

## Constraints

The decision variables satisfy the following constraints:

- Each item is placed in exactly one stack:
  
$$
\sum_{s=1}^S x_{is} = 1 \quad \forall i.
$$

- Each stack contains exactly $T$ items:
  
$$
\sum_{i=1}^N x_{is} = T \quad \forall s.
$$

---

## Alternate Representation 

A solution can also be represented as a vector:

$$
u = (u_1, u_2, \dots, u_N), \quad u_i \in \{1,\dots,S\}.
$$

with

$$
\sum_{i=1}^{N} [u_i = s] = T \quad \forall s \in \{1,\dots,S\}.
$$

where $u_i$ denotes the stack assigned to item $i$.




## Instance data file

The first line of the input contains two space-separated integers, $T$ and
$S$, where $T$ is the number of tiers, and $S$ is the number of stacks.

The second line contains $N$ the number of items to be stored. 

The third line contains $N$ space-separated integers, $p_1, p_2, \dots, p_N$,
corresponding to the number of items represented by their retrieval order.

## Solution file

A solution file lists the stack numbers $u_1, u_2, \dots, u_N$.

## Example

### Instance

```
4 3
12
7 11 8 3 10 1 2 9 6 12 4 5 
```

### Solution

```
1 1 2 3 3 1 2 3 3 1 2 2 
```

$J(u) = 12$

### Explanation

Each stack is listed from bottom to top according to the arrival order.  
Blocking pairs $(i,j)$ are identified whenever item $i$ is below item $j$ in the same stack and $p_i < p_j$ (i.e., item $i$ must be retrieved before item $j$).  

- **Stack 1:** items [1, 2, 6, 10]  
  Blocking pairs: **(1,2), (1,10), (2,10), (6,10)** → 4

- **Stack 2:** items [3, 7, 11, 12]  
  Blocking pairs: **(7,11), (7,12), (11,12)** → 3

- **Stack 3:** items [4, 5, 8, 9]  
  Blocking pairs: **(4,5), (4,8), (4,9), (5,9), (8,9)** → 5

The total number of blocking pairs is therefore $4+3+5=12$.  
Hence, the objective value for this solution is $J(u)=12$.

## Acknowledgement

000

## References

M. ElWakil, A. Eltawil, and M. Gheith (2022). "On the integration of the parallel stack loading problem with the block relocation problem" *Computers and Operations Research*, 
138, 105609.
\[ [DOI](https://doi.org/10.1016/j.cor.2021.105609) \]

