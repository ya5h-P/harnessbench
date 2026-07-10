def count_subarrays(nums, target):
    """Number of contiguous non-empty subarrays whose sum == target."""
    n = len(nums)
    total = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == target:
                total += 1
    return total
