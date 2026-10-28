# Pattern 1 — Arrays & Hashing

**NeetCode 150 category:** 1 of 18 · **Problems:** 9 · **Prerequisites:** none — start here.

---

## The core idea

Most array problems that look like they need two nested loops can be done in one pass if you *remember what you have already seen*. A hash map or hash set gives you that memory with average O(1) insert and lookup, so a search that would have cost O(n) per element collapses to O(1), and an O(n²) scan becomes O(n).

There are really only two moves:

1. **Remember values** — a set for "have I seen this?", a map for "what was the index/count of this?".
2. **Remember derived keys** — a map keyed by something computed from the element (a sorted string, a character-count tuple, a prefix product, a grid coordinate).

Everything in this category is one of those two.

---

## Recognition signals

Reach for a hash map or set when the prompt says or implies:

- "duplicate", "unique", "distinct"
- "frequency", "count", "most common", "top k"
- "pair that sums to", "two numbers that…", "complement"
- "group", "anagram", "same letters"
- "have I seen this before?", "first repeated", "contains"
- a nested loop over the same array is the obvious brute force

If the array is sorted, consider two pointers first — it is cheaper on memory. If the values are bounded small integers, an array as a lookup table can beat a dict on constants.

---

## Mental model

Think of a **notebook**. You walk the array once. At each element you:

- **write** what you just saw (value → index, or value → count), then
- **ask** the notebook a question about the past ("have I already seen `target - x`?").

The answer is available in O(1), so the walk is O(n). The notebook costs O(n) memory — that is the trade you are making: time for space.

```
x = 3, target = 9
notebook: { 2: 0, 7: 1 }          # value -> index
need = target - x = 6
lookup(6) -> miss                 # keep walking
notebook[3] = 2                   # write this element down
```

---

## Python toolkit

| Tool | Use it for | Notes |
|---|---|---|
| `set()` | membership, dedupe | `x in s` is O(1) average |
| `dict` | value → index, value → count | preserves insertion order (3.7+) |
| `collections.Counter` | counting | `most_common(k)` is a heap sort; O(n log k) |
| `collections.defaultdict(list)` | grouping | avoids `if key not in d` |
| `tuple` keys | composite keys | lists are unhashable; convert with `tuple(...)` |

**Why O(1)?** A dict hashes the key and jumps to a bucket. Average O(1); worst case O(n) if every key collides, which Python's hash randomisation makes impractical to trigger with normal data. Say "average O(1)" in an interview — it is the honest phrasing.

**Gotchas:** only hashable keys (no `list`, no `set`, no `dict` as a key); `float('nan')` never equals itself; mutating a dict while iterating over it raises.

---

## The templates

### 1. Seen set — duplicate detection

```python
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

`len(set(nums)) < len(nums)` is the one-liner, but the loop version shows the pattern and short-circuits.

### 2. Frequency map — counting

```python
from collections import Counter

def top_k_frequent(nums, k):
    counts = Counter(nums)                 # value -> count
    return [v for v, _ in counts.most_common(k)]
```

`most_common(k)` without an argument sorts everything (O(n log n)); with `k` it uses a heap (O(n log k)). If the problem demands better than O(n log n), bucket by frequency instead: counts are bounded by `len(nums)`.

### 3. Complement lookup — the pair problem

```python
def two_sum(nums, target):
    index_of = {}                          # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in index_of:
            return [index_of[need], i]
        index_of[x] = i
    return []
```

The order matters: **check, then write**. Writing first would let an element pair with itself.

### 4. Group by a computed key

```python
def group_anagrams(strs):
    groups = {}
    for s in strs:
        key = tuple(sorted(s))             # anagrams share this key
        groups.setdefault(key, []).append(s)
    return list(groups.values())
```

Sorting each string is O(m log m) per word. For long strings, key on a 26-length count tuple instead — O(m) per word:

```python
key = [0] * 26
for ch in s:
    key[ord(ch) - ord('a')] += 1
key = tuple(key)
```

### 5. Set plus expansion — consecutive runs

```python
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:
            continue                       # not the start of a run
        length = 1
        while x + length in s:
            length += 1
        best = max(best, length)
    return best
```

The `if x - 1 in s: continue` is what makes it O(n): each run is walked exactly once, from its start only.

### 6. Prefix and suffix products — no division

```python
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    prefix = 1
    for i in range(n):
        out[i] = prefix                     # product of everything left of i
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix                    # times everything right of i
        suffix *= nums[i]
    return out
