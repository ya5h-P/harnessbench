def window_maxes(nums, k):
    """List of the maximum of each contiguous window of size k (len = len(nums)-k+1). Empty list if k>len(nums) or nums is empty."""
    from collections import deque
    if k <= 0 or k > len(nums):
        return []
    dq = deque(); out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
