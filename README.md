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

Items such as boxes arrive at a storage bay and are stored in vertical stacks satisfying the first-come-first-stacked policy. After some time, these items must be retrieved according to a retrieval order that may differ 
from the original storage order. Since the retrieval process operates under a last-in-first-out policy, blocking items may occur. A blocking item is defined as an item whose 
retrieval date is later than that of other item(s) located beneath it. In such cases, the blocking item must be relocated to enable access to the underlying items. 
These relocations represent additional handling operations, and minimizing their number is a key objective in optimizing the efficiency of the storage and retrieval process. 
(ElWakil _et al._, 2022). 

## Task

The problem consists of determining how to stack the arriving items in a storage bay with a fixed area (defined by a number of horizontal tiers and vertical stacks) so that the number of blocking pairs is minimized. 

## Detailed description

The parallel stack loading problem considers stacking $N$ items. For each item, there is an arrival order $i$ and a retrieval order $p_i$; the larger the value of $p_i$, the later the retrieval date. The aim is to stack the items in a storage bay which is composed of $S$ vertical stacks, where a maximum of $T$ items can be stored in each stack.

### Key characterstics
1- Items are assumed to have identical sizes and the individual slots of the storage bay match this size. 

2- The bay is assumed to be empty at the beginning of the planning horizon. 

3- The bay may be full after stacking all the items if $ST = N$. Alternatively, if $ST > N$, therfore the bay will not be fully occupied. 

4- Items may or may not have unique retrieval orders i.e. more than one item may share the same retreival order. 

### Example - Full bay with unique retrieval orders 
Let's say we have a group of items with $N = 6$ to be stacked in a storage bay with $T = 3$ and $S = 2$ while the arrival order is as follows:
```
$i$      1      2      3      4      5      6
$p_i$   [4]    [1]    [6]    [2]    [3]    [5]
```
Graphically, and for ease of notation, each item is labelled with its retrieval order in brackets. For instance, we say item [4] is the first one to arrive. Similarly, the second arriving item is item [1] and item [5] is the last to arrive. A number of different solutions can be generated for stacking these items. For example, two possible solutions (storage bays) are shown. 

```
T3   |   [5]   [2]                                    T3   |   [2]   [5]                                      
T2   |   [3]   [6]                                    T2   |   [1]   [3]                                      
T1   |   [4]   [1]                                    T1   |   [4]   [6]                                      
      ----------------                                      ----------------
          S1    S2                                              S1    S2
        solution 1                                           solution 2 
```

## Blocking Relation

For a pair of items, if item $i$ arrives earlier than item $j$ ($i < j$) and both are placed in the same stack, then item $j$ will be above $i$. If, in addition, $p_i < p_j$ (so item $i$ must be retrieved before item $j$), then item $j$ will block item $i$ if they are stacked together.

For example, in solution 1, items [1], [6] and [2] are in the same stack. Item [1] is at tier 1 while item [6] is at tier 2 and item [2] is at tier 3, as item [1] arrives before item [6], which arrives before item [2]. In addition, items [6] and [2] must be relocated first to retrieve item [1]; therefore items [6] and [2] are blocking items. In solution 2, item [6] does not block any item whilst item [2] blocks item [1].


For all pairs with $i<j$ (item $i$ arrives earlier than item $j$), the blocking relation parameter is defined as follows: 

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

These constraints enforce $y_{ij}=1$ if both $i$ and $j$ are assigned to the same stack (i.e. $x_{is} = x_{js} = 1$). This version is fully linear and can be solved with any MILP solver.

---

## Objective Function

The objective counts the number of pairs that have a blocking relation and placed in the same stack:

$$ 
J(u)=\sum_{i=1}^{N-1} \sum_{j=i+1}^{N} c_{ij} \cdot y_{ij}, \qquad \min_{u} J(u).
$$

---

## Constraints

The decision variables satisfy the following constraints:

- Each item is placed in exactly one stack:
  
$$
\sum_{s=1}^S x_{is} = 1 \quad \forall i \in \{1, \dots, N\}.
$$

- Each stack contains at most $T$ items:
  
$$
\sum_{i=1}^N x_{is} \leq T \quad \forall s \in \{1, \dots, S\}.
$$

---

## Alternate Representation 

A solution can also be represented as a vector $u$, which lists the stack number where each item is placed. The elements of vector $u$ are ordered according to the items’ arrival sequence:

$$
u = (u_1, u_2, \dots, u_N), \quad u_i \in \{1,\dots,S\}.
$$

Since the first-come-first-stacked policy is followed, the items assigned to the same stack are stored in their order of arrival. In other words, later arriving items are stacked above earlier ones.

Considering the earlier mentioned example, the solution vector $u$ for the solution 1 and solution 2 are as follows: 

**solution 1**: u = (1, 2, 2, 2, 1, 1)

**solution 2**: u = (1, 1, 2, 1, 2, 2) 

It is important to note that a vital condition for the solution represented by $u$ to be feasible is that a maixmum of $T$ items can share the same stack number since each stack can hold at most $T$ items, i.e.,

$$
\sum_{i=1}^{N} [u_i = s] \leq T \quad \forall s \in \{1,\dots,S\}.
$$

---

## Instance data file

The input data can be structured in a plain text. 

The first line of the input contains two space-separated integers, $T$ and
$S$, where $T$ is the number of tiers, and $S$ is the number of stacks.

The second line contains a single integer, $N$, the number of items to be stored. 

The third line contains $N$ space-separated integers, $p_1, p_2, \dots, p_N$,
where $p_i$ denotes the retrieval order of item $i$ ($1$ = earliest, larger values = later). The order in which these integers are listed corresponds to their order of arrival. 

For example:
$$
T S  
N  
p_1 p_2 p_3 \dots p_n
$$

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

The first two lines of the instance defines $T = 4, S = 3$ and $N = 12$. The thrid line list the items in the order of their arrival order. 

##### Items 
```
i      1      2      3      4      5      6      7      8      9      10      11      12
p_i   [7]    [11]   [8]    [3]    [10]   [1]    [2]    [9]    [6]    [12]     [4]     [5]
```

Regarding the solution file, $u$ can be converted into the following storage bay. Items with $u_i = 1$ are items [7], [11], [1], [2]. The same applies for other stacks. Each stack is filled with the corresponding items from bottom to top according to the arrival order.  

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

This problem statement is based upon work from COST Action Randomised Optimisation Algorithms Research Network (ROAR-NET), CA22137, supported by COST (European Cooperation in Science and Technology).

## References

M. ElWakil, A. Eltawil, and M. Gheith (2022). "On the integration of the parallel stack loading problem with the block relocation problem" *Computers and Operations Research*, 
138, 105609.
\[ [DOI](https://doi.org/10.1016/j.cor.2021.105609) \]

