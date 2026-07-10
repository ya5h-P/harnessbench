def has_dup_within(nums, k):
    """True iff some value appears at two indices i<j with j-i<=k."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, min(i + k + 1, n)):
            if nums[i] == nums[j]:
                return True
    return False
