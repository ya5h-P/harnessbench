def has_dup_within(nums, k):
    """True iff some value appears at two indices i<j with j-i<=k."""
    window = set()
    from collections import deque
    order = deque()
    for x in nums:
        if x in window:
            return True
        window.add(x); order.append(x)
        if len(order) > k:
            window.discard(order.popleft())
    return False
