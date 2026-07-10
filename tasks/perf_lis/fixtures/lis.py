def lis_length(nums):
    """Length of the longest strictly-increasing subsequence."""
    n = len(nums)
    if n == 0:
        return 0
    best = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    return max(best)
