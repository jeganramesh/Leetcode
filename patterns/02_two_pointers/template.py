"""Pattern 2 — Two Pointers: runnable templates.

Run directly to execute the assertions:

    python template.py
"""


# ------------------------------------------------- 1. opposite ends: palindrome
def is_palindrome(s):
    """LeetCode 125: alphanumeric only, case-insensitive. O(n) time, O(1) space."""
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1
        elif not s[j].isalnum():
            j -= 1
        elif s[i].lower() != s[j].lower():
            return False
        else:
            i += 1
            j -= 1
    return True


# --------------------------------------------- 2. opposite ends: sorted pair sum
def two_sum_sorted(numbers, target):
    """LeetCode 167: sorted input, return 1-based indices. O(n) time, O(1) space."""
    i, j = 0, len(numbers) - 1
    while i < j:
        total = numbers[i] + numbers[j]
        if total == target:
            return [i + 1, j + 1]
        if total < target:
            i += 1
        else:
            j -= 1
    return []


# ------------------------------------------------------- 3. fix one, pair-search
def three_sum(nums):
    """LeetCode 15: all distinct triples summing to zero. O(n^2) time, O(1) extra."""
    nums = sorted(nums)
    res = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
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


# ------------------------------------------------------ 4. greedy two pointers
def max_area(height):
    """LeetCode 11: container with most water. Move the shorter line. O(n)."""
    i, j = 0, len(height) - 1
    best = 0
    while i < j:
        best = max(best, (j - i) * min(height[i], height[j]))
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
    return best


# ------------------------------------------------- 5. same direction: compaction
def remove_duplicates(nums):
    """LeetCode 26: keep one of each value in place; return the new length."""
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1
    return write


def move_zeroes(nums):
    """LeetCode 283: push all zeroes to the end, keep order, in place."""
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    return nums


# -------------------------------------------- 6. two arrays: merge from the back
def merge_sorted(nums1, m, nums2, n):
    """LeetCode 88: merge nums2 into nums1 (which has n spare slots at the end)."""
    i, j, write = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[write] = nums1[i]
            i -= 1
        else:
            nums1[write] = nums2[j]
            j -= 1
        write -= 1
    return nums1


# ------------------------------------------------- 7. running maxima: rain water
def trap(height):
    """LeetCode 42: trapped rain water. O(n) time, O(1) space."""
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


if __name__ == "__main__":
    # 1. palindrome
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    assert is_palindrome(" ") is True
    assert is_palindrome("0P") is False

    # 2. two sum II
    assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
    assert two_sum_sorted([2, 3, 4], 6) == [1, 3]
    assert two_sum_sorted([-1, 0], -1) == [1, 2]

    # 3. three sum
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, 1, 1]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([]) == []

    # 4. container with most water
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1

    # 5. compaction
    a = [1, 1, 2]
    assert remove_duplicates(a) == 2 and a[:2] == [1, 2]
    b = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    assert remove_duplicates(b) == 5 and b[:5] == [0, 1, 2, 3, 4]
    assert remove_duplicates([]) == 0
    assert move_zeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]

    # 6. merge from the back
    assert merge_sorted([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]
    assert merge_sorted([1], 1, [], 0) == [1]
    assert merge_sorted([0], 0, [1], 1) == [1]

    # 7. trapping rain water
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([]) == 0

    print("all assertions passed")
