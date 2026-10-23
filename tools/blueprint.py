"""draws assets/blueprint.svg: the hero of the profile.

an architectural plan of a platform that stays private. rooms carry
the scale, not the features. walls draw themselves, labels fade in
after them, the status dot keeps blinking. everything is computed
here, nothing is borrowed from anyone's widget farm.
"""
import pathlib

W, H = 1720, 520
BG = "#101018"
GRID = "#1d1d2b"
FRAME = "#2a2a3c"
AMBER = "#F0B64E"
INK = "#c9c6d8"
DIM = "#6f6c82"
FIRE = "#E04462"
MONO = "Consolas, 'Courier New', monospace"

OUT = pathlib.Path(__file__).resolve().parents[1] / "assets" / "blueprint.svg"


def esc(s):
    return s.replace("&", "&").replace("<", "<").replace(">", ">")


def wall(x1, y1, x2, y2, delay):
    length = round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5, 1)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'style="stroke-dasharray:{length};stroke-dashoffset:{length};'
            f'animation:draw .7s ease-out {delay}s forwards"/>')

def label(cx, y, name, fact, delay):
    return (
        f'<text x="{cx}" y="{y}" text-anchor="middle" fill="{AMBER}" '
        f'font-size="21" font-weight="bold" letter-spacing="4" class="lbl" '
        f'style="animation-delay:{delay}s">{esc(name)}</text>\n'
        f'<text x="{cx}" y="{y + 26}" text-anchor="middle" fill="{INK}" '
        f'font-size="16" class="lbl" style="animation-delay:{delay + .25}s">'
        f"{esc(fact)}</text>"
    )


def trow(y, key, value):
    return (
        f'<text x="1242" y="{y}" fill="{DIM}" font-size="13" letter-spacing="2" '
        f'class="lbl" style="animation-delay:1.4s">{esc(key)}</text>\n'
        f'<text x="1346" y="{y}" fill="{AMBER}" font-size="15" font-weight="bold" '
        f'class="lbl" style="animation-delay:1.4s">{esc(value)}</text>'
    )


parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
             f'<title>BuildGuide, a plan of a private build</title>')
parts.append(f"""<style>
  text {{ font-family: {MONO}; }}
  .wall {{ stroke: {AMBER}; stroke-width: 2.2; }}
  .lbl {{ opacity: 0; animation: fade .6s ease forwards; }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes fade {{ to {{ opacity: 1; }} }}
  @keyframes whisper {{ to {{ opacity: .05; }} }}
  @keyframes blink {{ 0%, 100% {{ opacity: .12; }} 50% {{ opacity: 1; }} }}
</style>""")
parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
parts.append(
    '<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">'
    f'<path d="M 40 0 L 0 0 0 40" fill="none" stroke="{GRID}" stroke-width="1"/>'
    '</pattern></defs>'
    f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" fill="url(#g)"/>'
)
parts.append(f'<rect x="20" y="20" width="{W - 40}" height="{H - 40}" rx="14" '
              f'fill="none" stroke="{FRAME}" stroke-width="1.4"/>')

# title line
parts.append(
    f'<text x="120" y="66" fill="{AMBER}" font-size="44" font-weight="bold" '
    f'letter-spacing="12" class="lbl" style="animation-delay:.2s">BUILDGUIDE</text>'
)
parts.append(
    f'<text x="1180" y="62" text-anchor="end" fill="{DIM}" font-size="15" '
    f'letter-spacing="2" class="lbl" style="animation-delay:.4s">'
    f'{esc("multi-role construction platform · sheet 01 · partial disclosure")}</text>'
)

# outer walls of the plan, one continuous path
parts.append(
    '<path d="M 120 100 H 1180 V 430 H 120 Z" fill="none" class="wall" '
    'style="stroke-dasharray:2780;stroke-dashoffset:2780;'
    'animation:draw 1.6s ease-out forwards"/>'
)

# interior walls, doors left as gaps
parts.append('<g class="wall">')
for x1, y1, x2, y2, d in [
    (480, 100, 480, 190, .7), (480, 240, 480, 265, .8),
    (830, 100, 830, 190, .9), (830, 240, 830, 265, 1.0),
    (120, 265, 430, 265, 1.1), (486, 265, 770, 265, 1.2),
    (826, 265, 1180, 265, 1.3),
    (480, 265, 480, 330, 1.4), (480, 380, 480, 430, 1.5),
    (830, 265, 830, 330, 1.6), (830, 380, 830, 430, 1.7),
]:
    parts.append(wall(x1, y1, x2, y2, d))
parts.append('</g>')

# rooms: name + the verified scale
for cx, y, name, fact in [
    (300, 168, "SCHEMA", "240 data models"),
    (655, 168, "API", "454 endpoints"),
    (1005, 168, "I18N", "5 locales · 15 000 keys"),
    (300, 328, "TESTS", "7200+ in the CI gate"),
    (655, 328, "AI", "estimator by photo"),
    (1005, 328, "BILLING", "ledger · idempotent"),
]:
    parts.append(label(cx, y, name, fact, 2.2))

# title block, the way real drawings keep their stamp
parts.append(
    f'<rect x="1210" y="100" width="480" height="330" fill="none" '
    f'stroke="{AMBER}" stroke-width="1.4" class="lbl" '
    f'style="animation-delay:.3s"/>'
)
parts.append(
    f'<line x1="1210" y1="132" x2="1690" y2="132" stroke="{AMBER}" '
    f'stroke-width="1" class="lbl" style="animation-delay:.5s"/>'
)
parts.append(
    f'<text x="1242" y="120" fill="{INK}" font-size="14" font-weight="bold" '
    f'letter-spacing="6" class="lbl" style="animation-delay:.6s">TITLE BLOCK</text>'
)
for i, (key, value) in enumerate([
    ("PROJECT", "BuildGuide"),
    ("FOUNDER", "Igor Vasilyev"),
    ("SURVEY", "11 stages · 111 criteria"),
    ("NORMS", "338 · СП/ГОСТ"),
    ("DOCUMENTS", "133 · self-audited"),
]):
    parts.append(trow(170 + i * 44, key, value))
parts.append(
    f'<text x="1242" y="390" fill="{DIM}" font-size="13" letter-spacing="2" '
    f'class="lbl" style="animation-delay:1.4s">STATUS</text>\n'
    f'<rect x="1346" y="378" width="11" height="11" fill="{FIRE}" '
    f'style="animation:blink 1.3s ease-in-out infinite"/>\n'
    f'<text x="1368" y="390" fill="{INK}" font-size="15" font-weight="bold" '
    f'class="lbl" style="animation-delay:1.4s">in development</text>'
)
parts.append(
    f'<text x="1210" y="462" fill="{DIM}" font-size="13" letter-spacing="2" '
    f'class="lbl" style="animation-delay:1.8s">'
    f'{esc("SCALE 1:240 · DIMENSIONS IN FACTS, NOT IN PIXELS")}</text>'
)

# the watermark nobody is supposed to read, everyone does
parts.append(
    f'<text x="650" y="270" text-anchor="middle" fill="{AMBER}" font-size="84" '
    f'letter-spacing="10" opacity="0" transform="rotate(-7 650 270)" '
    f'style="animation:whisper .8s ease 3s forwards">'
    f'{esc("PARTIAL DISCLOSURE")}</text>'
)

svg = "\n".join(parts) + "\n</svg>\n"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding="utf-8")
print(f"blueprint drawn: {OUT} ({len(svg)} bytes)")
