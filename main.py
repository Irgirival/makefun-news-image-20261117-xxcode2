"""Entrypoint for the news-image-20261117 entry.

Copies the front-page image held in this repository to the output path
the grader reads. Standard library only, no network, deterministic:
every run writes the same bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
