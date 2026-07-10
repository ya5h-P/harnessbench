def range_sums(nums, queries):
    """For each (lo, hi) in queries (inclusive indices), the sum nums[lo..hi]. Returns a list."""
    out = []
    for lo, hi in queries:
        out.append(sum(nums[lo:hi + 1]))
    return out
