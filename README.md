<!--
SPDX-FileCopyrightText: 2025 Mohamed ElWakil <m.elwakil@f-eng.tanta.edu.eg>
SPDX-FileCopyrightText: 2025 Tomás Marques <tmarques0580@gmail.com>

SPDX-License-Identifier: CC-BY-4.0
-->

# The Parallel Stack Loading Problem  

Mohamed ElWakil, Production Engineering and Mechanical Design Department, Faculty of Engineering, Tanta University, Tanta, Egypt 

Tomás Marques, Department of Production and Systems, University of Minho, Portugal

Copyright 2025 Mohamed ElWakil and Tomás Marques 

This document is licensed under CC-BY-4.0.

## Introduction

Items of identical size arrive at a storage bay and are stored in vertical stacks satisfying the first-come-first-stored policy. After some time, these items must be retrieved according to a sequence that may differ 
from the original storage order. Since the retrieval process operates under a last-in–first-out policy, blocking items may occur. A blocking item is defined as an item whose 
retrieval date is later than that of another item(s) located beneath it. In such cases, the blocking item must be relocated to enable access to the underlying items. 
These relocations represent additional handling operations, and minimizing their number is a key objective in optimizing the efficiency of the storage and retrieval process. 
(ElWakil _et al._, 2022). 

## Task

The problem consists of determining how to stack the arriving items in a storage bay with definite area (defined by a number of horizontal tiers and vertical stacks) so that the number of blockings is minimized. 

## Detailed description

The parallel stack loading problem considers stacking $N$ items. For each item, there is an arriving order $i$ and a retrieval order $p_i$; the larger the value of $p_i$, the later 
the retrieval date. The objective is to stack the items in a storage bay which is empty at the beginning of the planning horizon. The storage bay is 
composed of $S$ vertical stacks, where at most $T$ items can be stored in each stack $(ST = N)$. 

Let's say we have a group of items with $N = 6$ to be stacked in a storage bay with $T = 3$ and $S = 2$ while the arrival order is as follows:
```
[4] <-- [1] <-- [6] <-- [2] <-- [3] <-- [5]
```
Graphically, and for ease of notation, each item is labelled with its retrieval order in brackets. For instance, we say item 1 (or item [4]) is the first one to arrive. In the same way, the second arriving item is item 2 (or item [1]) and item 6 (or item [5]) is the last to arrive. A number of different solutions can be generated for stacking the mentioned items. For example, two different solutions (storage bays) are shown. 

```
T3   |   [2]   [5]                                      T3   |   [5]   [2]
T2   |   [1]   [3]                                      T2   |   [3]   [6]
T1   |   [4]   [6]                                      T1   |   [4]   [1]
      ----------------                                        ----------------
          S1    S2                                                S1    S2
        solution 1                                             solution 2 
```
#


For a pair of items, if item $i$ arrives earlier than item $j$ ($i < j$) and both items are placed in the same stack, then item $j$ will be above $i$. If, in addition, $p_i < p_j$ (so item $i$ must be retrieved before item $j$), then item $j$ would block item $i$ if they are stacked together.

For example, in solution 2 , items [6] and [1] are in the same stack. Item [1] is at tier 1 while item [6] as item [1] arrives before item [6]. In addition, item [6] must be relocated first to retrieve item [1]; therefore item [6] is a blocking item. In solution 1, item [6] does not block any item.

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

This parameter is derived from the arrival and retrieval orders only and does not depend on the solution.

---

## Decision Variables

We introduce the following binary decision variable:

$$
x_{is} =
\begin{cases}
1, & \text{if item $i$ is stored in stack $s$}, \\
0, & \text{otherwise}
\end{cases}
\qquad \forall\ i=1,\dots,N,\forall\ s=1,\dots,S.
$$

We also define the following derived binary variable: 

$$
y_{ij} =
\begin{cases}
1, & \text{if items $i$ and $j$ are stored in the same stack}, \\
0, & \text{otherwise}
\end{cases}
\qquad \forall\ 1 \le i < j \le N.
$$


There are two ways to link $y_{ij}$ with $x_i$ and $x_j$: 

#### Formulation 1 — Non-linear MIQP

This compact formulation uses bilinear products:

$$
y_{ij} = \sum_{s=1}^S x_{is} \cdot x_{js}, \quad \forall\ 1 \leq i < j \leq N,
$$


This is simple but non-linear, and requires a solver that supports quadratic binary terms.

#### Formulation 2 — Linearised MILP

To avoid bilinear terms, we linearize the bilinear products as follows: 

$$
\begin{aligned}
y_{ij} \ge x_{is} + x_{js} - 1,
\qquad &\forall\ 1 \le i < j \le N.
\end{aligned}
$$

These enforce $y_{ij}=1$ if both $i$ and $j$ are assigned to the same stack. This version is fully linear and can be solved with any MILP solver.

---

## Objective Function

The objective counts blocking pairs:

$$ 
J(u)=\sum_{i=1}^{N-1} \sum_{j=i+1}^{N} c_{ij} \cdot y_{ij}, \qquad \min_{u} J(u).
$$

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

where $u_i$ denotes the stack assigned to item $i$. Since the first-come-first-stacked policy is fulfilled, the items of the same stack are stored with the order of their arrival. In other words, the later arrival items are stacked above the earlier arrival ones. 

---

## Instance data file

The first line of the input contains two space-separated integers, $T$ and
$S$, where $T$ is the number of tiers, and $S$ is the number of stacks.

The second line contains $N$ the number of items to be stored. 

The third line contains $N$ space-separated integers, $p_1, p_2, \dots, p_N$,
corresponding to the number of items represented by their retrieval order.

---

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

$J(u) = 10$

### Explanation

##### Arrival order (instance) 
```
[7] <-- [11] <-- [8] <-- [3] <-- [10] <-- [1] <-- [2] <-- [9] <-- [6] <-- [12] <-- [4] <-- [5]
```

##### Storage bay (solution)
```
T4   |   [12]   [ 5]   [ 6]                                      
T3   |   [ 1]   [ 4]   [ 9]                                  
T2   |   [11]   [ 2]   [10]                                  
T1   |   [ 7]   [ 8]   [ 3]                                   
      ----------------------                                  
          S1     S2     S3                                
```
#


Each stack is listed from bottom to top according to the arrival order.  
Blocking pairs $(i,j)$ are identified whenever item $i$ is below item $j$ in the same stack and $p_i < p_j$ (i.e., item $i$ must be retrieved before item $j$).  

- **Stack 1:** items [7], [11], [1], [12]  
  Blocking pairs: **(7,11), (7,12), (11,12), (1,12)** → 4

- **Stack 2:** items [8], [2], [4], [5]  
  Blocking pairs: **(2,4), (2,5), (4,5)** → 3

- **Stack 3:** items [3], [10], [9], [6]  
  Blocking pairs: **(3,10), (3,9), (3,6)** → 3

The total number of blocking pairs is therefore $4+3+3=10$.  
Hence, the objective value for this solution is $J(u)=10$.

## Acknowledgement

000

## References

M. ElWakil, A. Eltawil, and M. Gheith (2022). "On the integration of the parallel stack loading problem with the block relocation problem" *Computers and Operations Research*, 
138, 105609.
\[ [DOI](https://doi.org/10.1016/j.cor.2021.105609) \]

