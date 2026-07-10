def has_pair(nums, target):
    """True iff two DISTINCT indices i!=j have nums[i]+nums[j]==target."""
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return True
    return False
