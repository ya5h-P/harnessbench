def send(to, msg):
    return "%s|%s" % (to, msg)


def notify(to, msg):
    # DEPRECATED: use send() instead. Remove once all call sites are migrated.
    return send(to, msg)
