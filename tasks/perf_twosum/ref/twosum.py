def has_pair(nums, target):
    """True iff two DISTINCT indices i!=j have nums[i]+nums[j]==target."""
    seen = set()
    for x in nums:
        if target - x in seen:
            return True
        seen.add(x)
    return False