```

The tempting version divides the total by each element — it breaks on zeros and is disallowed. This is a hashing-adjacent idea: instead of remembering, precompute.

### 7. Composite keys — grids

```python
def is_valid_sudoku(board):
    rows, cols, boxes = set(), set(), set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == '.':
                continue
            box = (r // 3, c // 3)
            if (r, v) in rows or (c, v) in cols or (box, v) in boxes:
                return False
            rows.add((r, v)); cols.add((c, v)); boxes.add((box, v))
    return True
```

The trick is encoding *which constraint* into the key: `(row, value)`, `(col, value)`, `(box, value)`.

---

## Worked example — Two Sum (LeetCode 1)

**Problem.** Given `nums` and `target`, return the indices of the two numbers that add to `target`. Exactly one solution exists; you may not use the same element twice.

**Brute force.** Try every pair: O(n²) time, O(1) space. The waste is that for each `x` you re-scan the array looking for `target - x`.

**The fix.** Ask instead: "have I already seen `target - x`?" Keep a map from value to the index where you saw it. One pass, one lookup per element.

**Trace.** `nums = [2, 7, 11, 15], target = 9`

| i | x | need = 9 - x | map before | found? |
|---|---|---|---|---|
| 0 | 2 | 7 | `{}` | no → store `2:0` |
| 1 | 7 | 2 | `{2:0}` | yes → return `[0, 1]` |

**Code.** See template 3 above.

**Why it is correct.** At index `i` the map holds every earlier value with its index. If `target - nums[i]` is in the map, the two indices are distinct (`j < i`) and their values sum to `target`, so a valid pair is returned. The problem guarantees exactly one, so the first hit is the answer.

**Complexity.** O(n) time — one pass, O(1) per element on average. O(n) space for the map.

**Pitfalls.**
- Writing to the map before checking, which lets an element match itself (`target = 2x`).
- Returning values instead of indices (this problem wants indices).
- Assuming the array is sorted — it is not; the map removes that need.

---

## The nine problems

Work these in order. The hint column is the one idea that unlocks the problem; do not read it before trying.

| # | Problem | Difficulty | Key idea |
|---|---|---|---|
| 1 | Contains Duplicate | Easy | Set membership in one pass. |
| 2 | Valid Anagram | Easy | Compare frequency maps (or `Counter` equality). |
| 3 | Two Sum | Easy | Complement lookup in a value → index map. |
| 4 | Group Anagrams | Medium | Key each word by its sorted tuple or count tuple. |
| 5 | Top K Frequent Elements | Medium | Count, then heap of size k — or bucket by frequency. |
| 6 | Product of Array Except Self | Medium | Prefix sweep, then suffix sweep; no division. |
| 7 | Valid Sudoku | Medium | Three key sets: `(row, v)`, `(col, v)`, `(box, v)`. |
| 8 | Longest Consecutive Sequence | Medium | Set, and only expand from run starts. |
| 9 | Encode and Decode Strings | Medium | Length-prefix each string so delimiters cannot collide. |

### Notes worth having in your head

- **Valid Anagram** — sorting both is O(n log n); counting is O(n). Say which you are doing.
- **Top K Frequent** — `Counter.most_common(k)` is fine; mention the bucket alternative when the interviewer asks for better than O(n log n).
- **Longest Consecutive** — the O(n) bound only holds because of the `x - 1 in s` guard. Without it the inner `while` can run O(n) times per element.
- **Encode and Decode Strings** — the naive `','.join` breaks when strings contain commas. Prefix each with its length: `"5,hello"`. This is a *design* question, not a hashing one — the hashing idea is that you need an unambiguous key.

---

## Common pitfalls

- **Using a list for membership.** `if x in my_list` is O(n); that is the bug the pattern exists to remove.
- **Check-then-write vs write-then-check.** Order decides whether an element can match itself.
- **Forgetting hashable keys.** `key = sorted(s)` is a list — wrap it: `tuple(sorted(s))`.
- **Claiming O(1) worst case.** Say "average O(1)"; collisions make the worst case O(n).
- **Reaching for a hash map when the array is sorted.** Two pointers gives O(1) space.
- **Mutating a dict during iteration** — collect keys first or iterate over `list(d)`.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Nested loops (the thing to avoid) | O(n²) | O(1) |
| One pass with a set or map | O(n) average | O(n) |
| Sort, then scan | O(n log n) | O(1)–O(n) |
| Bucket by frequency (Top K) | O(n) | O(n) |

---

## After this pattern

Move to **Two Pointers** (category 2). The connection is direct: hashing buys you O(n) time with O(n) memory; two pointers buys O(n) time with O(1) memory, but only when the array is sorted or can be sorted.

Next pattern note: `patterns/02_two_pointers/` (not written yet).
