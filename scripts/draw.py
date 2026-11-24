"""Draw the profile images (light and dark) with no third-party services.

    python3 scripts/draw.py        # writes assets/hero-{light,dark}.svg and assets/path-{light,dark}.svg

Style follows the thesis diagrams (PHD/phd-tools/figures/phd_figstyle.py, rysunky.md):
players are sharp rectangles, system parts are rounded, data that point to a patient are solid clay,
de-identified data are dashed slate, the author's own contribution is a navy outline on a light fill.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = "Roboto, 'Helvetica Neue', Arial, sans-serif"

THEMES = {
    "light": dict(text="#333333", muted="#606A70", grid="#D0D5DA", frame="#9AA3A9", boundary="#F4F5F7",
                  navy="#2E3192", own="#F1F1FA", clay="#8E5A43", clay_tint="#F3E6DF", slate="#4F6D8A",
                  blue="#0076A8", player="#333333", bg="#FFFFFF"),
    "dark": dict(text="#E6EDF3", muted="#9198A1", grid="#30363D", frame="#6E7681", boundary="#161B22",
                 navy="#A5A8FF", own="#1F2140", clay="#D29A7E", clay_tint="#3A2A22", slate="#8FB3D9",
                 blue="#58B6E0", player="#C9D1D9", bg="#0D1117"),
}

T = 12.0  # length of the hero loop, seconds


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=15, fill="#333", weight="normal", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def frac(t):
    return round(t / T, 4)


def visible(t0, t1):
    """opacity animation: shown only between t0 and t1 seconds of the loop"""
    a, b = frac(t0), frac(t1)
    return (f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'values="0;1;0" keyTimes="0;{a};{b}"/>')


def dot(path, t0, t1, color, r=6):
    a, b = frac(t0), frac(t1)
    return (f'<circle r="{r}" fill="{color}" opacity="0">{visible(t0, t1)}'
            f'<animateMotion dur="{T}s" repeatCount="indefinite" path="{path}" calcMode="linear" '
            f'keyPoints="0;0;1;1" keyTimes="0;{a};{b};1"/></circle>')


def hero(c):
    W, H = 1200, 360
    rows = [178, 245, 312]
    P = []
    P.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
             f'role="img" aria-label="Pavlo Zamroz. Animated banner: a patient\'s records leave a clinic through three '
             f'channels; combined, they re-identify the patient; with a risk gate in place, one channel is refused and '
             f'the combination no longer points to the patient.">')
    P.append('<defs>')
    for name, col in (("clay", c["clay"]), ("slate", c["slate"]), ("grey", c["frame"])):
        P.append(f'<marker id="a-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                 f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
    P.append('</defs>')
    # name and one line
    P.append(text(40, 52, "Pavlo Zamroz", 30, c["navy"], "bold"))
    P.append(text(40, 82, "Re-identification risk of medical data in AI systems · PhD candidate, Lviv Polytechnic", 16,
                  c["muted"]))
    # clinic boundary
    P.append(f'<rect x="190" y="125" width="420" height="225" fill="{c["boundary"]}" stroke="{c["frame"]}" stroke-width="1.5"/>')
    P.append(text(204, 147, "Clinic", 13, c["muted"]))
    # patient (player) and records (storage)
    P.append(f'<rect x="40" y="220" width="110" height="50" fill="none" stroke="{c["player"]}" stroke-width="1.6"/>')
    P.append(text(95, 251, "Patient", 15, c["text"], anchor="middle"))
    P.append(f'<rect x="220" y="220" width="110" height="50" rx="4" fill="{c["bg"]}" stroke="{c["frame"]}" stroke-width="1.4"/>')
    P.append(f'<rect x="220" y="220" width="7" height="50" fill="{c["frame"]}"/>')
    P.append(text(279, 251, "Records", 15, c["text"], anchor="middle"))
    # flows that point to the patient
    P.append(f'<path d="M150,245 L218,245" stroke="{c["clay"]}" stroke-width="2.2" marker-end="url(#a-clay)"/>')
    P.append(f'<path d="M330,245 L448,245" stroke="{c["clay"]}" stroke-width="2.2" marker-end="url(#a-clay)"/>')
    # risk gate (own contribution) — faint while it is "off"
    gate_on = frac(6.0)
    P.append(f'<g opacity="0.3"><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" '
             f'values="0.3;0.3;1;1;0.3" keyTimes="0;{frac(5.7)};{gate_on};{frac(11.7)};1"/>'
             f'<rect x="450" y="160" width="130" height="172" rx="12" fill="{c["own"]}" stroke="{c["navy"]}" stroke-width="2"/>'
             + text(515, 152, "Risk gate", 15, c["navy"], "bold", "middle") + '</g>')
    # three channels and their recipients (players)
    names = ["Researchers", "External LLM", "Trained model"]
    for k, (y, n) in enumerate(zip(rows, names)):
        line = (f'<path d="M580,{y} L716,{y}" stroke="{c["slate"]}" stroke-width="2.2" stroke-dasharray="7 5" '
                f'marker-end="url(#a-slate)">')
        if k == 2:  # refused channel fades while the gate is on
            line += (f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" '
                     f'values="1;1;0.2;0.2;1" keyTimes="0;{frac(7.6)};{frac(7.8)};{frac(11.6)};1"/>')
        P.append(line + '</path>')
        P.append(f'<rect x="720" y="{y - 22}" width="140" height="44" fill="none" stroke="{c["player"]}" stroke-width="1.6"/>')
        P.append(text(790, y + 5, n, 15, c["text"], anchor="middle"))
        P.append(f'<path d="M860,{y} L986,245" stroke="{c["frame"]}" stroke-width="1.6" stroke-dasharray="2 5" '
                 f'marker-end="url(#a-grey)"/>')
    # linkage (adversary): lights up when the channels combine
    P.append(f'<rect x="990" y="220" width="160" height="50" fill="{c["bg"]}" stroke="{c["player"]}" stroke-width="1.6">'
             f'<animate attributeName="fill" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
             f'values="{c["bg"]};{c["clay_tint"]};{c["bg"]}" keyTimes="0;{frac(4.0)};{frac(5.7)}"/>'
             f'<animate attributeName="stroke" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
             f'values="{c["player"]};{c["clay"]};{c["player"]}" keyTimes="0;{frac(4.0)};{frac(5.7)}"/></rect>')
    P.append(text(1050, 251, "Linkage", 15, c["text"], anchor="middle"))
    # the re-identified patient: a small figure that appears in the linkage box
    P.append(f'<g opacity="0" fill="{c["clay"]}">{visible(4.0, 5.7)}'
             f'<circle cx="1122" cy="236" r="6"/><path d="M1110,262 a12,12 0 0 1 24,0 z"/></g>')
    # refusal mark on the third channel
    P.append(f'<g opacity="0" stroke="{c["navy"]}" stroke-width="3" stroke-linecap="round">{visible(7.7, 11.6)}'
             f'<path d="M600,302 L620,322 M620,302 L600,322"/></g>')
    # phase A: no gate — every channel carries the patient, the combination finds them
    for y in rows:
        P.append(dot(f"M150,245 L450,245 L580,{y} L720,{y}", 0.4, 3.0, c["clay"]))
        P.append(dot(f"M860,{y} L990,245", 3.0, 3.9, c["clay"]))
    # phase B: gate on — measured, de-identified, one channel refused, the combination finds nobody
    P.append(dot("M150,245 L450,245", 6.4, 7.6, c["clay"]))
    for y in rows[:2]:
        P.append(dot(f"M580,{y} L720,{y}", 7.7, 8.7, c["slate"]))
        P.append(dot(f"M860,{y} L990,245", 8.8, 9.7, c["slate"]))
    P.append('</svg>')
    return "\n".join(P)


# ---- path: research only, on one time axis ------------------------------------------------------------
Y0, Y1, X0, X1 = 2023.0, 2027.9, 190, 1180


def X(year):
    return round(X0 + (year - Y0) * (X1 - X0) / (Y1 - Y0), 1)


LINES = [
    # (name, colour key, y, segments, stations); station = (year, title, note, label above?, planned?)
    ("Research", "navy", 100, [(2023.7, 2026.95, "solid"), (2026.95, 2027.5, "planned")], [
        (2023.7, "PhD", "Lviv Polytechnic", True, False),
        (2024.9, "First paper", "Comput. Syst. Netw.", False, False),
        (2026.3, "MCP-HAF", "journal article", True, False),
        (2026.88, "LEA-2026", "two papers", False, False),
        (2027.5, "Defense", "planned", True, True),
    ]),
    ("Collaboration", "blue", 210, [(2024.0, 2026.95, "solid"), (2026.95, 2027.05, "planned")], [
        (2024.0, "State project", "No. 0124U002340", True, False),
        (2026.8, "IMT Atlantique", "visiting, Brest", True, False),
        (2027.05, "LaTIM", "seminar, Jan 2027", False, True),
    ]),
]


def path_map(c):
    W, H = 1220, 300
    P = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="Research path drawn like a metro map, 2023 to 2027: the PhD at Lviv Polytechnic from 2023, '
         f'the first paper in 2024, the MCP-HAF journal article in 2026, two LEA-2026 papers and the planned defense; '
         f'a state research project from 2024, the visit to IMT Atlantique in 2026 and a LaTIM seminar in January 2027.">']
    for yr in range(2023, 2028):
        x = X(yr)
        P.append(f'<line x1="{x}" y1="45" x2="{x}" y2="255" stroke="{c["grid"]}" stroke-width="1"/>')
        P.append(text(x, 280, str(yr), 12, c["muted"], anchor="middle"))
    for name, key, y, segs, stations in LINES:
        col = c[key]
        P.append(text(20, y + 5, name, 15, col, "bold"))
        for a, b, kind in segs:
            if kind == "planned":
                P.append(f'<line x1="{X(a)}" y1="{y}" x2="{X(b)}" y2="{y}" stroke="{col}" stroke-width="3" '
                         f'stroke-dasharray="4 5"/>')
            else:
                P.append(f'<line x1="{X(a)}" y1="{y}" x2="{X(b)}" y2="{y}" stroke="{col}" stroke-width="7" '
                         f'stroke-linecap="round"/>')
        for yr, title, note, above, planned in stations:
            x = X(yr)
            dash = ' stroke-dasharray="3 3"' if planned else ""
            P.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{c["bg"]}" stroke="{col}" stroke-width="3"{dash}/>')
            ty = y - 34 if above else y + 30
            P.append(text(x, ty, title, 13, c["text"], "bold", "middle"))
            if note:
                P.append(text(x, ty + 15, note, 11.5, c["muted"], anchor="middle"))
    P.append('</svg>')
    return "\n".join(P)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for mode, c in THEMES.items():
        (OUT / f"hero-{mode}.svg").write_text(hero(c), encoding="utf8")
        (OUT / f"path-{mode}.svg").write_text(path_map(c), encoding="utf8")
    print("written:", sorted(p.name for p in OUT.glob("*.svg")))
