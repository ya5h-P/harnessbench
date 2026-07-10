def running_medians(nums):
    """List of running medians: element i is the median of nums[0..i]. For an even count the median is the average of the two middle values (a float)."""
    import heapq
    lo, hi = [], []  # lo: max-heap (neg), hi: min-heap
    out = []
    for x in nums:
        if lo and x <= -lo[0]:
            heapq.heappush(lo, -x)
        else:
            heapq.heappush(hi, x)
        if len(lo) > len(hi) + 1:
            heapq.heappush(hi, -heapq.heappop(lo))
        elif len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        if len(lo) == len(hi):
            out.append((-lo[0] + hi[0]) / 2.0)
        else:
            out.append(float(-lo[0]))
    return out
