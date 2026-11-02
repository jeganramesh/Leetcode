# Pattern 2 — Two Pointers

**NeetCode 150 category:** 2 of 18 · **Problems:** 5 · **Prerequisite:** [1. Arrays & Hashing](../01_arrays_and_hashing/README.md)

---

## The core idea

Keep two indices into the same sequence and move them under a rule, so that every element is looked at a constant number of times. A nested-loop search becomes a single pass.

There are two shapes, and confusing them is the most common mistake:

1. **Opposite ends, moving inward.** One pointer at each end. At each step you discard the element that provably cannot be part of the answer. This needs the data to be **sorted** — or to have a monotone property that makes discarding safe.
2. **Same direction, fast and slow.** One pointer reads, one writes. Used for **in-place compaction**: removing duplicates, moving zeroes, partitioning. The writer only advances when the reader finds a keeper.

(A third shape, fast/slow cycle detection, gets its own note later — pattern 4.)

---

## Recognition signals

- "sorted array", or the input can be sorted without losing what the answer needs
- "pair", "triplet", "two numbers that sum to…"
- "palindrome", "reverse in place"
- "remove duplicates / elements in place", "move zeroes to the end", O(1) extra space
- "maximum area / water between two lines"
- the obvious brute force is two nested loops over the same array

**If the array is not sorted and cannot be sorted, this pattern is usually wrong.** Hashing (pattern 1) buys O(n) time with O(n) memory; two pointers buys O(n) time with O(1) memory but needs order.

---

## Mental model

A corridor with a person standing at each end. Between them is the set of candidate answers. Each step, one person walks one pace inward — and in doing so, a whole block of candidates is thrown away.

```
[ a0  a1  a2  a3  a4  a5 ]
  L                    R     sum too small -> L++  (a0 cannot pair with anything)
      L                R     sum too large -> R--  (a5 cannot pair with anything)
```

The proof obligation is always the same sentence: *why is it safe to discard that element?* If you cannot answer it, the pattern does not apply.

---

## Templates

### 1. Opposite ends — palindrome check

```python
def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True
```

### 2. Opposite ends — pair sum in a sorted array

```python
def two_sum_sorted(numbers, target):
    i, j = 0, len(numbers) - 1
    while i < j:
        total = numbers[i] + numbers[j]
        if total == target:
            return [i + 1, j + 1]      # 1-based, as LeetCode 167 asks
        if total < target:
            i += 1                     # too small: the left value is too small
        else:
            j -= 1                     # too large: the right value is too big
    return []
```

The discard argument: in a sorted array, if `a[i] + a[j] < target`, then `a[i]` is too small to pair with **anything** at or left of `j`, so `i` can move on.

### 3. Fix one element, then pair-search — 3Sum

```python
def three_sum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break                              # sorted: no three positives sum to 0
        if i > 0 and nums[i] == nums[i - 1]:
            continue                           # skip duplicate first elements
        l, r = i + 1, len(nums) - 1
        while l < r:
            total = nums[i] + nums[l] + nums[r]
            if total == 0:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
            elif total < 0:
                l += 1
            else:
                r -= 1
    return res
```

### 4. Greedy two pointers — container with most water

```python
def max_area(height):
    i, j = 0, len(height) - 1
    best = 0
    while i < j:
        best = max(best, (j - i) * min(height[i], height[j]))
        if height[i] < height[j]:
            i += 1          # the shorter line caps the area; move it
        else:
            j -= 1
    return best
```

The move rule is the whole insight: the area is limited by the shorter line, so keeping it can never help — width only shrinks from here.

### 5. Same direction — in-place compaction

```python
def remove_duplicates(nums):
    """LeetCode 26: keep one copy of each value, return the new length."""
    if not nums:
        return 0
    write = 1                       # nums[0] is always kept
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

The reader inspects everything; the writer only advances on a keeper. Everything past `write` is garbage.

### 6. Two pointers over two arrays — merge from the back

```python
def merge_sorted(nums1, m, nums2, n):
    """LeetCode 88: merge into nums1, which has room at the end."""
    i, j, write = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[write] = nums1[i]
            i -= 1
        else:
            nums1[write] = nums2[j]
            j -= 1
        write -= 1
```

Writing from the back avoids overwriting elements of `nums1` you have not read yet.

### 7. Two pointers with running maxima — trapping rain water

```python
def trap(height):
    if not height:
        return 0
    l, r = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while l < r:
        if height[l] < height[r]:
            left_max = max(left_max, height[l])
            water += left_max - height[l]
            l += 1
        else:
            right_max = max(right_max, height[r])
            water += right_max - height[r]
            r -= 1
    return water
