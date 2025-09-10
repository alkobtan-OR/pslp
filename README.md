<!--
SPDX-FileCopyrightText: 2025 Mohamed ElWakil <m.elwakil@f-eng.tanta.edu.eg>
SPDX-FileCopyrightText: 2025 Tomás Marques <tmarques0580@gmail.com>

SPDX-License-Identifier: CC-BY-4.0
-->

# The Parallel Stack Loading Problem Minimizing the Number of Blockings 

Mohamed ElWakil, Production Engineering and Mechanical Design Departement, Faculty of Engineering, Tanta University, Tanta, Egypt 

Tomás Marques, Portugal

Copyright 2025 Mohamed ElWakil and Tomás Marques 

This document is licensed under CC-BY-4.0.

## Introduction

Items of identical size arrive at a storage bay and are stored in vertical stacks. After some time, these items must be retrieved according to a sequence that may differ 
from the original storage order. Since the retrieval process operates under a last-in–first-out (LIFO) policy, blocking items may occur. A blocking item is defined as an item whose 
retrieval date is later than that of another item(s) located beneath it. In such cases, the blocking item must be relocated to enable access to the underlying items. 
These relocations represent additional handling operations, and minimizing their number is a key objective in optimizing the efficiency of the storage and retrieval process. 
(ElWakil _et al._, 2022). 

## Task

The problem consists in determining how to stack the arriving items in a storage bay with definite area so that the number of blockings is minimized. 

## Detailed description

The parallel stack loading problem considers stacking $N$ items. For each item, there is an arriving order $i$ and a retrieval order $p_i$; the larger the value of $p_i$, the later 
the retrieval date. The objective is stack the items in a storage bay which is empty at the beginning of the planning horizon. The storage bay is 
composed of $S$ vertical stacks, where at most $T$ items can be stored in each stack $(ST = N)$. 

Lets say we have a group of itmes with $N = 6$ to be stacked in a storage bay with $S = 2$ and $T = 3$. If the arrival order is as follows
#### Arrival order (instance) 
```
[4] <-- [1] <-- [6] <-- [2] <-- [3] <-- [5]
```
Item 4 is the first to arrive, then item 1 until item 5 is the last to arrive. Item is labelled with its retrieval order as we say item $p_i$. Based on that, item 6 is the third to
arrive and the last one to be retrieved. A number of different solution can be generted for stacking the mentioned items. For example, 

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

For a pair of items, if item $p_i$ arrives before item $p_j$, if both items are stored in the same stack, item $p_j$ will be at 
a higher tier than item $i$. For instance, if items 6 and 2 are stacked in the same stack as in solution 2, item 2 is at tier 3 while item 6 is at tier 2 as item arrives before 
item 6. Additionally if $p_j < p_i$, it means that item $i$ whould be retrieved earlier than item $j$. To do so, item $j$ would be relocated to somewhere else
first to retreive item $i$. Therefore, item $j$ is called a blocking item. For example, item 6 blocks item 1 at solution 1, where it does not block any item at solution 1.  

Let, $c_{ij} = 1$ if item $j$ would be a blocking item if it is stacked with item $i$ in the same stack satisfying the order of arrival and the first-come-first-stacked policy. And
$y_{ij} = 1 if item $i$ and $j$ are stacked in the same stack, 0 otherwise. Therefore the objective function is: 

$$ \min \sum_i \sum_j c_{ij} y_{ij}$$

A decision variable defined as $x_{is} = 1$ if item $i$ is stored in stack $s$, 0 otherwise. 

A solution is a vectore $u = (u_1, u_2, \dots, u_N)$ such that $1 \leq u_i \leq S$ and $ \sum {i=1}^{N} [u_i = s] = H for all $1 \leq s \leq S$, where $u_i$ denotes the stack number
where item $i$ is stacked and $u_i=s$ if $x_{is} = 1$ and $0$ otherwise.  


## Instance data file

The first line of the input contains two space-separated integers, $T$ and
$S$, where $T$ is the number of tiers, and $S$ is the number of stacks.

The second line contains $N$ the number of itmes to be stored. 

The third line contains $N$ space-separated integers, $p_1, p_2, \dots, p_M$,
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

$J(u) = 7

### Explanation

There are $7$ blocking items. items 7, 11, 1, 12 are stacked in stack 1 following the same order from bottom to top since it is the order of arrival. Such stack has two blocking
items: items 11 and 12. Stack 2: blocking items 4 and 5. Stack 3: blocking items 6, 9, and 10. 

## Acknowledgement

000

## References

M. ElWakil, A. Eltawil, and M. Gheith (2022). "On the integration of the parallel stack loading problem with the block relocation problem" *Computers and Operations Research*, 
138, 105609.
\[ [DOI](https://doi.org/10.1016/j.cor.2021.105609) \]

