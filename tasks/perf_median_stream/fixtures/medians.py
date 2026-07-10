def running_medians(nums):
    """List of running medians: element i is the median of nums[0..i]. For an even count the median is the average of the two middle values (a float)."""
    out = []
    seen = []
    for x in nums:
        seen.append(x)
        s = sorted(seen)
        m = len(s)
        if m % 2:
            out.append(float(s[m // 2]))
        else:
            out.append((s[m // 2 - 1] + s[m // 2]) / 2.0)
    return out