```

The invariant: the lower side's maximum is the true bound for that column, because the other side is at least as tall.

---

## Worked example — 3Sum (LeetCode 15)

**Problem.** Return every **distinct** triple of values that sums to zero. Positions may not repeat; the same triple in a different order is not distinct.

**Brute force.** Three nested loops: O(n³), and it produces duplicates unless you dedupe the output afterwards.

**The fix.** Sort once — O(n log n). Then fix the first element with an outer loop and reduce the rest to a *sorted pair-sum*, which two pointers solve in one linear pass. Total O(n²).

**Trace.** `nums = [-1, 0, 1, 2, -1, -4]` → sorted `[-4, -1, -1, 0, 1, 2]`

| i | nums[i] | need pair summing to | pointers | found |
|---|---|---|---|---|
| 0 | -4 | 4 | (-1, 2) → 1, (0, 2) → 2, (1, 2) → 3 | — |
| 1 | -1 | 1 | (-1, 2) → 1 | `[-1, -1, 2]` |
| 1 | -1 | 1 | (0, 1) → 1 | `[-1, 0, 1]` |
| 2 | -1 | — | skipped: equals nums[1] | — |
| 3 | 0 | 0 | (1, 2) → 3 | — |

Result: `[[-1, -1, 2], [-1, 0, 1]]`.

**Why it is correct.** After sorting, for a fixed `i` the pair that completes the triple must come from the suffix `nums[i+1:]`, which is sorted. The pair-sum discard argument applies, so the two pointers never skip a valid pair. Duplicates are eliminated at the source — by skipping equal `nums[i]` before the inner loop, and equal `nums[l]` / `nums[r]` after recording — so no distinct triple is lost and none is repeated.

**Complexity.** O(n²) time (the sort is dominated), O(1) extra space beyond the output.

**Pitfalls in this exact problem.**
- Skipping duplicates only at `i`, not at `l` and `r` — you then emit the same triple several times.
- Using `nums[i] + nums[i]` instead of `nums[i] + nums[l] + nums[r]` (a real bug when transcribing).
- Forgetting `break` when `nums[i] > 0`: correct but slower.
- Deduping the output with a `set` instead of at the source: works, but hides the reasoning and is slower.

---

## The five problems

| # | Problem | Difficulty | Key idea |
|---|---|---|---|
| 1 | Valid Palindrome | Easy | Pointers at both ends; skip non-alphanumerics; compare lowercased. |
| 2 | Two Sum II | Medium | Sorted input → pair sum with two pointers; return 1-based indices. |
| 3 | 3Sum | Medium | Sort, fix one element, two-pointer the suffix, skip duplicates at all three positions. |
| 4 | Container With Most Water | Medium | Area = width × shorter line; always move the shorter pointer. |
| 5 | Trapping Rain Water | Hard | Two pointers with running left/right maxima; the lower side is the true bound. |

### Notes worth having in your head

- **Valid Palindrome** — `s[i].isalnum()` and `s[i].lower()` keep it one pass with O(1) space. Building a cleaned copy first is O(n) space and usually accepted, but say which you are doing.
- **Two Sum II** — the input is guaranteed sorted, so the O(1)-space solution is expected. Using a hash map works but ignores the given order.
- **Container With Most Water** — the greedy move is provable: if `height[i] < height[j]`, then for every `k < j` the area with `i` is capped by `height[i]`, and narrower, so `i` can be discarded.
- **Trapping Rain Water** — the stack solution also exists (monotonic stack, pattern 10). Two pointers is O(1) space and is the one to reach for.

---

## Common pitfalls

- **Running two pointers on unsorted data.** Without order there is no discard argument, and the answer is silently wrong.
- **Moving both pointers on a match** when the problem wants all pairs — you skip valid combinations.
- **Forgetting the duplicate skips** in N-sum problems; the output then has repeats.
- **Using `<` where `<=` is needed** at the boundaries, so the loop exits one step early or loops forever.
- **Same-direction confusion.** In compaction the writer must lag the reader; advancing both together overwrites unread data.
- **Merging from the front** into an array with spare room at the end — you clobber unread elements.

---

## Complexity summary

| Shape | Time | Extra space |
|---|---|---|
| Opposite ends, sorted pair sum | O(n) | O(1) |
| N-sum (sort + fix + pair search) | O(n^(N-1)) | O(1) |
| Same direction, in-place compaction | O(n) | O(1) |
| Merge two sorted arrays | O(m + n) | O(1) |
| Hashing alternative (pattern 1) | O(n) | O(n) |

---

## After this pattern

Next is **Sliding Window** (category 3): the same two-index machinery, but both pointers move forward and the window must stay contiguous. The link to remember — two pointers discards from the *ends*, a sliding window discards from the *left edge of a run*.

Next pattern note: `patterns/03_sliding_window/` (not written yet).
