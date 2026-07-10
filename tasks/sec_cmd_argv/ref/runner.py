def build_command(tool, filename):
    """Build the command to run `tool` on `filename` for a subprocess call."""
    # an argv LIST keeps filename as exactly one argument, immune to shell metacharacters
    return [tool, filename]
