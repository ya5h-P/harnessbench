import os, sys
w = sys.argv[1]
open(os.path.join(w, 'report.py'), 'w', encoding='utf-8').write('GREETING = "Hello {name}, you have {count} messages."\n\n\ndef generate(name, count):\n    """Render the greeting for a user (now using the stdlib str.format)."""\n    return GREETING.format(name=name, count=count)\n')
open(os.path.join(w, 'migration_notes.md'), 'w', encoding='utf-8').write('# Migration notes\n\nRemoved the vendored `tinytemplate` module and replaced its `render()` with the standard\nlibrary. `report.generate()` now uses `str.format` on the `{name}`/`{count}` placeholders,\nproducing byte-identical output. `tinytemplate.py` has been deleted and is no longer imported.\n')
os.remove(os.path.join(w, 'tinytemplate.py'))
