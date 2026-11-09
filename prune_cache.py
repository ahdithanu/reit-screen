"""Keep the raw cache bounded for daily runs.

Mutable sources (companyfacts, submissions, frames, fred, yahoo): keep the newest 2 copies per key.
Filing documents (archives): keep the oldest and the newest copy, because verify.py compares the
original fetch with the latest re-fetch when it checks that quotes are verbatim.
Never touches manifest.csv. Prints what it removed.
"""
import re
from collections import defaultdict

from common import RAW


def main():
    removed = 0
    for d in sorted(p for p in RAW.iterdir() if p.is_dir()):
        groups = defaultdict(list)
        for f in d.iterdir():
            m = re.match(r"^(.*)__\d{8}T\d{6}Z", f.name)
            if m:
                groups[m.group(1)].append(f)
        for key, files in groups.items():
            files.sort()
            keep = {files[0], files[-1]} if d.name == "archives" else set(files[-2:])
            for f in files:
                if f not in keep:
                    f.unlink()
                    removed += 1
    print(f"prune_cache: removed {removed} old cached copies")


if __name__ == "__main__":
    main()
