import tinytemplate

GREETING = "Hello {name}, you have {count} messages."


def generate(name, count):
    """Render the greeting for a user."""
    return tinytemplate.render(GREETING, {"name": name, "count": count})
