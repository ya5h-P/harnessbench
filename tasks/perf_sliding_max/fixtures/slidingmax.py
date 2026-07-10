def window_maxes(nums, k):
    """List of the maximum of each contiguous window of size k (len = len(nums)-k+1). Empty list if k>len(nums) or nums is empty."""
    if k <= 0 or k > len(nums):
        return []
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
