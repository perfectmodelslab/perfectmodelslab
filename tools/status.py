"""rewrites the status line between the markers in README.md.

runs from a GitHub Action on a schedule; the line is the only moving
part of the profile, and this script is the reason it moves. the
workflow amends the commit instead of appending, so the profile keeps
its single commit by design.
"""
import datetime
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = "https://api.github.com/repos/perfectmodelslab/ComfyUI-PerfectLab/releases/latest"


def latest_ship():
    req = urllib.request.Request(API, headers={"User-Agent": "perfectlab-profile"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["tag_name"].strip()


def main():
    line = (f"in development · latest public ship: perfectlab {latest_ship()} · "
            f"rewritten {datetime.date.today().isoformat()}")
    md = (ROOT / "README.md").read_text(encoding="utf-8")
    new, n = re.subn(
        r"(<!-- status:begin -->\n).*?(\n<!-- status:end -->)",
        lambda m: m.group(1) + line + m.group(2),
        md, flags=re.S)
    if n != 1:
        raise SystemExit("status markers not found exactly once")
    if new != md:
        (ROOT / "README.md").write_text(new, encoding="utf-8")
        print("status line rewritten:", line)
    else:
        print("status line already current:", line)


if __name__ == "__main__":
    main()
