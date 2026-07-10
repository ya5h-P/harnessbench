"""tinytemplate — a tiny vendored templating helper (to be removed)."""

def render(template, context):
    """Replace each {key} in template with str(context[key])."""
    out = template
    for k, v in context.items():
        out = out.replace("{" + k + "}", str(v))
    return out
