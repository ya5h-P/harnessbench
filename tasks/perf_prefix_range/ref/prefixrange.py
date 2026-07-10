def range_sums(nums, queries):
    """For each (lo, hi) in queries (inclusive indices), the sum nums[lo..hi]. Returns a list."""
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    return [pre[hi + 1] - pre[lo] for lo, hi in queries]
