def build_command(tool, filename):
    """Build the command to run `tool` on `filename` for a subprocess call."""
    # BUG: returns a shell STRING; when passed to subprocess(..., shell=True) a filename
    # like "a.png; rm -rf ." injects extra commands. It also splits multi-word names.
    return "%s %s" % (tool, filename)
