def count_subarrays(nums, target):
    """Number of contiguous non-empty subarrays whose sum == target."""
    from collections import Counter
    seen = Counter({0: 1})
    pre = 0; total = 0
    for x in nums:
        pre += x
        total += seen[pre - target]
        seen[pre] += 1
    return total
