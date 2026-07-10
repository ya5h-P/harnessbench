def count_pairs(nums, target):
    """Number of index pairs i<j with nums[i]+nums[j]==target."""
    n = len(nums)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                total += 1
    return total
