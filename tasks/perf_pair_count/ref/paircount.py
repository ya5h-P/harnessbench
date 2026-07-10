def count_pairs(nums, target):
    """Number of index pairs i<j with nums[i]+nums[j]==target."""
    from collections import Counter
    seen = Counter()
    total = 0
    for x in nums:
        total += seen[target - x]
        seen[x] += 1
    return total
