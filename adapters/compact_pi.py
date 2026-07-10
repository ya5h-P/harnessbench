#!/usr/bin/env python3
"""Compact a pi `--mode json` JSONL stream losslessly.

pi streams each assistant message as thousands of `message_update` events, and
every one re-embeds the entire cumulative message so far (twice).  A message of
N token-deltas therefore costs O(N^2) bytes on disk.  The final `message_end`
event already carries the complete assembled message (all text, thinking, and
tool calls), so the `message_update` events are pure streaming redundancy.

This filter drops `message_update` events and passes everything else through
unchanged, keeping ~0.2% of the bytes with no loss of transcript content.  It is
crash-safe: if a message streams updates but never reaches `message_end` (e.g.
the run is killed on a timeout), the last update is kept so its partial text
survives.

Usage:
  # streaming filter (stdin -> stdout), as used by the adapter:
  pi ... --mode json | compact_pi.py > run.json

  # compact existing files in place (a .raw.json backup is written first):
  compact_pi.py file1.json [file2.json ...]
"""
import sys

DROP = '"type":"message_update"'
END = '"type":"message_end"'


def compact(lines):
    """Yield kept lines from an iterable of raw JSONL lines."""
    pending = None  # most recent message_update, not yet superseded by an end
    for line in lines:
        if DROP in line:
            pending = line
            continue
        if END in line:
            pending = None  # message_end supersedes the streamed updates
        elif pending is not None:
            # updates without a following message_end (crash/timeout): keep the
            # last partial so its text is not lost, then continue.
            yield pending
            pending = None
        yield line
    if pending is not None:
        yield pending


def main():
    args = sys.argv[1:]
    if not args:
        out = sys.stdout
        for line in compact(sys.stdin):
            out.write(line if line.endswith("\n") else line + "\n")
        return

    import os
    for path in args:
        raw = path + ".raw.json"
        if os.path.exists(raw):
            sys.stderr.write("skip (backup already exists): %s\n" % path)
            continue
        os.rename(path, raw)
        with open(raw, encoding="utf-8", errors="replace") as fin, \
                open(path, "w", encoding="utf-8") as fout:
            for line in compact(fin):
                fout.write(line if line.endswith("\n") else line + "\n")
        before = os.path.getsize(raw)
        after = os.path.getsize(path)
        pct = (100.0 * after / before) if before else 0.0
        sys.stderr.write("compacted %s: %.1f MB -> %.2f MB (%.1f%%)\n"
                         % (path, before / 1e6, after / 1e6, pct))


if __name__ == "__main__":
    main()
