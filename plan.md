# Study Plan

Two phases. Finish one before starting the next.

---

## Phase 1 — NeetCode 150

150 problems across 18 pattern categories (28 easy, 101 medium, 21 hard). The categories are ordered by conceptual dependency, so earlier ones set up later ones. Work them top to bottom; inside a category, work easy → medium → hard.

| # | Category | Problems | Why it comes here |
|---|---|---|---|
| 1 | Arrays & Hashing | 9 | The foundation. Hash maps show up in every later category. |
| 2 | Two Pointers | 5 | Sorted-input scans; builds on array indexing. |
| 3 | Sliding Window | 6 | A natural extension of two pointers to contiguous ranges. |
| 4 | Stack | 7 | Parsing, nesting, and monotonic stacks. |
| 5 | Binary Search | 7 | Sorted data and monotone answer spaces. |
| 6 | Linked List | 11 | Pointer discipline, cycles, merging. |
| 7 | Trees | 15 | Recursion and BFS/DFS; the base for tries and graph search. |
| 8 | Tries | 3 | Prefix structures on top of tree traversal. |
| 9 | Heap / Priority Queue | 7 | Ordering under a size bound; top-k and streaming. |
| 10 | Backtracking | 9 | DFS over choices; uses recursion from Trees. |
| 11 | Graphs | 13 | BFS/DFS, topological sort, union-find. |
| 12 | Advanced Graphs | 6 | Weighted shortest paths, MST, Eulerian paths. |
| 13 | 1-D Dynamic Programming | 12 | State over a single index. |
| 14 | 2-D Dynamic Programming | 11 | State over two indices. |
| 15 | Greedy | 8 | Local choice plus an exchange argument. |
| 16 | Intervals | 6 | Sorting by endpoint, then sweeping. |
| 17 | Math & Geometry | 8 | Matrix manipulation and number tricks. |
| 18 | Bit Manipulation | 7 | Bitwise identities; a compact finish. |

The full problem list, with tick-boxes, is in [`checklist.md`](checklist.md).

### Weekly cadence (10 weeks)

| Weeks | Focus | Target |
|---|---|---|
| 1–2 | Arrays & Hashing, Two Pointers, Sliding Window, Stack | ~27 problems |
| 3–4 | Binary Search, Linked List, Trees | ~33 problems |
| 5–6 | Tries, Heap, Backtracking, Graphs | ~32 problems |
| 7–8 | Advanced Graphs, 1-D DP, 2-D DP | ~29 problems |
| 9–10 | Greedy, Intervals, Math & Geometry, Bit Manipulation + re-solve the weakest 25 | ~29 new, ~25 re-solves |

Adjust the pace to your data. If you cannot solve a fresh problem unaided, spend more time on the category rather than advancing.

---

## Phase 2 — 30 Patterns

After the 150, run the same material again through the *pattern* lens. This phase is where recognition becomes reflex: each pattern gets one page naming the signals, the invariant, the template, and the failure modes.

| # | Pattern | # | Pattern | # | Pattern |
|---|---|---|---|---|---|
| 1 | Arrays & Hashing | 11 | Monotonic Deque | 21 | Graph Shortest Path (Dijkstra) |
| 2 | Two Pointers | 12 | Top K Elements (Heap) | 22 | Dynamic Programming — 1D |
| 3 | Sliding Window | 13 | K-way Merge | 23 | Dynamic Programming — 2D |
| 4 | Fast & Slow Pointers | 14 | BFS | 24 | DP — Knapsack |
| 5 | Binary Search | 15 | DFS + Backtracking | 25 | DP — Subsequences |
| 6 | Binary Search on the Answer | 16 | Tree Traversals | 26 | DP — Intervals |
| 7 | Merge Intervals | 17 | Binary Search Tree | 27 | DP on Trees |
| 8 | Cyclic Sort | 18 | Trie | 28 | Bit Manipulation |
| 9 | Linked List In-Place Reversal | 19 | Union-Find | 29 | Math & Number Theory |
| 10 | Monotonic Stack | 20 | Topological Sort | 30 | Greedy |

Tick-boxes are in [`checklist.md`](checklist.md). Explanations live in [`patterns/`](patterns/).

---

## Rules

**Solve, do not read.** A problem is done when you have written the solution from a blank editor and it passes. Reading a solution and thinking "yes, that makes sense" does not count.

**Re-solve, do not re-read.** When you revisit, close the solution and reproduce it. If you need to look, the problem goes back in the queue.

**Log the failure, not just the result.** After a failed attempt, note which of these it was — each has a different fix:

| Error class | Fix |
|---|---|
| Conceptual misunderstanding | Re-study the mental model and one worked example |
| Pattern misidentification | More mixed practice; re-read the recognition signals |
| Broken invariant | Re-derive the correctness argument, then re-code |
| Implementation error | Hand-trace on a tiny input |
| Edge-case failure | Build an edge-case checklist for the pattern |
| Complexity misjudged | Re-derive the cost from the loop structure |

**Mastery test.** Mark a pattern complete only when you can, without notes: solve a fresh problem; explain why it works; state the time and space cost; solve an unfamiliar variation; and repeat all four after a week.

**Order matters more than volume.** Finishing one category properly beats half-finishing three.

---

## Notes

- The problem list here follows the NeetCode 150 grouping supplied for this plan: 18 categories, 150 problems.
- The 30-pattern phase is a re-framing of the same material, not a second curriculum. Most of its problems are re-solves of Phase 1 problems, deliberately.
- If time is short, filter Phase 1 to easy and medium (125 problems); every pattern is still covered. Add the hards only if your target companies ask them.
