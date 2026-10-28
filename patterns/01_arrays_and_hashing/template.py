"""Pattern 1 — Arrays & Hashing: runnable templates.

Each function is a self-contained template for one shape of the pattern.
Run this file directly to execute the assertions at the bottom:

    python template.py
"""

from collections import Counter


# ---------------------------------------------------------------- 1. seen set
def contains_duplicate(nums):
    """True if any value appears more than once. O(n) time, O(n) space."""
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


# ------------------------------------------------------- 2. frequency counting
def is_anagram(s, t):
    """True if t is an anagram of s. O(n) time, O(1) space (26 letters)."""
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)


def top_k_frequent(nums, k):
    """The k most frequent values. O(n log k) time with most_common(k)."""
    return [value for value, _ in Counter(nums).most_common(k)]


# --------------------------------------------------------- 3. complement lookup
def two_sum(nums, target):
    """Indices of the two values summing to target. Check BEFORE writing."""
    index_of = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in index_of:
            return [index_of[need], i]
        index_of[x] = i
    return []


# ------------------------------------------------------- 4. group by a key
def group_anagrams(strs):
    """Group words that are anagrams. Key = sorted tuple, or a count tuple."""
    groups = {}
    for s in strs:
        key = tuple(sorted(s))
        groups.setdefault(key, []).append(s)
    return list(groups.values())


def group_anagrams_count_key(strs):
    """Same, but O(m) per word instead of O(m log m)."""
    groups = {}
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord("a")] += 1
        groups.setdefault(tuple(counts), []).append(s)
    return list(groups.values())


# ------------------------------------------------- 5. prefix / suffix products
def product_except_self(nums):
    """out[i] = product of all other elements. No division, handles zeros."""
    n = len(nums)
    out = [1] * n

    prefix = 1
    for i in range(n):
        out[i] = prefix          # everything to the left of i
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix         # times everything to the right of i
        suffix *= nums[i]

    return out


# ----------------------------------------------------------- 6. composite keys
def is_valid_sudoku(board):
    """Validate a 9x9 Sudoku board. Key each constraint as a tuple."""
    rows, cols, boxes = set(), set(), set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == ".":
                continue
            box = (r // 3, c // 3)
            if (r, v) in rows or (c, v) in cols or (box, v) in boxes:
                return False
            rows.add((r, v))
            cols.add((c, v))
            boxes.add((box, v))
    return True


# ------------------------------------------------- 7. set plus run expansion
def longest_consecutive(nums):
    """Length of the longest run of consecutive integers. O(n) time."""
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:
            continue                 # only start counting from a run start
        length = 1
        while x + length in values:
            length += 1
        best = max(best, length)
    return best


# ----------------------------------------------------- 8. length-prefix codec
def encode(strs):
    """Encode a list of strings as one string. '5,hello' style."""
    return "".join(f"{len(s)},{s}" for s in strs)


def decode(s):
    """Inverse of encode."""
    out = []
    i = 0
    while i < len(s):
        j = i
        while s[j] != ",":
            j += 1
        length = int(s[i:j])
        start = j + 1
        out.append(s[start:start + length])
        i = start + length
    return out


if __name__ == "__main__":
    assert contains_duplicate([1, 2, 3, 1]) is True
    assert contains_duplicate([1, 2, 3, 4]) is False

    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False

    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]

    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 3], 6) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]

    grouped = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert sorted(sorted(g) for g in grouped) == sorted(
        sorted(g) for g in [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    )
    assert sorted(sorted(g) for g in group_anagrams_count_key(
        ["eat", "tea", "tan", "ate", "nat", "bat"])) == sorted(
        sorted(g) for g in [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    )

    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert is_valid_sudoku(board) is True

    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0

    words = ["hello", "world", "a,b", ""]
    assert decode(encode(words)) == words

    print("all assertions passed")
